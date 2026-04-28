# 프로젝트 개요

## 목표

데이콘 스마트 창고 출고 지연 예측 대회에서 향후 30분 평균 출고 지연 시간을 예측한다. 평가지표는 MAE이며, 현재 실험 목표는 public score 9점대 진입이다.

## 데이터 구조

- train: 10,000개 scenario, 각 scenario는 25개 slot
- test: 2,000개 scenario, 각 scenario는 25개 slot
- scenario는 독립 그룹으로 보며, 같은 scenario 안의 25개 slot context는 활용 가능하다.
- layout generalization과 운영 상태 분포 이동이 핵심 난제다.

## 현재 최고 성과

- 최고 제출: `submission_a124_1443.csv`
- Public MAE: `10.0960054075`
- 달성일: `2026-04-29`

## 핵심적으로 배운 점

- scenario baseline 신호가 매우 중요하며, raw target을 직접 맞추는 것만으로는 한계가 있었다.
- `baseline + scale + routed_z` 구조는 a100/a101 계열에서 유효성을 보였다.
- support/testlike 신호는 hard switch로 쓰면 위험하고, 보조 feature 또는 부드러운 routing 신호로만 다뤄야 한다.
- aggressive correction layer, hard subset mask, direct DANN 계열은 public에서 안정적으로 먹히지 않았다.
- a114 이후로는 미래창/pressure/late-slot 관점이 점수 개선에 더 직접적으로 반응했다.
- a122/a124 결과상 late/high-stress underprediction을 완만하게 보정하는 방향이 현재 가장 유효하다.

## 최근 방향 전환

초반에는 모델 구조와 MoE routing 중심으로 접근했다. 이후 public score가 10.10 부근에서 막히면서 원점 EDA와 미래 예측 관점으로 다시 돌아갔다. 그 결과, 후반 slot과 high-pressure/high-stress 구간에서 과소예측되는 축을 발견했고, 이를 평균 보존형 uplift로 다루는 방향이 새 최고점으로 이어졌다.

## 다음 계획

2026-04-30에는 `a125`부터 시작한다.

- `a124_1443`을 anchor로 유지한다.
- late-shift uplift의 시작 slot, coverage quantile, uplift 평균, 최대 보정 폭을 좁은 범위에서 정밀 탐색한다.
- 제출 후보는 public-safe 후보와 aggressive 후보로 나누어 관리한다.
- 목표는 10.096대에서 10.09 초반, 이후 10.00대와 9점대 진입을 노리는 것이다.
