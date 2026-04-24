# 일일 리포트

- 생성 날짜: `2026-04-24`
- 현재 최고 public 점수: `10.1064209775`
- 현재 최고 파일: `submission_a101_10.csv`

## 오늘의 핵심 변화

- `a107_10`을 public에 제출했고 결과는 `10.1067154934`였습니다.
- `a108`은 pseudo-group 기반 `shift-heavy expert` 재학습 실험으로 구현과 검증까지 진행했습니다.
- `a108` 구현 중 scenario hardness를 direct feature에 넣었을 때 비정상적으로 좋은 로컬 성능이 나와, leakage-like 착시로 판단하고 즉시 수정했습니다.
- hardness를 feature에서 제거하고 weighting에만 사용한 뒤 다시 검증했고, 최종 public 결과는 `10.1122539111`이었습니다.

## 오늘 얻은 해석

1. `a100 family` 자체는 여전히 맞습니다.
2. `a101_10`은 아직도 가장 강한 public 앵커입니다.
3. `a101` 이후 correction layer 계열은 public에서 반복적으로 실패했고, 현재는 우선순위를 낮추는 것이 맞습니다.
4. `a107`은 correction layer 추가보다 expert 재학습이 더 건강한 방향이라는 점을 보여줬습니다.
5. `a108`은 pseudo-group 방향이 완전히 틀린 것은 아니라는 점을 보여줬지만, 아직 제출용 카드는 아닙니다.
6. 특히 hardness를 feature로 직접 쓰는 것은 매우 위험하며, weighting/selection 보조로만 써야 한다는 점이 분명해졌습니다.

## 현재 최고 기록 유지 여부

- 최고 public은 여전히 `submission_a101_10.csv = 10.1064209775`
- 오늘 실험들은 이 기록을 넘지 못했습니다.

## 내일 방향

현재 기준으로 가장 합리적인 다음 방향은 아래와 같습니다.

1. `a101_10` 앵커 유지
2. correction layer 추가는 당분간 중단
3. `shift-heavy expert` 재학습 방향 유지
4. pseudo-group를 더 복잡하게 늘리기보다, 더 단순하고 물리적인 extreme 그룹 정의를 우선 사용
5. average OOF보다 `worst-group / adversarial subset / unseen-like` 기준 validation을 강화

## 한 줄 요약

오늘은 `a107`로 expert 재학습 방향이 더 건강하다는 점을 확인했고, `a108`로 pseudo-group 접근의 위험한 지점까지 정리했습니다. 내일부터는 `a101` 앵커를 유지한 채, correction layer가 아니라 validation과 expert 학습 기준을 더 정교하게 만드는 방향이 맞습니다.
