import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\open")
PORTFOLIO = ROOT / "dacon-smart-warehouse-portfolio"
DOCS = PORTFOLIO / "docs"
DAILY_LOGS = DOCS / "daily_logs"
PUBLIC_SCORE_LOG = DOCS / "public_score_log.json"

DEFAULT_PUBLIC = [
    {"date": "2026-04-01", "name": "baseline", "score": 11.83, "file": "submission_baseline.csv", "note": "baseline"},
    {"date": "2026-04-10", "name": "a48_v4_3", "score": 10.1477, "file": "submission_a48_v4_3.csv", "note": "strong ensemble base"},
    {"date": "2026-04-12", "name": "a56_3", "score": 10.1276, "file": "submission_a56_3.csv", "note": "STT + TransLF + a48"},
    {"date": "2026-04-13", "name": "a66_5", "score": 10.1260335184, "file": "submission_a66_5.csv", "note": "TransLF ratio increased"},
    {"date": "2026-04-17", "name": "a75_01", "score": 10.122152212, "file": "submission_a75_01.csv", "note": "residual CatBoost jump"},
    {"date": "2026-04-17", "name": "a76_01", "score": 10.121563682, "file": "submission_a76_01.csv", "note": "anchor2 residual"},
    {"date": "2026-04-18", "name": "a77_01", "score": 10.1214405285, "file": "submission_a77_01.csv", "note": "anchor3 residual"},
    {"date": "2026-04-18", "name": "a79_01", "score": 10.1214263184, "file": "submission_a79_01.csv", "note": "sequence residual branch"},
    {"date": "2026-04-18", "name": "a81_01", "score": 10.121418246, "file": "submission_a81_01.csv", "note": "sequence residual v2"},
]


def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_public_score_log():
    if not PUBLIC_SCORE_LOG.exists():
        PUBLIC_SCORE_LOG.write_text(
            json.dumps(DEFAULT_PUBLIC, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


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


def read_public_scores():
    ensure_public_score_log()
    data = read_json(PUBLIC_SCORE_LOG) or []
    data = sorted(data, key=lambda x: (x.get("score", 999), x.get("date", "")))
    return data


def list_recent_candidate_dirs():
    rows = []
    for path in ROOT.glob("a*_candidates"):
        if path.is_dir():
            summary = path / f"{path.name}_summary.csv"
            if summary.exists():
                rows.append((path.name.replace("_candidates", ""), summary, summary.stat().st_mtime))
    rows.sort(key=lambda x: x[2], reverse=True)
    return rows[:5]


def summarize_recent_experiments():
    experiments = []
    for name, summary_path, _ in list_recent_candidate_dirs():
        top_rows = read_candidate_head(summary_path, 3)
        experiments.append({"name": name, "summary_path": summary_path, "top_rows": top_rows})
    return experiments


def build_delta_text(public_scores):
    if len(public_scores) < 2:
        return "이전 기록과 비교할 정보가 충분하지 않습니다."
    best = min(public_scores, key=lambda x: x["score"])
    prev = sorted(public_scores, key=lambda x: x["date"])[-2]
    diff = prev["score"] - best["score"]
    return (
        f"현재 최고는 `{best['name']}` / `{best['score']}`이고, "
        f"직전 기록 `{prev['name']}` / `{prev['score']}` 대비 `{diff:.9f}` 개선되었습니다."
    )


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    DAILY_LOGS.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    public_scores = read_public_scores()
    best_public = min(public_scores, key=lambda x: x["score"])
    recent_experiments = summarize_recent_experiments()
    metrics = {
        "a79": read_json(ROOT / "a79_assets" / "a79_metrics.json"),
        "a80": read_json(ROOT / "a80_assets" / "a80_metrics.json"),
        "a81": read_json(ROOT / "a81_assets" / "a81_metrics.json"),
    }

    daily_report = []
    daily_report.append(f"# Daily Report\n")
    daily_report.append(f"- Generated at: {now}")
    daily_report.append(f"- Current best public score: `{best_public['score']}`")
    daily_report.append(f"- Current best file: `{best_public['name']}`")
    daily_report.append(f"- Summary: {build_delta_text(public_scores)}")
    daily_report.append("")
    daily_report.append("## Recent Branch Status")

    for exp in recent_experiments:
        key = exp["name"]
        daily_report.append(f"### {key.upper()}")
        metric = metrics.get(key)
        if metric:
            for k, v in metric.items():
                if isinstance(v, (int, float)):
                    daily_report.append(f"- {k}: `{v}`")
        else:
            daily_report.append("- metrics not found")

        top_rows = exp["top_rows"]
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

    log_lines = []
    log_lines.append(f"# {today}")
    log_lines.append("")
    log_lines.append(f"- Generated at: {now}")
    log_lines.append(f"- Current best public: `{best_public['name']}` / `{best_public['score']}`")
    log_lines.append(f"- Change summary: {build_delta_text(public_scores)}")
    log_lines.append("")
    log_lines.append("## What Changed Today")
    log_lines.append("- 최신 실험 브랜치와 후보 파일 기준으로 자동 요약")
    for exp in recent_experiments:
        log_lines.append(f"- `{exp['name']}` 후보 생성/업데이트 확인")
        for row in exp["top_rows"][:2]:
            log_lines.append(
                f"  - top: `{row.get('file_name', 'NA')}` | `{row.get('name', 'NA')}` | metric `{row.get('oof_mae', row.get('rank_score', 'NA'))}`"
            )
    log_lines.append("")
    log_lines.append("## Public Score Log")
    for row in sorted(public_scores, key=lambda x: x["date"], reverse=True)[:5]:
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
    (DOCS / "status_snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Updated:")
    print(DOCS / "daily_report.md")
    print(DAILY_LOGS / f"{today}.md")
    print(DOCS / "status_snapshot.json")


if __name__ == "__main__":
    main()
