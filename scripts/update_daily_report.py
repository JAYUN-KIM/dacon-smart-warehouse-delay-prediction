import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\open")
PORTFOLIO = ROOT / "dacon-smart-warehouse-portfolio"
DOCS = PORTFOLIO / "docs"


KNOWN_PUBLIC = [
    ("baseline", 11.83),
    ("a48_v4_3", 10.1477),
    ("a56_3", 10.1276),
    ("a66_5", 10.1260335184),
    ("a75_01", 10.122152212),
    ("a76_01", 10.121563682),
    ("a77_01", 10.1214405285),
    ("a79_01", 10.1214263184),
    ("a81_01", 10.121418246),
]


def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_candidate_head(path: Path, n: int = 5):
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    header = lines[0].split(",")
    rows = []
    for line in lines[1 : n + 1]:
        vals = line.split(",")
        rows.append(dict(zip(header, vals)))
    return rows


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    summaries = {
        "a79": read_candidate_head(ROOT / "a79_candidates" / "a79_candidates_summary.csv", 3),
        "a80": read_candidate_head(ROOT / "a80_candidates" / "a80_candidates_summary.csv", 3),
        "a81": read_candidate_head(ROOT / "a81_candidates" / "a81_candidates_summary.csv", 3),
    }
    metrics = {
        "a79": read_json(ROOT / "a79_assets" / "a79_metrics.json"),
        "a80": read_json(ROOT / "a80_assets" / "a80_metrics.json"),
        "a81": read_json(ROOT / "a81_assets" / "a81_metrics.json"),
    }

    best_name, best_score = min(KNOWN_PUBLIC, key=lambda x: x[1])

    daily_report = []
    daily_report.append(f"# Daily Report\n")
    daily_report.append(f"- Generated at: {now}")
    daily_report.append(f"- Current best public score: `{best_score}`")
    daily_report.append(f"- Current best file: `{best_name}`")
    daily_report.append("")
    daily_report.append("## Recent Branch Status")

    for key in ["a79", "a80", "a81"]:
        daily_report.append(f"### {key.upper()}")
        metric = metrics.get(key)
        if metric:
            for k, v in metric.items():
                if isinstance(v, (int, float)):
                    daily_report.append(f"- {k}: `{v}`")
        else:
            daily_report.append("- metrics not found")

        top_rows = summaries.get(key) or []
        if top_rows:
            daily_report.append("- top candidates:")
            for row in top_rows:
                file_name = row.get("file_name", "NA")
                name = row.get("name", "NA")
                score = row.get("oof_mae", row.get("rank_score", "NA"))
                daily_report.append(f"  - `{file_name}` | `{name}` | metric `{score}`")
        else:
            daily_report.append("- candidate summary not found")
        daily_report.append("")

    (DOCS / "daily_report.md").write_text("\n".join(daily_report), encoding="utf-8")

    snapshot = {
        "generated_at": now,
        "best_public": {"name": best_name, "score": best_score},
        "known_public_scores": [{"name": n, "score": s} for n, s in KNOWN_PUBLIC],
        "recent_metrics": metrics,
    }
    (DOCS / "status_snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Updated:")
    print(DOCS / "daily_report.md")
    print(DOCS / "status_snapshot.json")


if __name__ == "__main__":
    main()

