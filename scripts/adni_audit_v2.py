#!/usr/bin/env python3
"""Read-only, standard-library ADNI audit for a mounted SMB/CIFS archive.

Commands:
  python adni_audit_v2.py inventory --root /mount/GeXinting/ADNI --depth 3 --out audit_quick.json
  python adni_audit_v2.py inventory --root /mount/GeXinting/ADNI --scope data --depth 8 --seconds 300 --out audit_data.json
  python adni_audit_v2.py clinical --csv /mount/GeXinting/ADNI/clinical/ADNIMERGE.csv --out audit_clinical.json

Never alters the dataset. Does not export patient IDs, exam dates, paths,
file-level names or any row data. Output: aggregate counts and recognized
clinical table basenames/column names only. The inventory does not read image
pixels and does not stat every file (to reduce SMB round-trips).
"""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import time

TOP_FOLDERS = ('data', 'processed_data', 'raw_data', 'recon_all_new')
KNOWN_MODALITIES = ('t1_nii', 't1_dcm', 'dti_nii', 'dti_dcm',
                    'fmri_nii', 'fmri_dcm', 'amyloid_nii', 'amyloid_dcm',
                    'tau_nii', 'tau_dcm')
EXTENSIONS = ('.nii.gz', '.nii', '.dcm', '.dicom', '.ima', '.mgz', '.mgh',
              '.csv', '.tsv', '.xlsx', '.xls', '.json', '.xml', '.stats',
              '.bvec', '.bval', '.npy', '.npz', '.pkl', '.h5', '.zip',
              '.tar.gz', '.gz', '.txt', '.png', '.jpg', '.log')
TABLE_KEYWORDS = ('adnimerge', 'registry', 'diagnos', 'dxsum', 'mmse',
                  'moca', 'adas', 'cdr', 'ravlt', 'roster', 'datadic',
                  'blchange', 'ucsf', 'visit', 'clinical', 'neuropsych',
                  'petmeta', 'mrifreesurfer', 'qc')
RECOGNIZED_FIELDS = ('RID', 'PTID', 'VISCODE', 'VISCODE2', 'EXAMDATE',
                     'IMAGEUID', 'DX', 'DX_bl', 'DXCHANGE', 'AGE', 'PTGENDER',
                     'PTEDUCAT', 'Month', 'MMSE', 'ADAS13', 'CDRSB', 'MOCA',
                     'RAVLT.immediate', 'ABETA', 'AV45', 'FLDSTRENG',
                     'Hippocampus', 'ICV')
FS_NAMES = ('aseg.stats', 'lh.aparc.stats', 'rh.aparc.stats',
            'lh.aparc.a2009s.stats', 'rh.aparc.a2009s.stats',
            'wmparc.stats')
ID_PATTERN = re.compile(r'\d{3}_s_\d{4}', re.IGNORECASE)


def kind(name):
    value = name.lower()
    for suffix in sorted(EXTENSIONS, key=len, reverse=True):
        if value.endswith(suffix):
            return suffix
    return '[no extension]' if '.' not in name else '[other]'


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def write_report(path, report):
    output = Path(path).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Report written:', output)
    print('No subject IDs, individual rows, scan dates, source paths or credentials are exported.')


def read_csv_header(path):
    try:
        with open(path, 'r', newline='', encoding='utf-8-sig', errors='replace') as handle:
            first_line = handle.readline(32768)
        if not first_line:
            return []
        delimiter = '\t' if path.lower().endswith('.tsv') else ','
        fields = next(csv.reader([first_line], delimiter=delimiter), [])
        return [name.strip() for name in fields]
    except (OSError, UnicodeError, csv.Error):
        return []


def inventory(args):
    root = Path(args.root).expanduser().absolute()
    if not root.is_dir():
        raise SystemExit('The ADNI root path is missing or inaccessible.')
    if root.name.lower() != 'adni':
        raise SystemExit('For safety, --root must point to the ADNI directory itself.')
    if args.depth < 0 or args.max_entries <= 0 or args.seconds <= 0:
        raise SystemExit('Depth must be >= 0 and the limits must be positive.')
    if args.scope == 'all':
        scan_root = root
    else:
        scan_root = root / args.scope
    if not scan_root.is_dir():
        raise SystemExit('Requested scope directory does not exist in the ADNI root.')

    start = time.monotonic()
    sections = defaultdict(lambda: {'directories': 0, 'files': 0, 'file_types': Counter()})
    modalities = Counter()
    fs_stats = Counter()
    candidates = []
    clinical_tables_seen = 0
    header_reads = 0
    max_candidates = 60
    stack = [(str(scan_root), 0)]
    files = directories = entries = errors = symlinks = beyond_depth = 0
    stop_reason = None

    while stack:
        if time.monotonic() - start >= args.seconds:
            stop_reason = 'time_limit'
            break
        folder, depth = stack.pop()
        try:
            with os.scandir(folder) as iterator:
                for entry in iterator:
                    entries += 1
                    if entries >= args.max_entries:
                        stop_reason = 'entry_limit'
                        break
                    if time.monotonic() - start >= args.seconds:
                        stop_reason = 'time_limit'
                        break
                    try:
                        if entry.is_symlink():
                            symlinks += 1
                            continue
                        relative = os.path.relpath(entry.path, root)
                        section = relative.split(os.sep, 1)[0] if relative != '.' else '[root]'
                        if section not in TOP_FOLDERS:
                            section = '[other-in-ADNI]' if args.scope == 'all' else args.scope
                        if entry.is_dir(follow_symlinks=False):
                            directories += 1
                            sections[section]['directories'] += 1
                            low = entry.name.lower()
                            if low in KNOWN_MODALITIES:
                                modalities[low] += 1
                            if depth < args.depth:
                                stack.append((entry.path, depth + 1))
                            else:
                                beyond_depth += 1
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        files += 1
                        sections[section]['files'] += 1
                        extension = kind(entry.name)
                        sections[section]['file_types'][extension] += 1
                        low = entry.name.lower()
                        if low in FS_NAMES:
                            fs_stats[low] += 1
                        if extension in ('.csv', '.tsv', '.xlsx', '.xls'):
                            clinical_tables_seen += 1
                            if any(word in low for word in TABLE_KEYWORDS):
                                if len(candidates) < max_candidates and not ID_PATTERN.search(low):
                                    record = {'table_basename': entry.name, 'section': section}
                                    if extension in ('.csv', '.tsv') and header_reads < args.max_headers:
                                        cols = read_csv_header(entry.path)
                                        cols_lower = {col.lower() for col in cols}
                                        record['column_count'] = len(cols)
                                        record['recognized_columns'] = [
                                            field for field in RECOGNIZED_FIELDS
                                            if field.lower() in cols_lower
                                        ]
                                        header_reads += 1
                                    candidates.append(record)
                    except OSError:
                        errors += 1
        except OSError:
            errors += 1
        if stop_reason:
            break

    report = {
        'report_type': 'adni_inventory_v2',
        'created_utc': stamp(),
        'root_label': 'ADNI',
        'scope': args.scope,
        'scan_limits': {'max_directory_depth': args.depth,
                        'max_entries': args.max_entries,
                        'max_seconds': args.seconds},
        'scan_results': {'elapsed_seconds': round(time.monotonic() - start, 1),
                         'entries_seen': entries, 'files_seen': files,
                         'directories_seen': directories,
                         'errors': errors, 'symlinks_skipped': symlinks,
                         'directories_beyond_depth_not_scanned': beyond_depth,
                         'stopped_by': stop_reason or 'directory_tree_exhausted',
                         'complete': stop_reason is None and beyond_depth == 0},
        'sections': {name: {'directories': data['directories'],
                            'files': data['files'],
                            'file_types': dict(data['file_types'].most_common())}
                     for name, data in sorted(sections.items())},
        'named_modality_directories_found': dict(sorted(modalities.items())),
        'freesurfer_stats_files_seen': dict(sorted(fs_stats.items())),
        'tabular_files_seen': clinical_tables_seen,
        'clinical_candidate_tables_sample': candidates,
        'warnings': [
            'Counts are files, not independent people, sessions or scan quality.',
            'A missing table in an INCOMPLETE/depth-limited scan does not mean it is absent.',
            'No pixel data read. No file-size stats to avoid SMB metadata overhead.',
            'No data on AD diagnosis, future cognitive outcomes or scan matching is proven yet.'
        ]
    }
    write_report(args.out, report)
    print(json.dumps(report['scan_results'], ensure_ascii=False, indent=2))
    print('Clinical candidates:', len(candidates),
          '| FreeSurfer stats:', sum(fs_stats.values()),
          '| Named modality folders:', sum(modalities.values()))


def number(text):
    if text is None:
        return None
    word = str(text).strip()
    if word in ('', '-4', '-1', '-9', 'NA', 'NaN', 'nan', 'N/A', 'NULL'):
        return None
    try:
        value = float(word)
        return value if math.isfinite(value) else None
    except ValueError:
        return None


def month_from_record(row, keys):
    for col in ('Month', 'MONTH', 'Month_bl'):
        key = keys.get(col.lower())
        if key:
            value = number(row.get(key))
            if value is not None and value >= 0:
                return int(round(value))
    for col in ('VISCODE2', 'VISCODE'):
        key = keys.get(col.lower())
        if not key:
            continue
        code = str(row.get(key, '')).lower().strip()
        if code in ('bl', 'baseline'):
            return 0
        match = re.fullmatch(r'm(\d{1,3})', code)
        if match:
            return int(match.group(1))
    return None


def clinical(args):
    path = Path(args.csv).expanduser().absolute()
    if not path.is_file() or path.suffix.lower() not in ('.csv', '.tsv'):
        raise SystemExit('Specify an accessible CSV/TSV file.')
    start = time.monotonic()
    sep = '\t' if path.suffix.lower() == '.tsv' else ','
    ids = defaultdict(lambda: {'visits': set(), 'scores': defaultdict(set),
                               'baseline_scores': set(), 'future_scores': defaultdict(set),
                               'diagnosis_at_baseline': None})
    diagnosis_counter = Counter()
    row_count = 0
    missing_id_rows = 0
    bad_score_rows = Counter()
    id_col = None
    available_scores = ['MMSE', 'ADAS13', 'CDRSB', 'MOCA']
    fields = []
    with open(path, 'r', newline='', encoding='utf-8-sig', errors='replace') as handle:
        reader = csv.DictReader(handle, delimiter=sep)
        fields = [f.strip() for f in (reader.fieldnames or []) if f]
        keys = {col.lower(): col for col in (reader.fieldnames or []) if col}
        id_col = keys.get('rid') or keys.get('ptid')
        score_keys = {s: keys.get(s.lower()) for s in available_scores}
        diag_key = keys.get('dx') or keys.get('diagnosis')
        if not id_col:
            raise SystemExit('No RID or PTID column; use a compatible ADNI clinical table.')
        for row in reader:
            row_count += 1
            pid = str(row.get(id_col, '')).strip()
            if not pid or pid in ('-4', 'NA'):
                missing_id_rows += 1
                continue
            visit = month_from_record(row, keys)
            patient = ids[pid]
            if visit is not None:
                patient['visits'].add(visit)
            if diag_key:
                diagnosis = str(row.get(diag_key) or '').strip()
                if diagnosis and diagnosis != '-4':
                    diagnosis_counter[diagnosis[:40]] += 1
                    if visit == 0:
                        patient['diagnosis_at_baseline'] = diagnosis[:40]
            for score_name, key in score_keys.items():
                if not key:
                    continue
                value = number(row.get(key))
                valid = value is not None and value >= 0
                if score_name in ('MMSE', 'MOCA'):
                    valid = valid and value <= 30 if valid else False
                if not valid:
                    bad_score_rows[score_name] += 1
                    continue
                if visit is not None:
                    patient['scores'][score_name].add(visit)
                    if visit == 0:
                        patient['baseline_scores'].add(score_name)
                    if visit > 0:
                        patient['future_scores'][score_name].add(visit)
            if args.max_rows and row_count >= args.max_rows:
                break

    score_summary = {}
    for score in available_scores:
        if not any(col.lower() == score.lower() for col in fields):
            continue
        score_summary[score] = {
            'subjects_with_valid_dated_score': sum(bool(p['scores'][score]) for p in ids.values()),
            'subjects_with_2plus_timepoints': sum(len(p['scores'][score]) >= 2 for p in ids.values()),
            'subjects_with_baseline_and_later': sum(
                score in p['baseline_scores'] and bool(p['future_scores'][score])
                for p in ids.values()),
            'subjects_baseline_and_month_9_15': sum(
                score in p['baseline_scores'] and any(9 <= m <= 15 for m in p['future_scores'][score])
                for p in ids.values()),
            'subjects_baseline_and_month_18_30': sum(
                score in p['baseline_scores'] and any(18 <= m <= 30 for m in p['future_scores'][score])
                for p in ids.values())
        }
    baseline_dx = Counter(p['diagnosis_at_baseline'] for p in ids.values()
                          if p['diagnosis_at_baseline'])
    report = {
        'report_type': 'adni_clinical_summary_v2', 'created_utc': stamp(),
        'input_basename': path.name if not ID_PATTERN.search(path.name) else '[redacted]',
        'elapsed_seconds': round(time.monotonic() - start, 1),
        'records_read': row_count, 'subjects_with_identifier': len(ids),
        'rows_missing_identifier': missing_id_rows,
        'partially_read_due_to_limit': bool(args.max_rows and row_count >= args.max_rows),
        'recognized_fields': [col for col in RECOGNIZED_FIELDS if col.lower() in {f.lower() for f in fields}],
        'subjects_with_visit_codes': sum(bool(p['visits']) for p in ids.values()),
        'subjects_with_2plus_visit_codes': sum(len(p['visits']) >= 2 for p in ids.values()),
        'baseline_diagnosis_values_counts': dict(baseline_dx.most_common(20)),
        'clinical_score_feasibility': score_summary,
        'notes': [
            'Only aggregate counts are exported; subject IDs remain in process memory.',
            'Counts are NOT yet linked to local T1 NIfTI or FreeSurfer results.',
            'Month 9-15 and 18-30 are heuristic follow-up windows, not predictive evaluation cohorts.',
            'Missing value conventions and diagnosis labels must be verified against the ADNI data dictionary.',
            'If Month/VISCODE is missing, dated trajectory counts are underestimates.'
        ]
    }
    write_report(args.out, report)
    print('Clinical rows:', row_count, '| subjects:', len(ids))
    for score, summary in score_summary.items():
        print(score, '| with baseline+later:', summary['subjects_with_baseline_and_later'])


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('inventory', help='Fast bounded metadata inventory (no image reads)')
    p.add_argument('--root', required=True, help='Mounted path ending in /GeXinting/ADNI')
    p.add_argument('--scope', choices=('all',) + TOP_FOLDERS, default='all')
    p.add_argument('--depth', type=int, default=3, help='Max levels of subdirectories to enter (default: 3)')
    p.add_argument('--seconds', type=int, default=120, help='Soft time limit (default: 120)')
    p.add_argument('--max-entries', type=int, default=100000,
                   help='Maximum directory entries to inspect (default: 100000)')
    p.add_argument('--max-headers', type=int, default=25,
                   help='Maximum matched CSV headers to read (default: 25)')
    p.add_argument('--out', default='adni_inventory_v2.json')
    p.set_defaults(func=inventory)
    q = sub.add_parser('clinical', help='Aggregate visit and cognitive score counts from a selected clinical CSV')
    q.add_argument('--csv', required=True, help='ADNIMERGE-like clinical CSV/TSV')
    q.add_argument('--out', default='adni_clinical_summary_v2.json')
    q.add_argument('--max-rows', type=int, default=0, help='Optional row cap; 0 means read whole CSV')
    q.set_defaults(func=clinical)
    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == '__main__':
    main()
