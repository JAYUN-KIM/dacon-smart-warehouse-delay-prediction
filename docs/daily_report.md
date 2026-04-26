# 일일 리포트

- 생성 날짜: `2026-04-26`
- 현재 최고 public 점수: `10.103316418`
- 현재 최고 파일: `submission_a114_09.csv`

## 오늘의 핵심 변화

- `a111_v2` 외부 파이프라인을 실제로 돌려봤고, 구조 참고용으로는 괜찮지만 경쟁 backbone으로는 약하다는 결론을 냈습니다.
- `a112`에서 미래창 피처를 300개 이상으로 크게 늘렸지만 성능이 오히려 악화됐습니다.
- `a113`에서는 미래창 피처를 줄였지만 row backbone 중심 확장으로는 개선이 없었습니다.
- `a114`에서 미래창 정보를 scenario baseline/scale 쪽에 집중 반영했고, 이 방향이 실제 최고 public `10.103316418`을 만들었습니다.
- `a115`에서는 `a114` backbone을 유지한 채 candidate generation만 더 정밀하게 튜닝했지만, public은 `10.1066275842`로 `a114`를 넘지 못했습니다.

## 오늘 얻은 해석

1. 미래창 해석 자체는 맞습니다.
2. 하지만 미래창 피처를 많이 늘릴수록 좋아지는 것은 아니고, row expert 쪽 과확장은 오히려 독이 됩니다.
3. 가장 잘 먹힌 건 미래 부하/압력 정보를 scenario baseline/scale 강화용으로 넣는 방식이었습니다.
4. `a115`가 local OOF는 더 좋아도 public에서는 못 넘은 걸 보면, 이제 같은 family 안에서 후보 생성/보정만 더 다듬는 방식은 한계가 있습니다.
5. 따라서 다음은 `a114`가 왜 먹혔는지를 유지한 채, 새 direct family로 넘어가는 것이 더 빠를 수 있습니다.

## 현재 최고 기록 유지 여부

- 최고 public은 이제 `submission_a114_09.csv = 10.103316418`
- `a115`는 local 개선에도 불구하고 이 기록을 넘지 못했습니다.

## 다음 방향

현재 기준으로 가장 합리적인 다음 방향은 아래와 같습니다.

1. `a114_09`를 메인 앵커로 유지
2. correction layer 추가는 계속 보류
3. `future-window` 해석은 유지하되, scenario-level stress 해석에 집중
4. row feature를 더 많이 늘리기보다 backbone 목표와 구조를 새로 설계
5. average OOF보다 `worst-group / adversarial subset / unseen-like / future-stress` 기준 validation을 강화
6. 다음은 같은 family의 미세조정보다, 지금까지 얻은 해석을 살린 `a116`급 새 direct family를 설계

## 한 줄 요약

오늘은 미래창 피처를 무작정 늘리는 건 답이 아니라는 점을 확인했고, `a114`처럼 scenario baseline/scale에 정확하게 넣었을 때만 실제 public 개선이 나온다는 걸 확인했습니다. 동시에 `a115`로 같은 family 안 미세조정의 한계도 확인했기 때문에, 다음은 새 backbone 설계 쪽으로 가는 게 맞습니다.
