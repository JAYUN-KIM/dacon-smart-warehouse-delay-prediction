# 실험 로그

## 현재 최고 기록

- 점수: `10.1064209775`
- 파일: `submission_a101_10.csv`
- 날짜: `2026-04-21`

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

## 최근 실험 해석

### a94

- `representation residual`
- `scenario baseline signal`
- `shift + high + unseen combo specialist`

를 통합해서 큰 점프를 만들었습니다.

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

을 얹어 현재 최고 기록 `10.1064209775`를 만들었습니다.

현재 최고 기록은 `a101_10`입니다.

### a102

support-aware fallback을 강하게 적용했지만 public에서 `10.1360030381`로 크게 악화됐습니다.

해석:
- support/testlike 신호는 가치가 있음
- 하지만 강한 switch/sparse fallback 기준으로 쓰면 public에서 쉽게 무너짐

### a104

`a101_10`을 앵커로 두고, confidence가 높은 subset에만 correction을 얹었지만 public에서 `10.1111502564`로 악화됐습니다.

해석:
- anchor가 약한 것이 아님
- subset 정의와 correction trigger가 local OOF에 과적합된 것으로 판단

### a105

hard subset 대신 continuous correction으로 전환했습니다.

- `delta = routed - anchor`
- `alpha(x)`로 correction strength 조절

방향은 맞아 보였지만 public은 `10.1104250846`, 저강도 버전 `a105_13`도 `10.1074718609`로 최고를 넘지 못했습니다.

해석:
- 방향은 맞음
- 하지만 correction magnitude calibration이 아직 불안정

### a106

`a105`를 더 보수적으로 만든 safe continuous correction이었지만 public은 `10.11045386`으로 더 나아지지 않았습니다.

해석:
- correction layer를 더 안전하게 줄이는 것만으로는 public이 바로 좋아지지 않음
- `a101` 이후 correction layer 계열은 반복적으로 public에서 실패 중

### a107

이번에는 correction layer를 더 얹지 않고, `shift-heavy expert` 자체를 물리 extreme 그룹 기준으로 다시 학습했습니다.

결과:
- `a101` direct router OOF: `7.4224`
- `a107` direct router OOF: `7.4162`
- public: `10.1067154934`

해석:
- correction layer 추가보다 expert 재학습이 더 건강한 방향
- public에서도 최고에 매우 근접했지만 아직 넘지는 못함

### a108

`a107`을 기반으로 pseudo-group 기반 shift-heavy expert를 다시 학습했습니다.

중간에 중요한 문제를 확인했습니다.

- scenario hardness를 직접 feature에 넣었을 때 비정상적으로 좋은 로컬 점수가 나옴
- leakage-like 착시로 판단
- hardness는 feature에서 제거하고, weighting에만 사용하도록 수정

수정 후:
- `a108` direct router OOF: `7.4219`
- public: `10.1122539111`

해석:
- pseudo-group 방향 자체는 가능성이 있음
- 하지만 현재 구현은 제출용 카드가 아니고 검증용 실험에 가까움
- hardness는 direct feature가 아니라 보조 signal로만 써야 안전함

## 현재 판단

지금 막힌 이유는 새 family가 부족해서라기보다,

- 어떤 correction을 어디에 적용할지
- 얼마나 강하게 적용할지
- 어떤 expert를 어떤 validation 기준으로 선택할지

를 정하는 메타 설계가 아직 public 기준으로 충분히 안정적이지 않기 때문입니다.

그래서 현재 메인 방향은 다음과 같습니다.

1. `a100 family` 유지
2. `a101_10`을 강한 public 앵커로 유지
3. correction layer 추가는 잠시 중단
4. `shift-heavy expert` 재학습 방향 유지
5. `worst-group / adversarial subset` 중심 validation 강화
