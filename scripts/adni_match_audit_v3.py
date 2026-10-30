#!/usr/bin/env python3
"""Read-only ADNI wide-XLSX feasibility audit.

This script never exports subject IDs, visit dates, or row-level clinical records.
It independently reconstructs source tables by RID/PTID and real examination date.
It DOES NOT verify image files on disk, diagnose AD, or classify numeric amyloid codes.

Run from the SuStaIn project root:
  python3 scripts/adni_match_audit_v3.py --xlsx data/all.xlsx \
      --out results/data_audit/09_matched_feasibility_v3.json

Requires: openpyxl.  Data are read locally.  Inspect summary before sharing.
"""
import argparse
import collections
import datetime as dt
import json
import math
import re
import sys
import time
from pathlib import Path

try:
    import openpyxl
    from openpyxl.utils.datetime import from_excel
except ImportError:
    raise SystemExit("Install openpyxl in the current environment: python3 -m pip install openpyxl")

COG = {
    "MMSE": ("RID_MMSE", "VISDATE_MMSE", "MMSCORE_MMSE", 0, 30),
    "ADAS13": ("RID_ADAS", "VISDATE_ADAS", "TOTAL13_ADAS", 0, 85),
    "CDRSB": ("RID_CDR", "VISDATE_CDR", "CDRSB_CDR", 0, 18),
    "MOCA": ("RID_MOCA", "VISDATE_MOCA", "MOCA_MOCA", 0, 30),
}
DX_MAP = {1: "CU", 2: "MCI", 3: "Dementia"}
DX_CHANGE_MAP = {1: "CU", 7: "CU", 9: "CU", 2: "MCI", 4: "MCI", 8: "MCI", 3: "Dementia", 5: "Dementia", 6: "Dementia"}


def clean(v):
    return str(v).strip() if v is not None else ""


def norm_rid(v):
    s = clean(v)
    if not s or s.lower() in ("nan", "none", "na"):
        return None
    try:
        k = float(s)
        if k.is_integer() and k > 0 and math.isfinite(k):
            return str(int(k))
    except (ValueError, OverflowError):
        pass
    return None


def norm_ptid(v):
    s = clean(v).upper()
    if s.startswith("ADNI_"):
        s = s[5:]
    if not s or s in {"NA", "NONE", "NAN"}:
        return None
    return s


def parse_date(v, epoch):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if 20000 <= v <= 80000:
            try:
                x = from_excel(v, epoch=epoch)
                return x.date() if isinstance(x, dt.datetime) else x
            except (ValueError, TypeError, OverflowError):
                pass
    s = clean(v)
    if not s or s.upper() in {"NA", "NAN", "NONE", "-4"}:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y.%m.%d", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    try:
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def valid_score(v, low, high):
    try:
        if v is None or isinstance(v, bool):
            return None
        x = float(str(v).strip())
        return round(x, 5) if math.isfinite(x) and low <= x <= high else None
    except ValueError:
        return None


def choose_diag(row):
    """Prefer harmonized DIAGNOSIS, then ADNI1 DXCURREN, then GO/2 DXCHANGE.
    Codes are provisional pending phase-specific QC; report origin counts.
    """
    for field, mapping in (("DIAGNOSIS_DXSUM", DX_MAP), ("DXCURREN_DXSUM", DX_MAP), ("DXCHANGE_DXSUM", DX_CHANGE_MAP)):
        x = row(field)
        if x is None or str(x).strip() == "":
            continue
        try:
            numeric = int(float(x))
            if float(x) == numeric and numeric in mapping:
                return (mapping[numeric], field)
        except (ValueError, TypeError, OverflowError):
            pass
    return (None, None)


def safe_status_category(value):
    if value is None or clean(value) == "":
        return None
    s = clean(value).lower().replace(" ", "")
    pos = {"positive", "pos", "a+", "amyloidpositive", "elevated"}
    neg = {"negative", "neg", "a-", "amyloidnegative", "notelevated"}
    if s in pos:
        return "explicit_positive_text"
    if s in neg:
        return "explicit_negative_text"
    try:
        x = float(s)
        if math.isfinite(x) and x == int(x) and abs(x) < 10:
            return "numeric_code_" + str(int(x)) + "_UNINTERPRETED"
        return "numeric_other_UNINTERPRETED"
    except ValueError:
        return "other_text_UNINTERPRETED"


def suppress_small(n):
    return n if n == 0 or n >= 5 else "<5"


def closest(records, when, max_days):
    """Return nearest dated record; ties prefer past; exclude contradictory same-day entries."""
    possible = [r for r in records if abs((r[0] - when).days) <= max_days]
    if not possible:
        return None
    possible.sort(key=lambda r: (abs((r[0] - when).days), r[0] > when, r[0]))
    anchor_date = possible[0][0]
    options = [r for r in possible if r[0] == anchor_date]
    labels = {r[1] for r in options}
    if len(labels) > 1:
        return None  # conflicting readings on the selected date
    return options[0]


def has_followup(records, index, target_days=None, tol=180):
    """Require post-index follow-ups; target at 12/24 months uses actual dates."""
    if target_days is None:
        return any((r[0] - index).days >= 180 for r in records)
    return any(max(180, target_days - tol) <= (r[0] - index).days <= target_days + tol for r in records)


def inspect(path, out, max_rows, cog_window, dx_window, amy_window):
    started = time.time()
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    ws.reset_dimensions()  # don't trust declared XLSX dimensions
    it = ws.iter_rows(values_only=True)
    try:
        header = next(it)
    except StopIteration:
        raise ValueError("Workbook has no header row")
    names = [clean(x) for x in header]
    ix = {name: i for i, name in enumerate(names) if name}
    required = ["PTID_reg", "RID_reg", "Subject ID_T1", "Study Date_T1", "Image ID_T1",
                "RID_DXSUM", "EXAMDATE_DXSUM", "RID_MMSE", "VISDATE_MMSE", "MMSCORE_MMSE"]
    missing = [n for n in required if n not in ix]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    # Only aggregate output: patient-level data stay in memory, are never written.
    p2r = collections.defaultdict(set)
    r2p = collections.defaultdict(set)
    scans = collections.defaultdict(dict)
    diag = collections.defaultdict(dict)
    cognition = {name: collections.defaultdict(dict) for name in COG}
    amyloid = collections.defaultdict(dict)
    counts = collections.Counter()
    src_counts = collections.Counter()
    date_counts = collections.Counter()
    amy_status_codes = collections.Counter()

    for n, vals in enumerate(it, 1):
        if max_rows and n > max_rows:
            break
        counts["rows_scanned"] += 1
        def get(k):
            j = ix.get(k)
            return vals[j] if j is not None and j < len(vals) else None

        rid, ptid = norm_rid(get("RID_reg")), norm_ptid(get("PTID_reg"))
        if rid and ptid:
            p2r[ptid].add(rid)
            r2p[rid].add(ptid)

        tptid = norm_ptid(get("Subject ID_T1"))
        if tptid:
            src_counts["T1_rows_with_subject"] += 1
            date = parse_date(get("Study Date_T1"), wb.epoch)
            iid = clean(get("Image ID_T1"))
            if date:
                date_counts["T1_rows_with_parsable_date"] += 1
                if iid:
                    src_counts["T1_rows_with_image_id_and_date"] += 1
                key = (iid if iid else "noid", date)
                scans[tptid][key] = (date, bool(iid))
            else:
                date_counts["T1_rows_without_parsable_date"] += 1

        did = norm_rid(get("RID_DXSUM"))
        if did:
            src_counts["DXSUM_rows_with_rid"] += 1
            ddate = parse_date(get("EXAMDATE_DXSUM"), wb.epoch)
            group, origin = choose_diag(get)
            if ddate:
                date_counts["DXSUM_rows_with_parsable_date"] += 1
            if ddate and group:
                key = (ddate, group)
                diag[did][key] = (ddate, group, origin)
                counts["DXSUM_rows_with_mapped_diagnosis"] += 1
            elif ddate and not group:
                counts["DXSUM_rows_with_date_but_unmapped_diagnosis"] += 1

        for name, (ridfield, datefield, valfield, low, high) in COG.items():
            r = norm_rid(get(ridfield))
            if not r:
                continue
            src_counts[name + "_rows_with_rid"] += 1
            dd = parse_date(get(datefield), wb.epoch)
            if dd:
                date_counts[name + "_rows_with_parsable_date"] += 1
            x = valid_score(get(valfield), low, high)
            if dd and x is not None:
                cognition[name][r][(dd, x)] = (dd, x)
                src_counts[name + "_rows_valid_dated_score"] += 1
            elif x is not None and not dd:
                counts[name + "_valid_score_missing_date"] += 1

        arid = norm_rid(get("RID_UCBERKELEY"))
        if arid:
            src_counts["amyloid_rows_with_rid"] += 1
            dd = parse_date(get("SCANDATE_UCBERKELEY"), wb.epoch)
            if dd:
                date_counts["amyloid_rows_with_parsable_date"] += 1
            category = safe_status_category(get("AMYLOID_STATUS_UCBERKELEY"))
            if category:
                amy_status_codes[category] += 1
            if dd and category:
                amyloid[arid][(dd, category)] = (dd, category)

        if n % 4000 == 0:
            print(f"Read {n} local XLSX rows...", file=sys.stderr)

    wb.close()
    complete = not bool(max_rows) or counts["rows_scanned"] < max_rows

    # Use one-to-one RID/PTID relationship; do not infer from aligned Excel row numbers.
    mapping = {p: next(iter(rs)) for p, rs in p2r.items()
               if len(rs) == 1 and len(r2p[next(iter(rs))]) == 1}
    t1_all = set(scans)
    t1_mapped = t1_all.intersection(mapping)
    group_stats = {g: collections.Counter() for g in ("CU", "MCI", "Dementia")}
    allstats = collections.Counter()
    for ptid in sorted(t1_mapped):
        rid = mapping[ptid]
        arr = sorted(set(scans[ptid].values()), key=lambda r: r[0])
        dxarr = list(diag[rid].values())
        bycog = {c: list(cognition[c][rid].values()) for c in COG}
        my_amy = list(amyloid[rid].values())
        if not arr:
            continue
        allstats["t1_subjects_with_any_dated_scan"] += 1
        if any(has_id for _, has_id in arr):
            allstats["t1_subjects_with_any_dated_image_id"] += 1

        candidates = []
        any_diag, any_score = False, False
        for scan_date, image_id_present in arr:
            diagnosis = closest(dxarr, scan_date, dx_window)
            scores = {c: closest(bycog[c], scan_date, cog_window) for c in COG}
            any_diag |= diagnosis is not None
            any_score |= any(x is not None for x in scores.values())
            if image_id_present and diagnosis and any(x is not None for x in scores.values()):
                candidates.append((scan_date, diagnosis, scores))
        if any_diag:
            allstats["t1_subjects_with_diagnosis_near_any_scan"] += 1
        if any_score:
            allstats["t1_subjects_with_cognition_near_any_scan"] += 1
        if not candidates:
            continue
        # Strict candidate: MRI image ID, diagnosis and cognitive score on the *same* T1 date window.
        # Use earliest such scan as a provisional baseline (not confirmed image file or QC).
        scan_date, diagnosis, scores = sorted(candidates, key=lambda x: x[0])[0]
        label = diagnosis[1]
        allstats["t1_subjects_with_diagnosis_and_any_cognitive_near_same_scan"] += 1
        group_stats[label]["n_t1_dx_any_cognition"] += 1
        for c, base in scores.items():
            if base is None:
                continue
            group_stats[label]["baseline_" + c] += 1
            # Index is when all model inputs became available, preventing within-window future-score leakage.
            index_date = max(scan_date, base[0])
            recordset = bycog[c]
            for suffix, target in (("followup_6m_plus", None), ("followup_12m_window", 365), ("followup_24m_window", 730)):
                if has_followup(recordset, index_date, target):
                    group_stats[label][c + "_" + suffix] += 1

        if my_amy:
            amy_record = closest(my_amy, scan_date, amy_window)
            if amy_record:
                group_stats[label]["amyloid_record_near_T1_UNVERIFIED_STATUS"] += 1
                if amy_record[1] == "explicit_positive_text":
                    group_stats[label]["amyloid_explicit_positive_text_near_T1"] += 1
                elif amy_record[1].startswith("numeric_code_"):
                    group_stats[label]["amyloid_numeric_status_near_T1_NEEDS_DICTIONARY"] += 1

    def smallsafe(d):
        return {key: suppress_small(val) for key, val in sorted(d.items())}

    summary = {
        "script_version": "3.0.0",
        "audit_purpose": "Locally anchored T1-MRI / diagnosis / cognition date-window feasibility; not final cohort selection",
        "read_complete": complete,
        "rows_read": counts["rows_scanned"],
        "source_field_qc": {
            "source_rows": smallsafe(src_counts),
            "date_parse_coverage": smallsafe(date_counts),
            "mapped_diagnosis_rows": counts["DXSUM_rows_with_mapped_diagnosis"],
            "unmapped_diagnosis_rows_with_dates": counts["DXSUM_rows_with_date_but_unmapped_diagnosis"],
            "valid_cognitive_score_without_date": smallsafe({k:v for k,v in counts.items() if k.endswith("valid_score_missing_date")}),
        },
        "registry": {
            "unique_one_to_one_ptid_rid_pairs": len(mapping),
            "ambiguous_ptids": suppress_small(sum(len(rs) != 1 for rs in p2r.values())),
            "ambiguous_rids": suppress_small(sum(len(ps) != 1 for ps in r2p.values())),
        },
        "t1_image_metadata": {
            "distinct_ptids_with_a_parseable_T1_scan_date": len(t1_all),
            "distinct_ptids_with_mapping_to_rid": len(t1_mapped),
            "unique_image_id_date_keys_not_file_verified": sum(len(v) for v in scans.values()),
        },
        "subject_level_date_window_feasibility": smallsafe(allstats),
        "diagnostic_groups_on_earliest_qualifying_T1_scan": {k: smallsafe(v) for k,v in group_stats.items()},
        "amyloid_status_value_counts_UNINTERPRETED": smallsafe(amy_status_codes),
        "matching_policy": {
            "diagnosis_window_days_around_T1": dx_window,
            "cognition_window_days_around_T1": cog_window,
            "amyloid_window_days_around_T1": amy_window,
            "6_month_minimum_followup_days": 180,
            "12_and_24_month_tolerance_days": 180,
            "t1_selection": "earliest dated T1 with image ID + date-matched diagnosis + at least one baseline cognitive score",
            "prediction_index": "later of T1 date and cognition baseline measurement date",
        },
        "warnings": [
            "No on-disk NIfTI/DICOM or FreeSurfer subject was matched or QC-verified; T1 records are only metadata.",
            "Imaging/clinical joins use RID-PTID registry and real study/exam dates, not Excel row alignment.",
            "Diagnosis codes are provisionally mapped; ADNI phase/version and harmonized DIAGNOSIS field require review.",
            "A+ is NOT inferred from numeric AMYLOID_STATUS codes; consult UCBERKELEY source data dictionary.",
            "Date-window matching does not establish eligibility, true AD pathology, or out-of-sample prediction.",
            "Cognitive scores measured after MRI are allowed in a baseline window; prediction index is moved to when those scores became available.",
            "Only aggregated counts are exported. Counts below five are suppressed; review report under local disclosure rules.",
        ],
        "elapsed_seconds": round(time.time() - started, 2),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description="Private and read-only ADNI wide-table T1-clinical date-matching feasibility audit")
    p.add_argument("--xlsx", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--max-rows", type=int, default=0, help="0 = read all rows; a positive value is a test ONLY")
    p.add_argument("--cognition-days", type=int, default=90, help="Baseline cognitive score within +/- days of MRI")
    p.add_argument("--diagnosis-days", type=int, default=180, help="Diagnosis within +/- days of MRI")
    p.add_argument("--amyloid-days", type=int, default=365, help="Amyloid status source within +/- days of MRI, unverified")
    args = p.parse_args()
    if args.xlsx.resolve() == args.out.resolve():
        p.error("Input and output must differ")
    if any(x < 0 for x in (args.max_rows, args.cognition_days, args.diagnosis_days, args.amyloid_days)):
        p.error("Window sizes and max rows must be nonnegative")
    try:
        summary = inspect(args.xlsx, args.out, args.max_rows, args.cognition_days, args.diagnosis_days, args.amyloid_days)
    except (ValueError, OSError) as e:
        p.error(str(e))
    print("Saved aggregate-only audit report:", args.out)
    print("Rows:", summary["rows_read"], "complete:", summary["read_complete"])
    print("One-to-one identity matches:", summary["registry"]["unique_one_to_one_ptid_rid_pairs"])
    print("Date-window T1+diagnosis+cognition:", summary["subject_level_date_window_feasibility"].get("t1_subjects_with_diagnosis_and_any_cognitive_near_same_scan", 0))
    print("Note: MRI file existence/QC and amyloid positivity are not verified")


if __name__ == "__main__":
    main()
