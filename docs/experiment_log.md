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

## 구간별 해석

### a75 ~ a81

- 강한 앵커 위에 residual을 얹는 방식이 실제 public에서 꾸준히 먹혔습니다.
- 이 시기에는 “좋은 베이스 예측기 + residual correction”이라는 구조가 유효했습니다.

### a82 ~ a83

- layout-aware signal과 sequence signal을 더 강하게 넣어보는 구간이었습니다.
- 구조적 의미는 있었지만 큰 점프를 만들 정도는 아니었습니다.

### a88

- representation-derived signal을 전체가 아니라 shift subset에만 적용했습니다.
- 여기서 다시 public 개선이 확인되면서, “특정 regime에만 다른 신호를 쓰는 방식”이 중요하다는 점이 선명해졌습니다.

### a94

- `representation residual`
- `scenario baseline signal`
- `shift + high + unseen combo specialist`

를 통합해서 큰 점프를 만들었습니다.

`a94_51`은 현재까지 나온 specialist 계열 중 가장 강한 기준점이었습니다.

### a95 ~ a99

- `a94`의 세분화, 보수적 refinement, feature 흡수 실험이 이어졌습니다.
- 의미 있는 로컬 개선은 있었지만, `a94_51`을 압도하는 구조적 점프는 아니었습니다.

### a100 ~ a101

이 구간부터 문제를 다시 정의했습니다.

기존:
- raw target 또는 residual을 직접 맞추는 구조

변경:
- `y = baseline + scale * routed_z`

즉,

- scenario baseline
- scenario scale
- standardized deviation
- expert routing

으로 나누어 보는 새로운 family가 시작되었습니다.

이 방향이 실제로 다시 큰 개선을 만들었고,
현재 최고 기록도 이 family에서 나왔습니다.

## 현재 판단

지금은 `a94 family`를 조금 더 다듬는 단계가 아니라,

- `baseline / scale / deviation`
- `soft routing`
- `fallback`
- `support / shift feature`

를 더 안정화하는 `a100 family`가 메인입니다.
