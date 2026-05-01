# 프로젝트 개요

## 목표

데이콘 스마트 창고 출고 지연 예측 대회에서 향후 30분 평균 출고 지연 시간을 예측한다. 평가지표는 MAE이며, 현재 실험 목표는 public score 9점대 진입이다.

## 데이터 구조

- train: 10,000개 scenario, 각 scenario는 25개 slot
- test: 2,000개 scenario, 각 scenario는 25개 slot
- scenario는 독립 그룹으로 보며, 같은 scenario 안의 25개 slot context는 활용 가능하다.
- layout generalization과 운영 상태 분포 이동이 핵심 난제다.

## 현재 최고 성과

- 최고 제출: `submission_a131_101.csv`
- Public MAE: `10.0920140626`
- 달성일: `2026-05-01`

## 핵심적으로 배운 점

- scenario baseline 신호가 매우 중요하며, raw target을 직접 맞추는 것만으로는 한계가 있었다.
- `baseline + scale + routed_z` 구조는 a100/a101 계열에서 유효성을 보였다.
- support/testlike 신호는 hard switch로 쓰면 위험하고, 보조 feature 또는 부드러운 routing 신호로만 다뤄야 한다.
- aggressive correction layer, hard subset mask, direct DANN 계열은 public에서 안정적으로 먹히지 않았다.
- a114 이후로는 미래창/pressure/late-slot 관점이 점수 개선에 더 직접적으로 반응했다.
- a122 이후 late/high-stress underprediction을 완만하게 보정하는 방향이 가장 꾸준하게 public 개선을 만들었다.
- a125부터 a127까지는 같은 coverage 안에서 평균 uplift와 late profile을 강화하는 방식이 연속으로 먹혔다.
- a130에서 scenario offset pivot이 public 악화를 만들며, 단순 보정 강화의 포화 신호를 확인했다.
- a131에서 raw data 기반 direct LGBM family를 새로 만들고, 이를 낮은 비율로 anchor에 흡수하자 새 최고점이 나왔다.
- OOF가 좋아도 test prediction 평균이 비정상적으로 무너지는 모델은 제출 후보에서 제외해야 한다.

## 최근 방향 전환

초반에는 모델 구조와 MoE routing 중심으로 접근했다. 이후 public score가 10.10 부근에서 막히면서 원점 EDA와 미래 예측 관점으로 다시 돌아갔다. 그 결과, 후반 slot과 high-pressure/high-stress 구간에서 과소예측되는 축을 발견했고, 이를 평균 보존형 uplift로 다루는 방향이 새 최고점으로 이어졌다.

2026-04-30에는 이 방향을 더 밀어 `a125`, `a126`, `a127`에서 연속 개선을 확인했다. 2026-05-01에는 같은 축의 포화 신호를 확인한 뒤, from-scratch direct model signal을 아주 낮은 비율로 흡수하는 방식으로 `a131_101` 새 최고점을 달성했다.

## 다음 계획

다음 실험은 `a132`부터 시작한다.

- `a131_101`을 anchor로 유지한다.
- row direct LGBM signal의 alpha를 `0.010~0.035` 범위에서 세밀하게 조절한다.
- late/high-stress mask와 direct signal이 같은 방향인 구간만 선택적으로 보정한다.
- slot-direct처럼 OOF 대비 test 분포가 무너지는 후보는 제외한다.
- 목표는 10.092대에서 10.08대, 이후 10.00대와 9점대 진입을 노리는 것이다.
