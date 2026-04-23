# 일일 리포트

- 생성 날짜: `2026-04-23`
- 현재 최고 public 점수: `10.1064209775`
- 현재 최고 파일: `submission_a101_10.csv`

## 오늘의 핵심 변화

- `a106_20`을 public에 제출했지만 `10.11045386`으로 더 나빠졌습니다.
- 이로써 `a101` 이후 correction layer 계열은 `a102`, `a104`, `a105`, `a106`까지 public에서 모두 최고 기록을 넘지 못했습니다.
- 방향을 바꿔 `a107`에서는 correction을 더 얹지 않고, `shift-heavy expert` 자체를 물리적 extreme 그룹 기준으로 다시 학습했습니다.

## 오늘 얻은 핵심 해석

1. `a100 family` 자체는 맞습니다.
2. 하지만 `a101` 이후 correction layer는 local OOF에 비해 public에서 반복적으로 흔들립니다.
3. 따라서 지금 병목은 새 family 부족보다, correction layer가 public에서 믿을 만큼 안정적이지 않다는 점입니다.
4. `a107`은 correction layer가 아니라 expert 재학습이라 더 건강한 실험이었고, 로컬 기준으로는 아주 미세한 개선이 있었습니다.
5. 다만 extreme group에서 `shift_jtt` expert가 `global`을 압도할 정도는 아니라서, 아직은 “방향은 맞지만 이득이 작다” 수준입니다.

## 현재 최고 기록 유지 여부

- 최고 public은 여전히 `submission_a101_10.csv = 10.1064209775`
- 오늘 실험들은 이 기록을 넘지 못했습니다.

## 내일 이어갈 방향

현재 기준으로 가장 논리적인 다음 단계는 아래 둘 중 하나입니다.

1. `a107` 계열을 기반으로 pseudo-group 정의와 expert 재학습을 더 정교하게 만드는 것
2. `a101`을 안전 앵커로 유지한 채, validation 기준을 worst-group / adversarial subset 중심으로 바꾸는 것

## 한 줄 요약

오늘 결론은 명확합니다.

**correction layer를 더 다듬는 것보다, 어려운 구간을 담당하는 expert 자체를 더 잘 학습시키는 쪽으로 넘어가야 합니다.**
