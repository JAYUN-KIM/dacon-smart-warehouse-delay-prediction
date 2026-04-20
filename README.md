# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 경진대회를 진행하면서 실험한 모델, 점수 변화, 해석, 다음 방향을 정리하는 저장소입니다.

현재는 `avg_delay_minutes_next_30m`를 예측하는 과정에서 단순 블렌딩보다 `shift / unseen / high-regime` 구간을 어떻게 정의하고 보정할지가 핵심이라고 보고 있습니다.

## 현재 최고 기록

- 최고 public 점수: `10.1133848903`
- 제출 파일: `submission_a94_51.csv`
- 핵심 아이디어:
  - `a88`의 representation 기반 shift residual
  - `a92`의 scenario baseline 관점
  - `shift + high cluster + unseen`을 함께 보는 `combo specialist`

## 지금까지의 큰 흐름

### 1. 기본 강한 앵커 만들기

- `a18`: EDA 기반 LightGBM
- `a48`: Transformer + LSTM + LGBM 앙상블
- `a56`, `a66`: STT + TransLF + a48 조합

### 2. residual stack 계열

- `a75`: residual CatBoost로 큰 점프
- `a76 ~ a78`: 앵커 기반 residual refinement
- `a79`, `a81`: sequence residual branch

### 3. layout-aware / sequence 확장

- `a82`: layout-aware residual expert
- `a83`: layout-aware sequence residual

### 4. representation / shift specialist 계열

- `a87`: TS2Vec 계열 representation branch
- `a88`: representation을 직접 제출용이 아니라 residual feature로 재사용
- `a89 ~ a91`: shift / unseen specialist 세분화 시도
- `a92`: EDA 기반 `scenario baseline + slot deviation + regime router`
- `a94`: `a88 + a92` 신호를 통합한 `combo specialist`로 최고 기록 갱신

## 현재 해석

- 단순 low-band 미세조정만으로는 한계가 분명함
- layout 전체보다 `shift regime` 정의가 더 중요함
- `representation-derived signal`은 전체 population보다 `shift / unseen / high cluster` 구간에서 더 잘 먹음
- 최근에는 “새 모델 하나 더”보다 “어디에 적용할지”가 더 중요했음

## 최근 실험 요약

- `a88_27`: `10.1201425252`
  - representation-as-feature shift expert
- `a94_51`: `10.1133848903`
  - `combo(shift + high + unseen)` specialist
  - 최근 가장 큰 개선
- `a95`, `a96`
  - `a94`를 더 세분화하거나 더 보수적으로 다듬는 실험
  - 아직 `a94_51`을 확실히 넘는 카드로 보이진 않음

## 다음 방향

- `a97`부터는 `a94 family`를 유지하되,
  - combo 정의를 더 안정적으로 만들지
  - 아니면 전혀 다른 signal source를 추가할지
  를 다시 판단하면서 갈 예정
- 현재 우선순위는 “작은 미세조정보다 구조적으로 먹힌 축을 더 안정적으로 재현하는 것”

## 저장소 구성

- [docs/project_overview.md](</C:/open/dacon-smart-warehouse-portfolio/docs/project_overview.md:1>)
  - 프로젝트 전체 흐름과 모델 방향 정리
- [docs/experiment_log.md](</C:/open/dacon-smart-warehouse-portfolio/docs/experiment_log.md:1>)
  - 점수 변화와 주요 실험 요약
- [docs/daily_logs](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_logs>)
  - 날짜별 작업 기록
- [docs/public_score_log.json](</C:/open/dacon-smart-warehouse-portfolio/docs/public_score_log.json:1>)
  - public 점수 이력

