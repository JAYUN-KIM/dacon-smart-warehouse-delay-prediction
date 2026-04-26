# 실험 로그

## 현재 최고 기록

- 점수: `10.103316418`
- 파일: `submission_a114_09.csv`
- 날짜: `2026-04-26`

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

## 현재 판단

1. `a100 family`는 맞았다.
2. `a114_09`는 현재 가장 강한 public 앵커다.
3. correction layer를 더 얹는 방향은 계속 우선순위를 낮춘다.
4. 미래창 해석은 유지하되, scenario-level stress 해석에 집중한다.
5. `a115`까지의 결과를 보면 이제 같은 family 안에서 calibration만 더 만지는 것으로는 9점대 진입이 어렵다.
6. 다음은 지금까지 얻은 해석을 살린 **새 direct family** 설계가 더 중요하다.
