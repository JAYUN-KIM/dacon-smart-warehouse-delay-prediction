import json
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\open")
PORTFOLIO = ROOT / "dacon-smart-warehouse-portfolio"
DOCS = PORTFOLIO / "docs"
DAILY_LOGS = DOCS / "daily_logs"
PUBLIC_SCORE_LOG = DOCS / "public_score_log.json"


def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_public_scores():
    data = read_json(PUBLIC_SCORE_LOG) or []
    return sorted(data, key=lambda x: (x.get("date", ""), x.get("score", 999)))


def read_candidate_head(path: Path, n: int = 3):
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) <= 1:
        return []
    header = lines[0].split(",")
    rows = []
    for line in lines[1 : n + 1]:
        values = line.split(",")
        rows.append(dict(zip(header, values)))
    return rows


def list_recent_candidate_dirs(top_k: int = 8):
    rows = []
    for path in ROOT.glob("a*_candidates"):
        if not path.is_dir():
            continue
        summary = path / f"{path.name}_summary.csv"
        if summary.exists():
            rows.append((path.name.replace("_candidates", ""), summary, summary.stat().st_mtime))
    rows.sort(key=lambda x: x[2], reverse=True)
    return rows[:top_k]


def summarize_recent_experiments():
    out = []
    for name, summary_path, _ in list_recent_candidate_dirs():
        out.append(
            {
                "name": name,
                "summary_path": summary_path,
                "top_rows": read_candidate_head(summary_path, 3),
            }
        )
    return out


def build_delta_text(public_scores):
    if len(public_scores) < 2:
        return "Not enough public score history yet."
    best = min(public_scores, key=lambda x: x["score"])
    prev_best_candidates = [x for x in public_scores if x["name"] != best["name"]]
    prev_best = min(prev_best_candidates, key=lambda x: x["score"])
    diff = prev_best["score"] - best["score"]
    return (
        f"Current best is `{best['name']}` / `{best['score']}`. "
        f"Compared with the previous best `{prev_best['name']}` / `{prev_best['score']}`, "
        f"the improvement is `{diff:.9f}`."
    )


def collect_metric_files():
    metrics = {}
    for asset_dir in ROOT.glob("a*_assets"):
        metric_file = asset_dir / f"{asset_dir.name.replace('_assets', '')}_metrics.json"
        if metric_file.exists():
            metrics[asset_dir.name.replace("_assets", "")] = read_json(metric_file)
    return metrics


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    DAILY_LOGS.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    public_scores = read_public_scores()
    best_public = min(public_scores, key=lambda x: x["score"]) if public_scores else {}
    recent_experiments = summarize_recent_experiments()
    metrics = collect_metric_files()

    daily_report = [
        "# Daily Report",
        "",
        f"- Generated at: {now}",
        f"- Current best public score: `{best_public.get('score', 'NA')}`",
        f"- Current best file: `{best_public.get('name', 'NA')}`",
        f"- Summary: {build_delta_text(public_scores)}",
        "",
        "## Recent Branch Status",
    ]

    for exp in recent_experiments:
        key = exp["name"]
        daily_report.append(f"### {key.upper()}")
        metric = metrics.get(key)
        if metric:
            for mk, mv in metric.items():
                if isinstance(mv, (int, float)):
                    daily_report.append(f"- {mk}: `{mv}`")
        else:
            daily_report.append("- metrics not found")
        if exp["top_rows"]:
            daily_report.append("- top candidates:")
            for row in exp["top_rows"]:
                metric_value = row.get("oof_mae", row.get("rank_score", "NA"))
                daily_report.append(
                    f"  - `{row.get('file_name', 'NA')}` | `{row.get('name', 'NA')}` | metric `{metric_value}`"
                )
        daily_report.append("")

    (DOCS / "daily_report.md").write_text("\n".join(daily_report), encoding="utf-8")

    log_lines = [
        f"# {today}",
        "",
        f"- Generated at: {now}",
        f"- Current best public: `{best_public.get('name', 'NA')}` / `{best_public.get('score', 'NA')}`",
        f"- Change summary: {build_delta_text(public_scores)}",
        "",
        "## What Changed Today",
    ]

    for exp in recent_experiments[:6]:
        log_lines.append(f"- `{exp['name']}` candidate branch updated")
        for row in exp["top_rows"][:2]:
            metric_value = row.get("oof_mae", row.get("rank_score", "NA"))
            log_lines.append(
                f"  - top: `{row.get('file_name', 'NA')}` | `{row.get('name', 'NA')}` | metric `{metric_value}`"
            )

    log_lines.append("")
    log_lines.append("## Recent Public Scores")
    for row in sorted(public_scores, key=lambda x: (x["date"], x["score"]), reverse=True)[:6]:
        log_lines.append(
            f"- `{row['date']}` | `{row['name']}` | `{row['score']}` | `{row.get('note', '')}`"
        )

    (DAILY_LOGS / f"{today}.md").write_text("\n".join(log_lines), encoding="utf-8")

    snapshot = {
        "generated_at": now,
        "best_public": best_public,
        "known_public_scores": public_scores,
        "recent_metrics": metrics,
        "recent_experiments": [
            {
                "name": exp["name"],
                "summary_path": str(exp["summary_path"]),
                "top_rows": exp["top_rows"],
            }
            for exp in recent_experiments
        ],
    }
    (DOCS / "status_snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Updated:")
    print(DOCS / "daily_report.md")
    print(DAILY_LOGS / f"{today}.md")
    print(DOCS / "status_snapshot.json")


if __name__ == "__main__":
    main()
