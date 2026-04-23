# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하면서 만든 실험 기록 저장소입니다.

이 저장소의 목적은 단순히 점수만 남기는 것이 아니라, 아래 내용을 날짜별로 정리하는 데 있습니다.

- 지금 어떤 방향으로 실험하고 있는지
- 왜 그 방향을 선택했는지
- 어떤 시도가 실제로 public 점수를 개선했는지
- 어떤 시도가 로컬에서는 좋아 보였지만 public에서는 실패했는지

## 현재 최고 기록

- 최고 public 점수: `10.1064209775`
- 제출 파일: `submission_a101_10.csv`
- 기록 날짜: `2026-04-21`

## 현재 핵심 판단

지금 단계에서 메인 방향은 `a94 family`의 단순 미세조정이 아니라 `a100 family`입니다.

현재 가장 중요한 구조는 아래와 같습니다.

1. `scenario baseline`
2. `scenario scale`
3. `standardized deviation`
4. `soft routing`
5. `safe correction / fallback control`

즉 이제는 평균적으로 잘 맞는 단일 모델을 더 찾는 것보다, 어떤 샘플에서 어떤 expert를 얼마나 믿을지 안정적으로 결정하는 시스템이 더 중요합니다.

## 최근 흐름 요약

### 1. specialist 계열

- `a88`: representation 기반 shift expert
- `a94`: representation residual + scenario baseline + shift/high/unseen combo specialist

이 구간에서는 `shift/high/unseen` 같은 어려운 구간을 low-band보다 더 직접적으로 다루는 방향이 실제로 효과가 있었습니다.

### 2. decomposition + routing 계열

- `a100`: `baseline + scale + routed deviation` 구조를 처음 public 개선으로 연결
- `a101`: soft expected-error router + fallback으로 현재 최고 기록 달성

현재 최고 public은 `a101_10`에서 나왔고, 이 때문에 지금의 메인 family는 사실상 `a100 family`라고 보고 있습니다.

### 3. a101 이후 실패에서 얻은 교훈

- `a102`: support-aware fallback을 너무 강하게 적용해서 크게 악화
- `a104`: `a101_10`을 앵커로 썼지만 subset mask가 너무 날카로워서 public 실패
- `a105`, `a106`: continuous correction 방향은 맞았지만 correction magnitude calibration이 불안정

즉 최근 병목은 새 family가 부족한 것이 아니라, `a101` 이후 correction을 어디에 얼마나 적용할지 정하는 메타 설계가 불안정한 쪽에 가깝습니다.

### 4. a107에서 얻은 새 정보

- `a107`은 correction layer를 더 쌓지 않고, `shift-heavy expert` 자체를 물리적 extreme 그룹 기준으로 다시 학습한 실험입니다.
- 로컬 기준으로 `direct router`는 `a101`보다 아주 미세하게 좋아졌습니다.
- 하지만 extreme group 방어력은 `global` expert를 압도할 정도는 아니어서, “방향은 맞지만 이득이 아직 작다”는 결론을 얻었습니다.
- 즉 다음 단계는 correction layer를 더 다듬기보다, expert 재학습과 validation 설계를 더 정교하게 가져가는 쪽이 맞습니다.

## 앞으로의 방향

현재 기준으로 다음 방향은 아래처럼 잡고 있습니다.

1. `a100 family` 유지
2. `a101_10` 같은 강한 public 앵커 유지
3. hard subset mask와 aggressive fallback은 지양
4. support/testlike는 주연 신호가 아니라 보조 feature로만 사용
5. correction layer 추가보다 `shift-heavy expert` 재학습과 `worst-group` 검증 강화 쪽으로 이동

한 줄로 정리하면,

**새 family로 갈아타는 단계라기보다, a100 family를 더 안전하고 견고하게 운영 가능한 시스템으로 바꾸는 단계입니다.**

## 문서 구성

- [프로젝트 개요](</C:/open/dacon-smart-warehouse-portfolio/docs/project_overview.md>)
- [실험 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/experiment_log.md>)
- [일일 리포트](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_report.md>)
- [날짜별 작업 기록](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_logs>)
- [public 점수 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/public_score_log.json>)
