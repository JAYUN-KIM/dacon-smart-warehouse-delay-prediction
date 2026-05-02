# 프로젝트 개요

## 목표

데이콘 스마트 창고 출고 지연 예측 대회에서 향후 30분 평균 출고 지연 시간을 예측한다. 평가지표는 MAE이며, 현재 실험 목표는 public score 9점대 진입이다.

## 데이터 구조

- train: 10,000개 scenario, 각 scenario는 25개 slot
- test: 2,000개 scenario, 각 scenario는 25개 slot
- scenario는 독립 그룹으로 보며, 같은 scenario 안의 25개 slot context는 활용 가능하다.
- layout generalization과 운영 상태 분포 이동이 핵심 난제다.

## 현재 최고 성과

- 최고 제출: `submission_a138_147.csv`
- Public MAE: `10.0265043299`
- 달성일: `2026-05-02`

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
- a137에서 이전 제출 예측을 모델 입력으로 쓰지 않는 raw-only reboot ensemble이 public `10.02829`를 기록하며 가장 큰 점프를 만들었다.
- a138에서 a137 성공 분포를 유지한 fine grid 후보가 `10.0265043299`로 현재 최고점을 갱신했다.
- OOF가 좋아도 test prediction 평균이 비정상적으로 무너지는 모델은 제출 후보에서 제외해야 한다.

## 최근 방향 전환

초반에는 모델 구조와 MoE routing 중심으로 접근했다. 이후 public score가 10.10 부근에서 막히면서 원점 EDA와 미래 예측 관점으로 다시 돌아갔다. 그 결과, 후반 slot과 high-pressure/high-stress 구간에서 과소예측되는 축을 발견했고, 이를 평균 보존형 uplift로 다루는 방향이 새 최고점으로 이어졌다.

2026-04-30에는 이 방향을 더 밀어 `a125`, `a126`, `a127`에서 연속 개선을 확인했다. 2026-05-01에는 같은 축의 포화 신호를 확인한 뒤, from-scratch direct model signal을 아주 낮은 비율로 흡수하는 방식으로 `a131_101` 새 최고점을 달성했다. 2026-05-02에는 기존 anchor 미세 조정 대신 raw train/test/layout_info 기반의 raw-only reboot pipeline을 만들었고, ranker/domain/future-window feature를 결합한 `a137`, `a138` 계열이 큰 public 개선을 만들었다.

## 다음 계획

다음 실험은 `a139`부터 시작한다.

- raw-only reboot pipeline을 유지한다.
- ranker model diversity를 늘려 a136 domain reboot와의 error correlation을 낮춘다.
- scenario-level queue/load/capacity feature를 확장한다.
- high-delay tail 전용 specialist를 추가하되 hard switch는 사용하지 않는다.
- `a138_147`의 public-hit prediction distribution에서 크게 벗어나는 후보는 제출 후보에서 제외한다.
- 목표는 10.0265에서 10.00대를 거쳐 9점대에 진입하는 것이다.
