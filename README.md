# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하면서, 실험 흐름과 판단 근거를 한국어로 정리해두는 저장소입니다.

이 저장소의 목적은 단순히 점수만 적는 것이 아니라 아래 내용을 날짜별로 남기는 것입니다.

- 지금 어떤 방향으로 실험하고 있는지
- 왜 그 방향을 선택했는지
- 어떤 실험이 실제 public 점수 개선으로 이어졌는지
- 어떤 실험이 로컬 OOF에서는 좋아 보여도 public에서 실패했는지

## 현재 최고 기록

- 최고 public 점수: `10.1005923422`
- 제출 파일: `submission_a117_09.csv`
- 기록 날짜: `2026-04-27`

## 현재 핵심 판단

지금 메인 방향은 더 이상 `a94 family` 미세조정이 아니라, `a100/a101`에서 만든 decomposition + routing 자산 위에 `future-window` 해석과 `ridge seq2seq delta`를 얼마나 안전하게 흡수하느냐입니다.

현재 가장 중요한 구조는 아래와 같습니다.

1. `scenario baseline`
2. `scenario scale`
3. `standardized deviation`
4. `soft routing`
5. `future-window 기반 scenario-level stress 해석`
6. `clipped ridge seq2seq delta`

즉 지금은 “correction layer를 더 세게 얹는 문제”보다, **public에서 검증된 앵커를 보존하면서 새로운 seq2seq 계열의 방향성만 얇고 안전하게 반영하는 문제**가 핵심입니다.

## 최근 실험 요약

### 1. specialist 계열

- `a88`: representation 기반 shift expert
- `a94`: representation residual + scenario baseline + shift/high/unseen combo specialist

이 구간에서는 `shift/high/unseen` 같은 어려운 구간을 따로 보는 specialist 방향이 실제로 잘 먹혔습니다.

### 2. decomposition + routing 계열

- `a100`: `baseline + scale + routed deviation`
- `a101`: soft expected-error router + fallback

이 구조가 오랫동안 최고 기록이었던 `a101_10 = 10.1064209775`를 만들었습니다.

### 3. a101 이후 correction layer 실패

`a102`, `a104`, `a105`, `a106`은 모두 `a101` 위에 correction을 더 얹는 방향이었습니다.

공통점:
- 로컬 OOF는 좋아 보이는 경우가 있었음
- public에서는 전부 `a101_10`을 넘지 못함

해석:
- `a100 family`가 틀린 것이 아니라
- correction layer가 local OOF에 과적합되고 있다고 판단 중

### 4. expert 재학습과 pseudo-group 실험

- `a107`: correction layer 없이 `shift-heavy expert` 자체 재학습
- `a108`: pseudo-group 기반 shift expert
- `a109`: `worst-group / testlike / baseline_hi` 중심 selection

얻은 교훈:
- correction layer 추가보다 expert 재학습이 더 건강한 방향이었음
- 하지만 pseudo-group를 복잡하게 만들수록 public winner와는 멀어졌음
- validation과 selection만 바꾸는 것으로는 대형 점프가 어렵다는 점을 확인

### 5. future-window 계열 연구

- `a110`: 미래 부하/압력/배터리 요약 피처를 backbone에 처음 반영
- `a111_v2`: 외부에서 받은 raw-only routed-z 파이프라인 검토
- `a112`: 미래창 피처를 300개 이상으로 크게 확장
- `a113`: compact future row backbone
- `a114`: 미래창 정보를 `scenario baseline/scale` 쪽에 집중 반영
- `a115`: `a114` backbone 유지 + candidate generation 정밀화

핵심 교훈:
- 미래창 해석 자체는 실제 신호가 맞음
- 하지만 row expert 쪽으로 미래창 피처를 과하게 늘리면 성능이 오히려 나빠짐
- 가장 잘 먹힌 건 `a114`처럼 미래 부하·압력 요약을 **scenario baseline/scale 강화용**으로 넣는 방식이었음
- `a115`는 로컬 OOF는 좋아졌지만 public에서는 `a114`를 넘지 못해, 이제는 이 family도 후보 생성 미세조정만으로는 한계가 있다는 신호를 줌

### 6. ridge seq2seq delta 계열

- `a116`: 25개 슬롯을 한 번에 예측하는 ridge seq2seq direct family 실험
- `a117`: direct ridge 자체는 약하지만, `a114` 앵커와의 delta를 얇게 clipped blend하면 public 개선이 나온다는 점 확인
- `a118`: 내일 제출 후보로, `a117_09`의 안전한 평균/최댓값 대역을 유지하면서 delta를 비대칭 클리핑하는 후보 생성

핵심 교훈:
- direct ridge 모델 단독은 약하지만, 기존 앵커와 다른 방향의 오차 정보를 갖고 있음
- 이 delta를 강하게 반영하면 public에서 흔들림
- `a117_09`처럼 `q98 clip + alpha 0.08` 수준의 얇은 반영은 실제 최고 public `10.1005923422`를 만들었음
- 다음은 correction을 키우는 게 아니라, `a117_09`의 안전한 형태를 유지하면서 delta shape만 조절하는 방향이 맞음

## 현재 방향

지금 기준으로 다음 방향은 아래처럼 정리하고 있습니다.

1. `a117_09`를 현재 최고 public 앵커로 유지
2. correction layer 추가는 계속 보류
3. `future-window` 신호와 `a114`의 scenario baseline/scale 해석은 유지
4. `a116` ridge seq2seq direct prediction은 단독 모델이 아니라 delta provider로만 사용
5. delta는 반드시 clipping, 낮은 alpha, 평균/최댓값 guard를 함께 적용
6. `support/testlike`는 보조 feature로만 사용
7. 내일은 `submission_a118_01.csv` public 점수부터 확인한 뒤, 10.00대 진입 가능성이 있는 clipping/alpha 구간을 더 좁힐 예정

즉 지금은 새 correction layer를 더 얹는 단계가 아니라, **public에서 실제로 먹힌 clipped delta 방향을 얼마나 안정적으로 다듬을지 결정하는 단계**입니다.

## 문서 구성

- [프로젝트 개요](docs/project_overview.md)
- [실험 로그](docs/experiment_log.md)
- [일일 리포트](docs/daily_report.md)
- [날짜별 작업 기록](docs/daily_logs/)
- [public 점수 로그](docs/public_score_log.json)
