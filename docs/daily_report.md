# 일일 리포트

- 생성 날짜: `2026-04-25`
- 현재 최고 public 점수: `10.1064209775`
- 현재 최고 파일: `submission_a101_10.csv`

## 오늘의 핵심 변화

- `a109_09`를 public에 제출했고 결과는 `10.1085982977`이었습니다.
- `a109`에서는 복잡한 pseudo-group보다 단순한 물리 extreme expert와 `worst-group / testlike / baseline_hi` 중심 선택 기준이 더 낫다는 점을 확인했습니다.
- `a110`에서는 문제를 창고 운영 관점에서 다시 해석해, 미래 부하와 압력 요약을 직접 피처로 넣는 `future-window` 실험을 진행했습니다.
- `a110_09`를 public에 제출했고 결과는 `10.106859334`였습니다.

## 오늘 얻은 해석

1. `a109`는 `a108`보다 훨씬 건강한 방향이었지만, validation과 선택 기준만으로는 `a101_10`을 넘기기 어려웠습니다.
2. `a110`은 최고 기록을 넘지 못했지만, correction layer 계열과 다르게 backbone 쪽의 새로운 신호가 실제로 작동한다는 점을 보여줬습니다.
3. 이 문제는 현재 상태만 맞추는 회귀보다, 같은 시나리오 안에서 이미 주어진 25슬롯 전체 맥락과 가까운 미래 부하를 읽는 문제가 더 가깝다는 해석이 강화됐습니다.
4. 따라서 다음 단계는 correction layer를 다시 얹는 것이 아니라, `a101`의 강한 자산 위에 `future-window` 해석을 더 안정적으로 흡수하는 쪽이 맞습니다.

## 현재 최고 기록 유지 여부

- 최고 public은 여전히 `submission_a101_10.csv = 10.1064209775`
- `a109`, `a110` 모두 이 기록을 넘지는 못했습니다.

## 다음 방향

현재 기준으로 가장 합리적인 다음 방향은 아래와 같습니다.

1. `a101_10` 앵커 유지
2. correction layer 추가는 계속 보류
3. `shift-heavy expert` 재학습 방향은 유지하되, pseudo-group는 더 단순하게 관리
4. `future-window` 기반의 창고 부하 해석을 backbone 신호로 더 정교하게 흡수
5. average OOF보다 `worst-group / adversarial subset / unseen-like / future-stress` 기준 validation을 강화

## 한 줄 요약

오늘은 `a109`로 validation과 선택 기준만 바꾸는 데 한계가 있다는 점을 확인했고, `a110`으로 미래 부하 요약이 실제 신호라는 점을 확인했습니다. 다음 단계는 `a101` 앵커를 유지한 채, correction layer가 아니라 backbone과 validation을 다시 다듬는 쪽입니다.
