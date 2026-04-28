# 실험 로그

## 현재 최고 기록

- 점수: `10.1005923422`
- 파일: `submission_a117_09.csv`
- 날짜: `2026-04-27`

## 주요 점수 흐름

- baseline: `11.83`
- `a48_v4_3`: `10.1477`
- `a56_3`: `10.1276`
- `a66_5`: `10.1260335184`
- `a75_01`: `10.122152212`
- `a76_01`: `10.121563682`
- `a77_01`: `10.1214405285`
- `a79_01`: `10.1214263184`
- `a81_01`: `10.121418246`
- `a83_01`: `10.1214032792`
- `a88_27`: `10.1201425252`
- `a94_51`: `10.1133848903`
- `a100_05`: `10.1090848449`
- `a101_10`: `10.1064209775`
- `a102_24`: `10.1360030381`
- `a104_15`: `10.1111502564`
- `a105_16`: `10.1104250846`
- `a105_13`: `10.1074718609`
- `a106_20`: `10.11045386`
- `a107_10`: `10.1067154934`
- `a108_12`: `10.1122539111`
- `a109_09`: `10.1085982977`
- `a110_09`: `10.106859334`
- `a114_09`: `10.103316418`
- `a115_146`: `10.1066275842`
- `a117_09`: `10.1005923422`
- `a117_18 계열`: `10.1014682069`
- `a118_01`: `10.1018318718`
- `a119_03`: `10.1010915332`

## 최근 실험 해석

### a94

- `representation residual`
- `scenario baseline signal`
- `shift + high + unseen combo specialist`

를 통합해서 큰 점프를 만든 실험입니다.

`a94_51`은 specialist 계열의 가장 강한 기준점이었습니다.

### a100

문제를 아래처럼 다시 분해했습니다.

- `baseline`
- `scale`
- `routed deviation`

그리고 `y = baseline + scale * routed_z` 구조를 도입해 `a100_05 = 10.1090848449`를 만들었습니다.

### a101

`a100` 위에

- soft expected-error router
- robust baseline / scale
- fallback

을 얹어 오랫동안 최고 기록이었던 `10.1064209775`를 만들었습니다.

### a102 ~ a106

이 구간은 모두 `a101` 위에 correction layer를 더 얹는 방향이었습니다.

공통된 결론:
- local OOF는 좋아 보이는 경우가 있었음
- public에서는 모두 실패

해석:
- backbone이 약해서가 아니라
- correction trigger / mask / magnitude calibration이 local OOF에 과적합됨

### a107

`a107`은 correction layer를 더 얹지 않고 `shift-heavy expert` 자체를 다시 학습한 실험이었습니다.

- `a101` direct router OOF: `7.4224`
- `a107` direct router OOF: `7.4162`
- public: `10.1067154934`

의미:
- correction layer 추가보다 expert 재학습이 더 건강한 방향임
- 다만 최고를 뒤집을 정도로 강하진 않음

### a108

`a108`은 pseudo-group 기반 shift-heavy expert 재학습 실험이었습니다.

중간에 중요한 문제를 확인했습니다.

- scenario hardness를 feature에 직접 넣었더니 비정상적으로 좋은 로컬 성능이 나옴
- leakage-like 착시로 판단
- hardness는 feature에서 제거하고 weighting에만 사용하도록 수정

수정 후:
- `a108` direct router OOF: `7.4219`
- public: `10.1122539111`

의미:
- pseudo-group 방향 자체는 가능성 있음
- 하지만 현재 구현은 아직 public 제출용 카드가 아님
- hardness를 direct feature로 쓰는 건 매우 위험함

### a109

`a109`는 pseudo-group를 더 늘리기보다 `shift_phys`, `shift_extreme` 같은 단순한 물리 expert와 `worst-group / testlike / baseline_hi` 중심 선택 기준으로 다시 정리한 실험이었습니다.

- public: `10.1085982977`

의미:
- `a108`보다 훨씬 안정적
- validation과 selection 방향은 맞았음
- 하지만 selection 기준만 바꾸는 것으로는 대형 점프가 어렵다는 점을 확인

### a110

`a110`은 문제를 창고 운영 관점에서 다시 해석한 실험입니다.

핵심 가설:
- 이 문제는 현재값만 맞추는 회귀가 아니라
- 같은 시나리오 안의 25슬롯 전체 맥락으로 가까운 미래 부하와 압력을 읽는 문제에 가깝다

추가한 핵심 피처:
- `lead1`, `fut2`, `fut3`
- `future_load_per_robot`
- `future_pressure_gap`
- `future_work_gap`
- `future_battery_gap`
- `future_instability`
- `future_stress_score`

결과:
- `a110` direct router OOF: `7.4081`
- best candidate OOF: `7.7730`
- public: `10.106859334`

의미:
- correction layer와는 다른 성격의 새로운 backbone 신호를 확인
- future-window 해석 자체는 실제로 유효함

### a111_v2

외부에서 받은 routed-z 파이프라인을 그대로 검토하고 실행했습니다.

결론:
- 구조는 정돈되어 있었음
- 하지만 raw feature 중심 standalone backbone이라 성능이 너무 약했음
- `a101/a110`을 대체할 수 있는 수준은 아니었고, 운영/구조 참고용에 가까웠음

### a112

질문: 미래창 피처를 300개 이상으로 늘리면 더 나아질까?

실험:
- 총 피처 수 `348`
- 미래창 관련 피처 `220`

결과:
- `direct_router_mae = 7.4448`
- best candidate OOF `7.7841`

의미:
- 미래창 해석이 틀린 건 아님
- 하지만 너무 많이 넣으면 신호가 희석되고 오히려 성능이 나빠짐

### a113

`a112`보다 작게 줄인 compact future row backbone 실험이었습니다.

결과:
- `direct_router_mae = 7.4633`
- best candidate OOF `7.7857`

의미:
- 단순히 개수를 줄이는 것만으로 해결되지 않음
- row expert 쪽에 future 신호를 과하게 넣는 방향 자체가 약할 수 있음

### a114

`a114`는 미래창 정보를 row expert 쪽으로 확장하는 대신, **scenario baseline/scale 강화용**으로 넣은 실험입니다.

결과:
- `direct_router_mae = 7.3957`
- best candidate OOF `7.7759`
- public: `10.103316418`

의미:
- 현재까지 future-window 계열 중 가장 성공적
- 미래창 신호는 “더 많이”보다 “어디에 넣느냐”가 중요하다는 점을 확인
- scenario-level stress 해석과 가장 궁합이 좋았음

### a115

`a115`는 `a114` backbone은 그대로 두고, 후보 생성과 fallback calibration만 정밀하게 다시 튜닝한 실험입니다.

결과:
- local best candidate OOF: `7.7112`
- public: `10.1066275842`

의미:
- 로컬 기준으론 좋아졌지만 public에서는 `a114`를 못 넘음
- 이 family 안에서 candidate generation만 더 미세하게 다듬는 방식은 한계가 있다는 신호

### a116

`a116`은 `a114` 이후 새 direct family를 찾기 위해, scenario-level feature를 펼친 뒤 25개 슬롯을 한 번에 예측하는 ridge seq2seq 계열을 시도한 실험입니다.

결과:
- feature count: `950`
- anchor OOF MAE: `7.7799119949`
- direct ridge OOF MAE: `7.9801287651`
- best ridge alpha: `500.0`

의미:
- direct ridge 자체는 앵커보다 약함
- 하지만 기존 앵커와 다른 방향의 예측 delta를 제공함
- 단독 제출 모델이 아니라, `a114/a117` 앵커를 보조하는 delta provider로 활용할 가치가 있음

### a117

`a117`은 `a116` direct ridge prediction을 그대로 섞지 않고, `a114` 앵커와의 차이를 clipping한 뒤 낮은 alpha로 반영한 실험입니다.

결과:
- `submission_a117_09.csv`
- 설정: `alpha=0.08`, `q98 clip`
- OOF MAE: `7.7673277855`
- public: `10.1005923422`

비교:
- 기존 최고 `a114_09 = 10.103316418`
- `a117_09`가 새 최고 기록 갱신
- 더 강한 계열은 `10.1014682069`로 `a117_09`를 넘지 못함

의미:
- ridge seq2seq direct family 전체를 믿으면 위험함
- 다만 앵커와의 delta를 제한적으로 반영하면 public 개선이 가능함
- 현재 핵심은 더 세게 보정하는 것이 아니라, public-safe clipped delta band를 찾는 것

### a118

`a118`은 `a117_09`에서 성공한 clipped delta 방향을 더 안전하게 다듬기 위한 비대칭 클리핑 후보 생성 실험입니다.

대표 후보:
- `submission_a118_01.csv`
- OOF MAE: `7.7275009155`
- test mean: `18.356560`
- test max: `44.054348`
- public: `10.1018318718`

의미:
- OOF 1등 후보는 평균과 최댓값이 올라가 public에서 흔들릴 위험이 있었음
- 따라서 `a117_09`의 평균/최댓값 대역에 가까운 후보를 우선 제출 후보로 선정
- 하지만 public에서는 `a117_09`를 넘지 못함
- 최댓값을 낮추고 비대칭 클리핑을 적용해도 public 개선으로 이어지지 않았음
- `a117_09`의 shape를 조금만 바꿔도 public이 민감하게 악화될 수 있음

### a119

`a119`는 `a118` 실패 이후, `a117_09`를 거의 그대로 유지하는 초근접 microgrid 후보 생성 실험입니다.

대표 후보:
- `submission_a119_03.csv`
- 방식: `q98 clip`을 `q98.5`로 아주 살짝 풀어준 후보
- OOF MAE: `7.760396`
- `a117_09` 대비 OOF 개선: 약 `0.00693`
- `a117_09` 대비 test 평균 변화량: 약 `0.00055`
- public: `10.1010915332`

의미:
- `a117_09`와 거의 같은 분포를 유지했지만 public 개선이 나오지 않음
- ridge delta 계열은 `a117_09` 근처에서 거의 포화된 것으로 판단
- 같은 family 안에서 alpha, clip quantile, tail tempering을 더 깎는 방식은 기대값이 낮음

## 현재 판단

1. `a100 family`와 `a114`의 future-window scenario 해석은 맞았다.
2. 현재 최고 public 앵커는 `a117_09`다.
3. `a116` ridge seq2seq direct model은 단독으로 약하지만 delta provider로 가치가 있다.
4. correction layer를 더 얹는 방향은 계속 우선순위를 낮춘다.
5. clipped ridge delta family는 `a117_09`에서 한 번 성공했지만 이후 `a118`, `a119`에서 포화 신호가 확인됐다.
6. 다음은 `a117_09`의 high-error scenario를 다시 분석해 ridge delta와 다른 독립 신호를 찾는 것이다.
