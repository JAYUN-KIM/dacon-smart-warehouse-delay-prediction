# 일일 요약

- 생성 시각: `2026-04-21`
- 현재 최고 점수: `10.1064209775`
- 현재 최고 파일: `submission_a101_10.csv`

## 오늘 바뀐 점

- `a100`에서 처음으로 `baseline + scale + routed deviation` 구조를 실제 점수 개선으로 연결했습니다.
- `a100_05`가 `10.1090848449`를 기록하면서, 기존 `a94` family보다 더 근본적인 구조 변화가 먹히는 것을 확인했습니다.
- 이어서 `a101`에서는
  - robust baseline/scale
  - soft expected-error router
  - confidence fallback
  을 넣어 `10.1064209775`까지 추가 개선했습니다.

## 오늘의 핵심 해석

- 이제 메인 축은 `a94 family`가 아니라 `a100 family`입니다.
- `a94`는 여전히 강한 안전 앵커지만, 더 큰 개선은 decomposition + routing 구조에서 나오고 있습니다.
- 특히 `soft routing`이 `best single expert`와 `equal blend`를 모두 넘겼다는 점이 중요합니다.

## 현재 판단

앞으로의 주력 방향은 다음입니다.

1. baseline / scale 안정화
2. z expert 역할 분리
3. router에 support / shift feature 추가
4. confidence-aware fallback 유지

즉, 다음 단계는 “조금 더 좋은 모델 하나”가 아니라
“routing system을 더 안전하고 똑똑하게 만드는 것”입니다.
