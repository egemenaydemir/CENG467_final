from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parent
EHRSQL_DIR = ROOT / "EHRSQL" / "dataset" / "ehrsql"
OUT_CSV = ROOT / "dataset_info.csv"


def process_file_counts(p):
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # normalize to list of records
    if isinstance(data, dict):
        for key in ("data", "rows", "examples", "instances"):
            if key in data and isinstance(data[key], list):
                records = data[key]
                break
        else:
            # fallback: count keys
            return len(data), 0, 0
    elif isinstance(data, list):
        records = data
    else:
        return 0, 0, 0

    total = 0
    answerable = 0
    unanswerable = 0
    for rec in records:
        total += 1
        if rec.get("is_impossible", False):
            unanswerable += 1
        else:
            answerable += 1
    return total, answerable, unanswerable

def collect_counts(datasets=None):
    results = {}
    if not EHRSQL_DIR.exists():
        raise FileNotFoundError(f"Missing folder: {EHRSQL_DIR}")
    ds_dirs = [d for d in sorted(EHRSQL_DIR.iterdir()) if d.is_dir()]
    for dsdir in ds_dirs:
        dsname = dsdir.name
        results[dsname] = {}
        for split, fname in (("train", "train.json"), ("valid", "valid.json"), ("test", "test.json")):
            p = dsdir / fname
            if not p.exists():
                results[dsname][split] = {"total": 0, "answerable": 0, "unanswerable": 0}
                continue
            total, answerable, unanswerable = process_file_counts(p)
            results[dsname][split] = {"total": total, "answerable": answerable, "unanswerable": unanswerable}
    return results


def write_csv(results, out=OUT_CSV):
    # Write a compact numeric CSV: one row per dataset with numeric columns
    header = [
        "dataset",
        "train_total",
        "train_answerable",
        "train_unanswerable",
        "valid_total",
        "valid_answerable",
        "valid_unanswerable",
        "test_total",
        "test_answerable",
        "test_unanswerable",
    ]
    overall = {k: 0 for k in [
        "train_total",
        "train_answerable",
        "train_unanswerable",
        "valid_total",
        "valid_answerable",
        "valid_unanswerable",
        "test_total",
        "test_answerable",
        "test_unanswerable",
    ]}

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for dsname, splits in sorted(results.items()):
            row = [dsname]
            for split_prefix in ("train", "valid", "test"):
                counts = splits.get(split_prefix, {"total": 0, "answerable": 0, "unanswerable": 0})
                row.extend([counts["total"], counts["answerable"], counts["unanswerable"]])
                overall[f"{split_prefix}_total"] += counts["total"]
                overall[f"{split_prefix}_answerable"] += counts["answerable"]
                overall[f"{split_prefix}_unanswerable"] += counts["unanswerable"]
            writer.writerow(row)
        # write overall totals row (dataset=TOTAL)
        total_row = ["TOTAL"] + [overall[c] for c in [
            "train_total",
            "train_answerable",
            "train_unanswerable",
            "valid_total",
            "valid_answerable",
            "valid_unanswerable",
            "test_total",
            "test_answerable",
            "test_unanswerable",
        ]]
        writer.writerow(total_row)
    return out, overall


def main():
    results = collect_counts()
    out, overall = write_csv(results)
    for dsname, splits in sorted(results.items()):
        for split, counts in splits.items():
            print(f"Dataset `{dsname}` {split}: total {counts['total']}, answerable {counts['answerable']}, unanswerable {counts['unanswerable']}")
    print(f"Saved CSV to: {out}")
    total_all = overall.get("train_total", 0) + overall.get("valid_total", 0) + overall.get("test_total", 0)
    answerable_all = overall.get("train_answerable", 0) + overall.get("valid_answerable", 0) + overall.get("test_answerable", 0)
    unanswerable_all = overall.get("train_unanswerable", 0) + overall.get("valid_unanswerable", 0) + overall.get("test_unanswerable", 0)
    print(f"Overall totals: total {total_all}, answerable {answerable_all}, unanswerable {unanswerable_all}")


if __name__ == '__main__':
    main()

