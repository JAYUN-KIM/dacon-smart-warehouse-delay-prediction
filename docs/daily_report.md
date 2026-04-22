# 일일 요약

- 생성 시각: `2026-04-22`
- 현재 최고 점수: `10.1064209775`
- 현재 최고 파일: `submission_a101_10.csv`

## 오늘 바뀐 점

- `a102`는 support-aware fallback을 강하게 적용했지만 public에서 크게 악화되었습니다.
- `a104`는 `a101_10`을 앵커로 두고 subset correction을 시도했지만 public에서 실패했습니다.
- `a105`는 hard subset 대신 continuous correction으로 바꾸어 로컬 구조는 더 설득력 있게 만들었지만, 아직 public 최고 기록을 넘지는 못했습니다.

## 오늘의 핵심 해석

- 문제는 `a100 family` 자체가 틀린 것이 아닙니다.
- 실제로 public 최고점은 여전히 `a101_10`에서 나왔고, decomposition + routing 방향은 맞았습니다.
- 다만 이후 실험들은 correction을 적용하는 방식이 너무 날카롭거나, subset 정의가 local OOF에 과적합된 것이 문제였습니다.

## 오늘 얻은 결론

1. `a101_10` 같은 강한 public 앵커는 유지해야 한다.
2. hard mask / sparse switch / 공격적 fallback은 피하는 것이 좋다.
3. `support/testlike`는 주연이 아니라 보조 feature로 써야 한다.
4. 다음도 새 family를 찾기보다, `a100 family`를 더 부드럽고 안전하게 operationalize하는 방향이 맞다.

## 현재 판단

앞으로의 핵심은:

- `baseline / scale / deviation` 구조 유지
- `soft routing` 유지
- `continuous correction` 강화
- `worst-group` 관점으로 검증 강화

즉, 이제 중요한 것은

**“더 센 모델 하나”보다 “얼마나 안전하게 correction을 적용하느냐”** 입니다.
