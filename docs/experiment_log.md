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
- `a105_13`: `10.1074718609`
- `a106_20`: `10.11045386`

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

그리고 `y = baseline + scale * routed_z` 구조로 direct correction 시스템을 만들었습니다.

`a100_05 = 10.1090848449`는 이 구조가 public에서도 먹힌 첫 증거였습니다.

### a101

`a100` 위에

- soft expected-error router
- robust baseline / scale
- fallback

을 넣어 `10.1064209775`까지 내려갔습니다.

현재 최고 기록은 `a101_10`입니다.

### a102

support-aware fallback을 강하게 적용했지만 public에서 `10.1360030381`로 크게 악화됐습니다.

해석:
- support/testlike 신호 자체는 가치가 있음
- 하지만 이를 강한 switch나 sparse fallback 기준으로 쓰면 public에서 쉽게 깨진다는 점을 확인했습니다

### a104

`a101_10`을 앵커로 두고, confidence가 높은 subset에만 hybrid correction을 얹는 방향이었습니다.

로컬 OOF는 좋아 보였지만 public은 `10.1111502564`로 악화됐습니다.

해석:
- 앵커가 약한 것이 아님
- subset 정의와 correction trigger가 local에 과적합된 것으로 보임

### a105

hard subset 대신 continuous correction으로 이동했습니다.

- `delta = routed - anchor`
- `alpha(x)`로 correction strength 조절

방향성은 괜찮았지만 public은 `10.1104250846`, 저강도 버전인 `a105_13`도 `10.1074718609`로 최고를 넘지 못했습니다.

해석:
- 방향 자체는 맞음
- 하지만 correction magnitude calibration이 아직 불안정

### a106

`a105`를 더 보수적으로 만든 safe continuous correction이었지만 public은 `10.11045386`로 더 나빠졌습니다.

해석:
- correction layer를 더 안전하게 줄인다고 해서 public이 바로 좋아지진 않음
- `a101` 이후 correction layer 계열이 반복적으로 public에서 실패한다는 신호가 더 강해짐

### a107

이번에는 correction layer를 더 쌓지 않고, `shift-heavy expert` 자체를 물리적 extreme 그룹 기준으로 다시 학습했습니다.

핵심:
- `a101` direct router OOF: `7.4224`
- `a107` direct router OOF: `7.4162`

즉 전체 라우터 기준으로는 아주 미세하게 개선됐습니다.

다만 extreme group 방어력은 `global` expert를 압도할 정도는 아니었습니다.

해석:
- correction layer 추가보다 expert 재학습이 더 건강한 방향
- 하지만 아직 이득 폭이 크진 않음

## 현재 판단

지금 막히는 이유는 새 family가 없어서가 아닙니다.

- 어떤 correction을 어디에 적용할지
- 얼마나 강하게 적용할지
- 어려운 샘플을 학습에서 어떻게 더 잘 반영할지

를 정하는 메타 설계가 아직 public 기준으로 충분히 안정적이지 않기 때문입니다.

그래서 현재 메인 방향은 아래와 같습니다.

1. `a100 family` 유지
2. `a101_10`을 강한 public 앵커로 유지
3. correction layer 추가보다 expert 재학습 쪽으로 이동
4. support/testlike는 보조 feature로만 사용
5. 평균 OOF보다 worst-group / adversarial subset 관점의 검증 강화
