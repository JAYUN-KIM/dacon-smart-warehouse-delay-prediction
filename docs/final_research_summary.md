# 최종 연구 요약

## 대회 개요

데이콘 스마트 창고 출고 지연 예측 대회는 각 scenario의 25개 slot 정보를 바탕으로 향후 30분 평균 출고 지연 시간(`avg_delay_minutes_next_30m`)을 예측하는 MAE 회귀 문제입니다.

데이터는 다음 구조를 가집니다.

- train: 10,000개 scenario x 25개 slot
- test: 2,000개 scenario x 25개 slot
- scenario는 독립 그룹
- 같은 scenario 안의 25개 slot context는 활용 가능
- layout generalization과 운영 상태 분포 이동이 핵심 난제

최종 public 점수는 `10.0038814352`이며, 최종 제출 파일은 `submission_a156_046.csv`입니다.

## 전체 연구 흐름

### 1. 초기 ensemble과 residual 보정

초기에는 CatBoost, LightGBM, sequence model, residual ensemble을 중심으로 접근했습니다. low-band residual 보정으로 public `10.12`대까지 진입했지만, 단순 앙상블과 residual stacking만으로는 개선 폭이 작았습니다.

이 단계에서 얻은 결론은 다음과 같습니다.

- scenario baseline 신호가 매우 큽니다.
- row 단위 residual만 고도화하면 전체 MAE 개선 폭이 제한됩니다.
- 평균 CV가 좋아도 public에서 바로 개선되지 않는 경우가 많습니다.

### 2. baseline + scale + routed_z decomposition

`a100/a101` 계열에서는 target을 다음처럼 분해했습니다.

`y = baseline + scale * routed_z`

핵심 구성은 다음과 같습니다.

- scenario baseline head
- robust scale head
- standardized deviation expert
- expected-error 기반 soft router

이 구조는 public `10.1064209775`까지 도달하며 유효성을 보였습니다. 그러나 이후 correction layer를 계속 얹는 방식은 local OOF 과적합이 강했고, public에서는 흔들렸습니다.

### 3. OOD와 routing 실패 분석

DANN, hard support-aware routing, aggressive correction, pseudo-group shift-heavy expert 등을 시도했습니다.

실패에서 얻은 판단은 다음과 같습니다.

- 도메인 차이를 지우는 방식은 운영 상태 안의 예측 신호까지 지울 수 있습니다.
- support/testlike score는 hard switch가 아니라 보조 feature로 써야 합니다.
- hard routing이나 hard fallback은 경계 샘플에서 public 악화를 만들 수 있습니다.
- correction layer는 validation residual의 noise까지 학습할 위험이 큽니다.

### 4. 미래창/창고 압력 feature 확장

중반 이후에는 대회 문제를 “창고 운영 압력의 미래 전개를 예측하는 문제”로 다시 해석했습니다.

추가한 feature 방향은 다음과 같습니다.

- future-window statistics
- order inflow, robot active, unique SKU, pressure/utilization 계열 통계
- scenario aggregate
- slot rank/profile
- path congestion, tech friction, queue shock
- layout capacity 관련 proxy

이 방향은 public에서 꾸준히 반응했고, `a114`, `a122`, `a127`까지 점진적 개선을 만들었습니다.

### 5. raw-only reboot

2026-05-02에는 기존 제출 예측을 모델 입력으로 쓰는 방식에서 벗어나 raw train/test/layout 기반 pipeline을 새로 만들었습니다.

이 raw-only reboot는 가장 큰 점프 중 하나였습니다.

- `submission_a137_011.csv`: public `10.02829`
- `submission_a138_147.csv`: public `10.0265043299`

이 단계에서 얻은 결론은 다음과 같습니다.

- 기존 anchor 미세조정이 포화됐을 때는 raw feature 기반 family를 새로 만드는 것이 효과적입니다.
- 하지만 raw-only model 단독보다는 public-hit prediction distribution과 결합할 때 더 안정적입니다.

### 6. future-pressure slot redistribution

2026-05-03의 핵심 breakthrough는 scenario 평균을 크게 흔들지 않고, 같은 scenario 안 25개 slot 사이에서 예측 질량을 재분배하는 것이었습니다.

창고 지연은 특정 slot에서 미래 압력, 작업 병목, 로봇/패킹 부하가 몰리며 발생할 수 있습니다. 따라서 단순히 scenario 평균을 올리는 것보다, 미래 압력 profile이 높은 slot으로 예측값을 이동하는 것이 public에 더 잘 맞았습니다.

주요 결과는 다음과 같습니다.

- `submission_a145_1755.csv`: public `10.0143960347`
- `submission_a145_4830.csv`: public `10.010757563`

### 7. queueing/domain reallocation

최종 구간에서는 외부 데이터를 직접 사용하지는 않았지만, 외부 warehouse/queueing 아이디어를 참고해 도메인 feature를 설계했습니다.

반영한 관점은 다음과 같습니다.

- utilization/capacity gap
- Kingman/VUT waiting-time proxy
- fork-join bottleneck
- path friction
- tech friction
- future queue shock

이 구조는 `submission_a151_886.csv`에서 public `10.0068002221`까지 개선을 만들었습니다.

### 8. final phase-lead

마지막에는 다시 문제 정의로 돌아갔습니다. target은 현재 지연이 아니라 향후 30분 평균 지연입니다. 따라서 현재 slot 예측에는 앞으로 1~2 slot의 예측 및 운영 압력 신호가 반영되어야 합니다.

`a154`에서는 future phase-lead를 적용해 OOF를 크게 줄였습니다. 다만 p99/max tail이 낮아져 public에서는 힘이 부족할 가능성이 있었습니다.

이를 보완하기 위해 `a155`에서는 phase-lead와 public-tail calibration을 결합했습니다.

- `submission_a155_481.csv`: public `10.0046018208`

마지막 `a156`은 `a155_481`을 기준으로 p99/max만 한 단계 더 밀었습니다.

- `submission_a156_046.csv`: public `10.0038814352`

## 최종 public 점수 흐름

| 날짜 | 제출 | public MAE | 핵심 |
| --- | --- | ---: | --- |
| 2026-04-18 | baseline | `11.83` | 초기 기준 |
| 2026-04-22 | `submission_a101_10.csv` | `10.1064209775` | decomposition + soft router |
| 2026-04-28 | `submission_a122_1045.csv` | `10.0967991272` | late/high-pressure uplift |
| 2026-05-02 | `submission_a138_147.csv` | `10.0265043299` | raw-only reboot |
| 2026-05-03 | `submission_a145_4830.csv` | `10.010757563` | slot redistribution |
| 2026-05-04 | `submission_a149_009.csv` | `10.0073867868` | public-guided extrapolation |
| 2026-05-04 | `submission_a151_886.csv` | `10.0068002221` | queueing/domain reallocation |
| 2026-05-04 | `submission_a155_481.csv` | `10.0046018208` | future phase-lead |
| 2026-05-04 | `submission_a156_046.csv` | `10.0038814352` | 최종 tail gamble |

## 가장 중요했던 판단

1. 모델 capacity보다 문제 정의와 예측 분포 설계가 중요했습니다.
2. scenario 평균을 직접 크게 흔드는 것보다 scenario 내부 slot redistribution이 더 강했습니다.
3. public은 p99/max tail shape에 매우 민감했습니다.
4. OOF가 좋아도 prediction distribution이 public-hit 후보와 크게 다르면 위험했습니다.
5. 마지막 개선은 `next_30m`라는 미래 예측 정의를 다시 반영했을 때 나왔습니다.

## 아쉬운 점

목표였던 9점대에는 도달하지 못했습니다. 최종 점수 `10.0038814352`는 9점대에 매우 근접했지만, 마지막 한 번의 public-tail gamble도 10.00 벽을 완전히 깨지는 못했습니다.

그럼에도 이번 기록은 단순한 점수 추적이 아니라, 실패한 접근과 성공한 접근을 함께 남긴 실험 이력입니다. 특히 OOD generalization, MoE routing, feature engineering, public feedback 기반 후보 선택, 예측 분포 calibration을 실제 대회 흐름 속에서 검증했다는 점이 포트폴리오로 의미 있습니다.
