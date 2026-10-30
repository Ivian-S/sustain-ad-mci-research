#!/usr/bin/env python3
"""Privacy-conscious, read-only profile of a suffix-merged ADNI XLSX workbook.

Understands source-specific fields including RID_reg, RID_DXSUM,
MMSCORE_MMSE, TOTAL13_ADAS, CDRSB_CDR, MOCA_MOCA, and Subject ID_T1.

Important: sources are profiled independently. This script NEVER assumes that
columns on the same Excel row represent the same participant or visit.
It reports row-wise identifier/visit agreement to help detect bad joins.

Only aggregates and approved column names go to JSON; individual IDs, dates,
score rows, file paths, and patient records are not emitted.
This is a preliminary audit, not a valid clinical cohort assembly or MRI match.

Requires openpyxl. Usage:
  python3 scripts/adni_xlsx_audit_v2.py schema --xlsx data/all.xlsx \\
    --out results/data_audit/07_schema_v2.json
  python3 scripts/adni_xlsx_audit_v2.py cohort --xlsx data/all.xlsx \\
    --sheet 1 --out results/data_audit/08_cohort_v2.json

Use --max-rows 500 for a quick partial test; omit for a full scan.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import json
import math
import re
import sys
import time

try:
    import openpyxl
except ImportError:
    sys.exit('openpyxl not installed. Use an environment with openpyxl available.')

VERSION = '2.0.0'
SOURCES = [
    'reg', 'ADAS', 'CDR', 'DXSUM', 'GDSCALE', 'MMSE', 'MOCA', 'NEUROBAT',
    'NPI', 'UCBERKELEY', 'UGOTPTAU181', 'UWNPSYCHSUM',
    'T1', 'Tau', 'DTI', 'FMRI', 'Amyloid',
]
GROUPS = {x.upper(): x for x in SOURCES}
SCHEMA_FIELDS = {
    'reg': ['RID','PTID','PHASE','VISCODE','VISCODE2','EXAMDATE','PTSTATUS'],
    'ADAS': ['RID','PTID','VISCODE','VISCODE2','VISDATE','TOTAL13','TOTSCORE'],
    'CDR': ['RID','PTID','VISCODE','VISCODE2','VISDATE','CDRSB','CDGLOBAL'],
    'DXSUM': ['RID','VISCODE','VISCODE2','EXAMDATE','DIAGNOSIS','DXCURREN','DXCHANGE'],
    'MMSE': ['RID','PTID','VISCODE','VISCODE2','VISDATE','MMSCORE'],
    'MOCA': ['RID','PTID','VISCODE','VISCODE2','VISDATE','MOCA'],
    'NEUROBAT': ['RID','PTID','VISCODE','VISCODE2','VISDATE','TRABSCOR','AVTOT1','AVTOT5','AVDELTOT'],
    'UCBERKELEY': ['RID','PTID','VISCODE','VISCODE2','SCANDATE','LONIUID','TRACER','qc_flag','AMYLOID_STATUS','CENTILOIDS'],
    'UWNPSYCHSUM': ['RID','VISCODE','VISCODE2','EXAMDATE','ADNI_MEM','ADNI_EF'],
    'UGOTPTAU181': ['RID','VISCODE','VISCODE2','EXAMDATE','PLASMAPTAU181'],
    'T1': ['Subject ID','Image ID','Study Date','Visit','Research Group','Description'],
    'Tau': ['Subject ID','Image ID','Study Date','Visit'],
    'DTI': ['Subject ID','Image ID','Study Date','Visit'],
    'FMRI': ['Subject ID','Image ID','Study Date','Visit'],
    'Amyloid': ['Subject ID','Image ID','Study Date','Visit'],
    'GDSCALE': ['RID','PTID','VISCODE2','GDTOTAL'],
    'NPI': ['RID','PTID','VISCODE2','NPITOTAL'],
}
FIELDS = {g: {re.sub(r'[^A-Z0-9]', '', f.upper()): f for f in fs} for g,fs in SCHEMA_FIELDS.items()}
SCORE_SPECS = {
    'MMSE': ('MMSE','MMSCORE',0,30),
    'ADAS13': ('ADAS','TOTAL13',0,85),
    'ADAS11': ('ADAS','TOTSCORE',0,70),
    'CDRSB': ('CDR','CDRSB',0,18),
    'MOCA': ('MOCA','MOCA',0,30),
    'ADNI_MEM': ('UWNPSYCHSUM','ADNI_MEM',None,None),
    'ADNI_EF': ('UWNPSYCHSUM','ADNI_EF',None,None),
}
MISSING = {'','NA','N/A','NAN','NONE','NULL','MISSING','-1','-4','-9','-999','--','.'}
VISIT_RE = re.compile(r'^m0*(\d+)$',re.I)


def clean_header(x):
    return str(x).strip() if x is not None else ''


def canonical(x):
    return re.sub(r'[^A-Z0-9]','',str(x).upper())


def parse_header(name):
    # Source suffix after final underscore (e.g. 'Study Date_T1').
    name = clean_header(name)
    if '_' not in name:
        return None
    stem, suffix = name.rsplit('_',1)
    group = GROUPS.get(suffix.upper())
    return (group, canonical(stem)) if group else None


def is_missing(value):
    if value is None: return True
    if isinstance(value,float) and not math.isfinite(value): return True
    if isinstance(value,(int,float)) and not isinstance(value,bool) and value in (-1,-4,-9,-999): return True
    if isinstance(value,str): return value.strip().upper() in MISSING
    return False


def normalize_rid(v):
    if is_missing(v) or isinstance(v,bool): return None
    if isinstance(v,float):
        if not v.is_integer(): return None
        v = int(v)
    s = str(v).strip()
    if re.fullmatch(r'\d+\.0',s): s=s[:-2]
    if not re.fullmatch(r'\d{1,8}',s): return None
    return str(int(s))


def normalize_ptid(v):
    if is_missing(v): return None
    s = str(v).strip().upper().replace(' ','')
    # Do not infer RID from PTID. Compare only the full exact PTID string.
    return s if 1 <= len(s) <= 36 else None


def parse_visit(v):
    if is_missing(v): return None
    s=str(v).strip().lower()
    if s in ('bl','baseline','m0','m00'): return 'm0'
    if s in ('sc','screening'): return 'sc'
    m=VISIT_RE.fullmatch(s)
    if m: return 'm'+str(int(m.group(1)))
    # Other visit identifiers retained only for internal set membership;
    # no raw visit tokens are exported.
    return 'other:'+s[:40] if s else None


def score_value(v, minimum, maximum):
    if is_missing(v) or isinstance(v,bool):return None, 'missing'
    try: x=float(v)
    except (TypeError,ValueError): return None, 'invalid'
    if not math.isfinite(x):return None, 'invalid'
    if minimum is not None and (x < minimum or x > maximum):return None,'out_of_range'
    return x,'valid'


def suppress(n):
    return '<5' if 0<n<5 else n


def extract_header(ws, rownum):
    ws.reset_dimensions()  # Guard against incorrect declared worksheet dimensions.
    return [clean_header(x) for x in next(ws.iter_rows(min_row=rownum,max_row=rownum,values_only=True),())]


def get_schema(headers):
    buckets=defaultdict(list)
    matched=defaultdict(dict)
    for i, name in enumerate(headers):
        parsed=parse_header(name)
        if not parsed:continue
        g, c=parsed
        buckets[g].append(i)
        if c in FIELDS.get(g,{}):
            matched[g].setdefault(c,i)
    return {
        'header_column_count':len(headers),
        'recognized_suffixed_columns':sum(map(len,buckets.values())),
        'group_column_counts':{g:len(buckets.get(g,())) for g in SOURCES},
        'recognized_research_fields':{
            g:[{'field':FIELDS[g][c],'column_1based':i+1} for c,i in sorted(matched.get(g,{}).items(),key=lambda x:x[1])]
            for g in SOURCES if matched.get(g)
        },
        'flags':{
            'has_t1_imaging_metadata':all(x in matched.get('T1',{}) for x in ('SUBJECTID','IMAGEID')),
            'has_cognitive_scores':any(canonical(field) in matched.get(g,{}) for _,(g,field,_,_) in SCORE_SPECS.items()),
            'has_diagnosis_table': 'RID' in matched.get('DXSUM',{}),
            'has_amyloid_status_column': 'AMYLOIDSTATUS' in matched.get('UCBERKELEY',{}),
            'has_direct_t1_roi_volumes': False,
        },
    }, matched


def at(row, matched, group, name):
    i=matched.get(group,{}).get(canonical(name))
    return row[i] if i is not None and i<len(row) else None


def group_id(row, matched, group):
    rid=normalize_rid(at(row,matched,group,'RID'))
    if rid:return ('RID',rid)
    ptid=normalize_ptid(at(row,matched,group,'PTID'))
    if not ptid:ptid=normalize_ptid(at(row,matched,group,'Subject ID'))
    return ('PTID',ptid) if ptid else None


def group_visit(row,matched,group):
    for key in ('VISCODE2','VISCODE','Visit'):
        s=parse_visit(at(row,matched,group,key))
        if s:return s
    return None


def dx_category(row, matched):
    # DXSUM-only precedence; no phase inference or claiming biologic AD.
    for field in ('DIAGNOSIS','DXCURREN','DXCHANGE'):
        v=at(row,matched,'DXSUM',field)
        if is_missing(v):continue
        s=str(v).strip()
        if s.endswith('.0'):s=s[:-2]
        if field=='DXCHANGE':
            d={'1':'CU','7':'CU','9':'CU','2':'MCI','4':'MCI','8':'MCI',
               '3':'Dementia','5':'Dementia','6':'Dementia'}
        else:d={'1':'CU','2':'MCI','3':'Dementia'}
        return d.get(s,'Unmapped'),field
    return None,None


def amyloid_label(value):
    # Only clear textual labels. Numeric status codes require a codebook.
    if is_missing(value):return None
    s=re.sub(r'\s+','',str(value).strip().lower())
    if s in {'positive','pos','a+','amyloidpositive','amyloid+'}:
        return 'positive_text_label'
    if s in {'negative','neg','a-','amyloidnegative','amyloid-'}:
        return 'negative_text_label'
    return 'requires_data_dictionary'


def profile(ws, matched, row_limit, progress_every, header_row):
    t0=time.monotonic()
    ws.reset_dimensions()
    counters=Counter()
    subjects={g:set() for g in SOURCES}
    rid_sets={g:set() for g in SOURCES}
    ptid_sets={g:set() for g in SOURCES}
    visits={g:defaultdict(set) for g in SOURCES}
    pairs={g:set() for g in SOURCES}
    source_duplicates=Counter()
    registry_rid_to_ptids=defaultdict(set)
    registry_ptid_to_rids=defaultdict(set)
    scores={key:{'subjects':set(),'visits':defaultdict(set),'valid_rows':0,'out_of_range_rows':0,
                 'invalid_rows':0,'subjects_bl':set(),'subjects_sc':set()} for key in SCORE_SPECS}
    dx_bl=defaultdict(set)
    dx_all=Counter()
    amyloid=Counter()
    amyloid_subjects=defaultdict(set)
    match_stats=Counter()
    checked_pair_rid={('reg','MMSE'),('reg','ADAS'),('reg','DXSUM'),('MMSE','ADAS'),('MMSE','CDR'),('DXSUM','MMSE'),('UCBERKELEY','DXSUM')}
    checked_pair_ptid={('T1','reg'),('T1','MMSE'),('T1','ADAS'),('T1','UCBERKELEY'),('T1','CDR')}
    incomplete=False
    for row in ws.iter_rows(min_row=header_row+1,values_only=True):
        if row_limit and counters['rows_scanned']>=row_limit:
            incomplete=True
            break
        counters['rows_scanned']+=1
        if progress_every and counters['rows_scanned']%progress_every==0:
            print('Scanned '+str(counters['rows_scanned'])+' rows...',file=sys.stderr,flush=True)
        current_ids={}
        current_visits={}
        current_rids={}
        current_ptids={}
        for g in SOURCES:
            sid=group_id(row,matched,g)
            if sid is None:continue
            current_ids[g]=sid
            subjects[g].add(sid)
            counters['records_'+g]+=1
            v=group_visit(row,matched,g)
            current_visits[g]=v
            if v:
                visits[g][sid].add(v)
                key=(sid,v)
                if key in pairs[g]:source_duplicates[g]+=1
                pairs[g].add(key)
            rid=normalize_rid(at(row,matched,g,'RID'))
            ptid=normalize_ptid(at(row,matched,g,'PTID')) or normalize_ptid(at(row,matched,g,'Subject ID'))
            if rid:rid_sets[g].add(rid);current_rids[g]=rid
            if ptid:ptid_sets[g].add(ptid);current_ptids[g]=ptid
        if len(current_rids)>=2:
            match_stats['rows_two_plus_rid']+=1
            if len(set(current_rids.values()))>1:match_stats['rows_rid_mismatch']+=1
        if len(current_ptids)>=2:
            match_stats['rows_two_plus_ptid']+=1
            if len(set(current_ptids.values()))>1:match_stats['rows_ptid_mismatch']+=1
        reg_rid=current_rids.get('reg')
        reg_ptid=current_ptids.get('reg')
        if reg_rid and reg_ptid:
            registry_rid_to_ptids[reg_rid].add(reg_ptid)
            registry_ptid_to_rids[reg_ptid].add(reg_rid)
        for a,b in checked_pair_rid:
            if a in current_rids and b in current_rids:
                label='RID_'+a+'__'+b
                match_stats[label+'_both']+=1
                if current_rids[a]==current_rids[b]:
                    match_stats[label+'_match']+=1
                    if (current_visits.get(a) is not None and current_visits.get(b) is not None):
                        match_stats[label+'_visit_known']+=1
                        if current_visits[a]==current_visits[b]:match_stats[label+'_visit_match']+=1
        for a,b in checked_pair_ptid:
            if a in current_ptids and b in current_ptids:
                label='PTID_'+a+'__'+b
                match_stats[label+'_both']+=1
                if current_ptids[a]==current_ptids[b]:
                    match_stats[label+'_match']+=1
                    if (current_visits.get(a) is not None and current_visits.get(b) is not None):
                        match_stats[label+'_visit_known']+=1
                        if current_visits[a]==current_visits[b]:match_stats[label+'_visit_match']+=1
        for name,(g,field,minimum,maximum) in SCORE_SPECS.items():
            if canonical(field) not in matched.get(g,{}):continue
            val=at(row,matched,g,field)
            _,state=score_value(val,minimum,maximum)
            if state=='valid':
                s=scores[name]
                s['valid_rows']+=1
                sid=current_ids.get(g)
                if sid:
                    s['subjects'].add(sid)
                    visit=current_visits.get(g)
                    if visit:
                        s['visits'][sid].add(visit)
                        if visit=='m0':s['subjects_bl'].add(sid)
                        if visit=='sc':s['subjects_sc'].add(sid)
            elif state=='invalid':scores[name]['invalid_rows']+=1
            elif state=='out_of_range':scores[name]['out_of_range_rows']+=1
        dx,field=dx_category(row,matched)
        if dx:
            dx_all[dx]+=1
            sid=current_ids.get('DXSUM')
            if sid and current_visits.get('DXSUM')=='m0':dx_bl[dx].add(sid)
        raw_amyloid=at(row,matched,'UCBERKELEY','AMYLOID_STATUS')
        label=amyloid_label(raw_amyloid)
        if label:
            amyloid[label]+=1
            sid=current_ids.get('UCBERKELEY')
            if sid:amyloid_subjects[label].add(sid)
    score_out={}
    for name,s in scores.items():
        if canonical(SCORE_SPECS[name][1]) not in matched.get(SCORE_SPECS[name][0],{}):continue
        vv=s['visits']
        def count_visit(code):return sum(code in x for x in vv.values())
        score_out[name]={
            'valid_observation_rows':s['valid_rows'],
            'unique_subjects_with_valid_score':len(s['subjects']),
            'invalid_or_nonnumeric_rows':s['invalid_rows'],
            'out_of_range_rows':s['out_of_range_rows'],
            'unique_subjects_with_2plus_distinct_visits':sum(len(x)>=2 for x in vv.values()),
            'unique_subjects_with_bl':len(s['subjects_bl']),
            'unique_subjects_with_screening':len(s['subjects_sc']),
            'unique_subjects_with_m12':count_visit('m12'),
            'unique_subjects_with_m24':count_visit('m24'),
            'unique_subjects_with_bl_and_m12':sum({'m0','m12'}.issubset(x) for x in vv.values()),
            'unique_subjects_with_bl_and_m24':sum({'m0','m24'}.issubset(x) for x in vv.values()),
        }
    source_out={}
    for g in SOURCES:
        if not matched.get(g) and not subjects[g]:continue
        source_out[g]={
            'nonempty_subject_rows':counters['records_'+g],
            'unique_subjects_from_available_identifier':len(subjects[g]),
            'unique_RID':len(rid_sets[g]) if 'RID' in matched.get(g,{}) else None,
            'unique_PTID':len(ptid_sets[g]) if any(z in matched.get(g,{}) for z in ('PTID','SUBJECTID')) else None,
            'unique_subject_visit_pairs':len(pairs[g]),
            'duplicate_subject_visit_rows':source_duplicates[g],
            'unique_subjects_with_2plus_visits':sum(len(x)>=2 for x in visits[g].values()),
        }
    pairs_out={}
    for kind,a,b in [ ('rid','DXSUM','MMSE'),('rid','DXSUM','ADAS'),('rid','MMSE','ADAS'),
                       ('rid','MMSE','CDR'),('rid','UCBERKELEY','DXSUM'),('rid','reg','DXSUM'),
                       ('ptid','T1','reg'),('ptid','T1','MMSE'),('ptid','T1','ADAS'),
                       ('ptid','T1','UCBERKELEY'),('ptid','T1','CDR')]:
        A=rid_sets[a] if kind=='rid' else ptid_sets[a]
        B=rid_sets[b] if kind=='rid' else ptid_sets[b]
        if A and B:pairs_out[f'{kind.upper()}_{a}__{b}']=len(A&B)
    unique_registry_map={
        rid:next(iter(ptids))
        for rid,ptids in registry_rid_to_ptids.items()
        if len(ptids)==1 and len(registry_ptid_to_rids[next(iter(ptids))])==1
    }
    inverse_registry_map={ptid:rid for rid,ptid in unique_registry_map.items()}
    t1_matched_rids={inverse_registry_map[ptid] for ptid in ptid_sets['T1'] if ptid in inverse_registry_map}
    def to_rids(subject_set):
        return {idval for typ,idval in subject_set if typ=='RID'}
    mmse_long_rids={sid[1] for sid,v in scores['MMSE']['visits'].items() if sid[0]=='RID' and len(v)>=2}
    dx_bl_mci=to_rids(dx_bl['MCI'])
    dx_bl_cu=to_rids(dx_bl['CU'])
    dx_bl_dementia=to_rids(dx_bl['Dementia'])
    mmse_available_rids=to_rids(scores['MMSE']['subjects'])
    adas_available_rids=to_rids(scores['ADAS13']['subjects'])
    amyloid_status_rids={label:to_rids(subject_set) for label,subject_set in amyloid_subjects.items()}
    can_map=bool(unique_registry_map)
    preliminary_intersections={
        'registry_unique_one_to_one_RID_PTID_pairs':len(unique_registry_map),
        'registry_ambiguous_RIDs':sum(len(v)!=1 for v in registry_rid_to_ptids.values()),
        'registry_ambiguous_PTIDs':sum(len(v)!=1 for v in registry_ptid_to_rids.values()),
        't1_subjects_with_one_to_one_registry_RID_mapping':len(t1_matched_rids) if can_map else None,
        't1_mapped_RID_and_any_valid_MMSE':len(t1_matched_rids & mmse_available_rids) if can_map else None,
        't1_mapped_RID_and_valid_ADAS13':len(t1_matched_rids & adas_available_rids) if can_map else None,
        't1_mapped_RID_and_MMSE_2plus_visit_codes':len(t1_matched_rids & mmse_long_rids) if can_map else None,
        't1_mapped_RID_and_DXSUM_baseline_MCI':len(t1_matched_rids & dx_bl_mci) if can_map else None,
        't1_mapped_RID_and_DXSUM_baseline_CU':len(t1_matched_rids & dx_bl_cu) if can_map else None,
        't1_mapped_RID_and_DXSUM_baseline_Dementia':len(t1_matched_rids & dx_bl_dementia) if can_map else None,
        't1_mapped_RID_and_baseline_MCI_and_MMSE_2plus_visit_codes':len(t1_matched_rids & dx_bl_mci & mmse_long_rids) if can_map else None,
        't1_mapped_RID_and_amyloid_explicit_positive_label':len(t1_matched_rids & amyloid_status_rids.get('positive_text_label',set())) if can_map else None,
    }
    # Registry crosswalk and subject intersections are provisional: no dates,
    # image UID checks, tracer harmonization or quality control are applied.
    row_align={
        'rows_with_2plus_RID_fields':match_stats['rows_two_plus_rid'],
        'rows_with_conflicting_RID_fields':match_stats['rows_rid_mismatch'],
        'rows_with_2plus_PTID_fields':match_stats['rows_two_plus_ptid'],
        'rows_with_conflicting_PTID_fields':match_stats['rows_ptid_mismatch'],
        'selected_pairwise_checks':{}
    }
    for kind,pa in [('RID',checked_pair_rid),('PTID',checked_pair_ptid)]:
        for a,b in sorted(pa):
            label=kind+'_'+a+'__'+b
            row_align['selected_pairwise_checks'][label]={
                'both_present_on_same_row':match_stats[label+'_both'],
                'matching_subject_id_on_same_row':match_stats[label+'_match'],
                'same_subject_and_both_visits_present':match_stats[label+'_visit_known'],
                'same_subject_and_matching_visit_code':match_stats[label+'_visit_match'],
            }
    warnings=[
        'This table is source-suffixed: each source was profiled independently. DO NOT treat aligned Excel row numbers as joined participant-visits without verification.',
        'Subject overlaps across sources do not prove same-visit matching; visit dates, ID mappings, QC, and image IDs remain to be checked.',
        'T1 subject IDs are PTIDs; no RID conversion is attempted without checking ROSTER/matching evidence.',
        'DXSUM counts are clinical diagnoses, not biomarker-confirmed AD; code mappings require confirmation by ADNI phase.',
        'Amyloid status is only a screening candidate. Text labels and imaging QC/tracer must be validated before defining A+.',
        'No clinical score was assumed to be on the same visit as a differently suffixed source on the same Excel row.',
        'Output aggregates may still be subject to institutional disclosure controls. No patient-level data are exported.'
    ]
    if match_stats['rows_two_plus_rid'] and match_stats['rows_rid_mismatch']:
        warnings.append('Conflicting RID values appear on the same Excel rows; do NOT join columns by row position.')
    if match_stats['rows_two_plus_ptid'] and match_stats['rows_ptid_mismatch']:
        warnings.append('Conflicting PTID values appear on the same Excel rows; imaging/clinical sources may be stacked side-by-side.')
    if incomplete:warnings.append('Partial scan: maximum row count reached. Counts are not full-dataset estimates.')
    return {
        'rows_scanned':counters['rows_scanned'],
        'complete_rows_read':not incomplete,
        'sources':source_out,
        'cognitive_scores':score_out,
        'diagnoses_DXSUM':{
            'observations_by_harmonized_clinical_group':{k:suppress(v) for k,v in dx_all.items()},
            'unique_baseline_subjects_by_group':{k:suppress(len(v)) for k,v in dx_bl.items()},
            'baseline_requires_VISCODE2_bl':True,
        },
        'amyloid_UCBERKELEY':{
            'observation_rows_by_label':{k:suppress(v) for k,v in amyloid.items()},
            'unique_subjects_by_label':{k:suppress(len(v)) for k,v in amyloid_subjects.items()},
        },
        'set_intersections_unmatched_for_visit':{k:suppress(v) for k,v in pairs_out.items()},
        'provisional_subject_only_intersections_not_image_matched':{k:(suppress(v) if isinstance(v,int) else v) for k,v in preliminary_intersections.items()},
        'same_row_identity_checks':row_align,
        'warnings':warnings,
        'elapsed_seconds':round(time.monotonic()-t0,2),
    }


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    sub=p.add_subparsers(dest='mode',required=True)
    for m in ('schema','cohort'):
        a=sub.add_parser(m)
        a.add_argument('--xlsx',required=True)
        a.add_argument('--out',required=True)
        a.add_argument('--sheet',type=int,default=1,help='1-based sheet index; default 1')
        a.add_argument('--header-row',type=int,default=1)
        if m=='cohort':
            a.add_argument('--max-rows',type=int,default=0,help='0=all rows; >0 for trial scan')
            a.add_argument('--progress-every',type=int,default=1000)
    args=p.parse_args()
    if args.sheet<1 or args.header_row<1:p.error('--sheet and --header-row must be >= 1')
    xlsx=Path(args.xlsx)
    if not xlsx.is_file():p.error('Input workbook does not exist (path is not printed for privacy)')
    start=time.monotonic()
    book=openpyxl.load_workbook(xlsx,read_only=True,data_only=True)
    try:
        if args.sheet>len(book.worksheets):p.error('Sheet index out of range')
        ws=book.worksheets[args.sheet-1]
        declared_rows,declared_cols=ws.max_row,ws.max_column
        headers=extract_header(ws,args.header_row)
        schema,matched=get_schema(headers)
        report={
            'script_version':VERSION,
            'mode':args.mode,
            'sheet_count':len(book.worksheets),
            'sheet_index_1based':args.sheet,
            'declared_rows_unverified':declared_rows,
            'declared_columns_unverified':declared_cols,
            'schema':schema,
            'privacy':'No raw patient records, patient IDs, dates, or file paths exported.',
        }
        if args.mode=='cohort':
            report['cohort_audit']=profile(ws,matched,args.max_rows,args.progress_every,args.header_row)
        report['total_elapsed_seconds']=round(time.monotonic()-start,2)
    finally:
        book.close()
    outfile=Path(args.out)
    outfile.parent.mkdir(parents=True,exist_ok=True)
    outfile.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Wrote aggregate report (no patient-level rows):',outfile)
    if args.mode=='cohort':
        print('Read rows:',report['cohort_audit']['rows_scanned'],
              'complete:',report['cohort_audit']['complete_rows_read'])


if __name__=='__main__':main()
