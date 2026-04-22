# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하면서 만든 실험 기록 저장소입니다.

이 저장소의 목적은 단순히 점수만 적는 것이 아니라,

- 지금 어떤 방향으로 실험하고 있는지
- 왜 그 방향으로 가고 있는지
- 어떤 시도가 실제로 먹혔는지
- 어떤 시도는 왜 실패했는지

를 날짜별로 남기는 것입니다.

## 현재 최고 기록

- 최고 public 점수: `10.1064209775`
- 제출 파일: `submission_a101_10.csv`
- 기준 날짜: `2026-04-21`

## 현재 핵심 판단

지금은 예전의 `a94 family`를 조금씩 다듬는 단계가 아니라,
`a100 family`를 메인 시스템으로 밀어붙이는 단계입니다.

현재 가장 중요한 구조는 다음과 같습니다.

1. `scenario baseline`
2. `scenario scale`
3. `standardized deviation`
4. `soft routing`
5. `fallback / correction control`

즉, 이제는 “평균적으로 잘 맞는 모델 하나”를 더 찾는 것보다,
“어떤 샘플에서 어떤 expert를 얼마나 믿을지”를 더 잘 결정하는 쪽이 중요합니다.

## 최근 흐름 요약

### 1. specialist 계열

- `a88`: representation 기반 shift expert
- `a94`: representation residual + scenario baseline + combo specialist

이 구간에서는 `shift/high/unseen` 같은 어려운 구간을 따로 보는 방식이 실제로 효과가 있었습니다.

### 2. decomposition + routing 계열

- `a100`: `baseline + scale + routed deviation` 구조를 처음 public 개선으로 연결
- `a101`: soft expected-error router + fallback으로 추가 개선

현재 최고 기록은 이 `a100 family`에서 나왔습니다.

### 3. 실패에서 얻은 정보

- `a102`: support-aware fallback을 너무 강하게 적용해서 크게 악화
- `a104`: `a101_10`을 앵커로 잡았지만 subset mask가 너무 날카로워 public에서 실패
- `a105`: continuous correction 자체는 의미 있었지만, 아직 public을 넘는 카드로 이어지지 못함

즉 지금의 병목은 “family가 틀린 것”보다
“correction을 어디에 얼마나 적용할지”가 아직 안정화되지 않았다는 쪽에 가깝습니다.

## 앞으로의 방향

현재 기준으로는 다음 방향이 가장 유망하다고 판단하고 있습니다.

1. `a100 family` 유지
2. `a101_10` 같은 강한 public 앵커 유지
3. hard subset mask 대신 continuous correction
4. support/testlike는 주연이 아니라 보조 feature로 사용
5. average OOF보다 worst-group 관점의 선택 기준 강화

한 줄로 정리하면,

**새 family로 갈아타는 것보다, a100 family를 더 부드럽고 안전하게 operationalize하는 것이 현재 메인 목표입니다.**

## 문서 구성

- [프로젝트 개요](</C:/open/dacon-smart-warehouse-portfolio/docs/project_overview.md>)
- [실험 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/experiment_log.md>)
- [일일 리포트](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_report.md>)
- [날짜별 작업 기록](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_logs>)
- [public 점수 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/public_score_log.json>)
