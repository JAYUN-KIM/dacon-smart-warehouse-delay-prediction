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

## 최근 실험 해석

### a94

- `representation residual`
- `scenario baseline signal`
- `shift + high + unseen combo specialist`

를 통합해서 큰 점프를 만들었습니다.

`a94_51`은 specialist 계열의 가장 강한 기준점이었습니다.

### a100

문제를 다음처럼 다시 분해했습니다.

- `baseline`
- `scale`
- `routed deviation`

그리고 `y = baseline + scale * routed_z` 구조로 direct correction을 만들었습니다.

`a100_05 = 10.1090848449`는 이 구조가 public에서도 먹힌다는 첫 증거였습니다.

### a101

`a100` 위에

- soft expected-error router
- robust baseline / scale
- fallback

을 얹어 `10.1064209775`까지 낮췄습니다.

현재 최고 기록은 이 `a101_10`입니다.

### a102

지원 거리(`support`)와 `testlike` 신호를 더 강하게 써봤지만,

- top-2 sparse routing
- support-aware fallback

이 너무 공격적으로 들어가면서 public이 `10.1360030381`까지 악화됐습니다.

결론:
- support/testlike는 유용한 정보일 수 있지만
- 그것을 “강한 스위치”처럼 쓰면 오히려 망가질 수 있습니다.

### a104

`a101_10`을 앵커로 두고,
확신 높은 subset에서만 `shift + repr hybrid`를 아주 조금 얹는 전략이었습니다.

로컬 OOF는 좋아 보였지만 public은 `10.1111502564`로 악화됐습니다.

결론:
- 문제는 앵커가 아니라
- subset 정의와 correction trigger가 너무 날카로웠던 것입니다.

### a105

`a101_10`을 앵커로 두고,
hard subset이 아니라 continuous correction으로 이동 강도만 조절하는 전략이었습니다.

아이디어는 맞았지만 public은 `10.1104250846`으로 아직 최고를 넘지 못했습니다.

결론:
- direction은 맞다
- 하지만 correction magnitude calibration이 아직 부족하다

## 현재 판단

지금 막힌 이유는 새 family가 없어서가 아니라,

- correction을 어디에 적용할지
- 얼마나 강하게 적용할지

를 정하는 메타 레이어가 아직 불안정하기 때문입니다.

그래서 현재 메인 방향은:

1. `a100 family` 유지
2. `a101_10`을 안전 앵커로 사용
3. hard mask보다 continuous correction
4. support/testlike는 보조 feature로만 활용
5. average OOF가 아니라 worst-group 관점 강화

즉, 지금 단계의 핵심은

**“더 좋은 모델 하나”보다 “더 안전하고 일관된 correction system”** 입니다.
