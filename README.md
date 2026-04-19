# DACON Smart Warehouse Delay Prediction

개인 대회 연구 레포입니다.  
데이콘 스마트 창고 출고 지연 예측 AI 경진대회에서, 향후 30분 평균 출고 지연 시간(`avg_delay_minutes_next_30m`)을 예측하기 위해 진행한 모델링, 앙상블, 실험 로그를 정리합니다.

## Project Summary

- Competition: DACON Smart Warehouse Delay Prediction
- Metric: MAE
- Goal: public/private generalization이 좋은 sequence + residual ensemble 설계
- Current best public score: `10.1214032792`
- Current best file: `submission_a83_01.csv`

## What I Worked On

- layout-free feature engineering
- Transformer / STT / LSTM / LightGBM base model 실험
- residual CatBoost stack (`a75~a78`)
- sequence residual models (`a79`, `a81`)
- layout-aware residual / layout-aware sequence residual (`a82`, `a83`)
- low-band correction / selective blending / gating 실험

## Repository Structure

- `docs/project_overview.md`
  프로젝트와 데이터, 실험 흐름 요약
- `docs/resume_summary.md`
  이력서/포트폴리오용 요약 문서
- `docs/experiment_log.md`
  주요 실험 흐름과 best score 기록
- `docs/daily_logs/`
  날짜별 작업 기록과 변화 요약
- `docs/public_score_log.json`
  public score와 제출 파일 기록
- `scripts/update_daily_report.py`
  현재 작업 폴더를 읽어 일일 요약과 날짜별 로그를 자동 생성

## Daily Workflow

1. 실험 코드 실행
2. `python scripts/update_daily_report.py`
3. 변경된 `docs/` 확인
4. commit / push

## Key Highlights

- `a75` residual CatBoost에서 큰 폭의 점수 개선
- `a79`에서 sequence residual branch를 추가해 새로운 error pattern 확보
- `a81`에서 `a79` anchor 기반 sequence residual V2로 추가 개선
- `a82`에서 layout-aware residual expert를 추가해 정적 warehouse 구조 정보를 반영
- `a83`에서 layout-aware sequence residual로 정적 layout + 동적 sequence를 함께 학습
- 매일 작업 로그와 실험 변화가 자동으로 문서화되도록 관리
