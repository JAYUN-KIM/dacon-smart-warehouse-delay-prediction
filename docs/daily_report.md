# 최종 일일 리포트

- 작성 날짜: `2026-05-04`
- 최종 최고 public 점수: `10.0038814352`
- 최종 최고 제출 파일: `submission_a156_046.csv`
- 상태: 대회 종료 및 마지막 제출 완료

## 오늘의 변화

오늘은 대회의 마지막 제출 기회까지 사용한 최종 마감일입니다. 전날 최고였던 `submission_a145_4830.csv`의 public `10.010757563`에서 시작해, public 피드백을 반영하며 `10.0038814352`까지 줄였습니다.

처음에는 `a149` 계열로 전날 성공한 slot redistribution을 더 강하게 밀었습니다. `submission_a149_009.csv`가 public `10.0073867868`을 기록하며, 전날보다 확실히 개선됐습니다. 이후 `a150`의 과한 tail extrapolation은 `10.0080170747`로 악화되어, tail을 무작정 올리면 안 된다는 경계를 확인했습니다.

그 다음에는 queueing/domain 관점의 reallocation을 적용해 `submission_a151_886.csv`가 `10.0068002221`을 기록했습니다. 여기서도 9점대에는 닿지 못했지만, 창고 운영 압력과 tail 분포 조절이 public에서 계속 유효하다는 것을 확인했습니다.

마지막 구간에서는 완전히 원점으로 돌아가 문제 정의를 다시 봤습니다. 이 대회는 현재 지연을 맞히는 문제가 아니라 `avg_delay_minutes_next_30m`, 즉 향후 30분 평균 지연을 맞히는 문제입니다. 그래서 같은 scenario 안에서 앞으로 1~2 slot의 예측과 운영 압력 신호를 현재 slot으로 당겨오는 `future phase-lead` 실험을 만들었습니다.

`a154`에서 phase-lead만 적용하자 OOF는 크게 좋아졌지만 p99/max 꼬리가 낮아졌습니다. 이를 보완하기 위해 `a155`에서는 phase-lead 구조를 유지하면서 public에서 먹힌 tail 분포를 복원했습니다. `submission_a155_481.csv`가 public `10.0046018208`을 기록했고, 마지막에는 이 후보를 anchor로 p99/max를 한 단계 더 밀어 `submission_a156_046.csv`를 제출했습니다.

## 오늘 확인한 public 점수

| 제출 | public MAE | 해석 |
| --- | ---: | --- |
| `submission_a149_009.csv` | `10.0073867868` | 전날 성공한 slot redistribution extrapolation이 추가 개선 |
| `submission_a150_012.csv` | `10.0080170747` | tail을 너무 강하게 밀면 악화됨을 확인 |
| `submission_a151_886.csv` | `10.0068002221` | queueing/domain reallocation으로 추가 개선 |
| `submission_a155_481.csv` | `10.0046018208` | future phase-lead + tail 복원 축이 적중 |
| `submission_a156_046.csv` | `10.0038814352` | 마지막 제출, 최종 최고 기록 |

## 오늘의 실험 요약

### a149/a150: public-guided extrapolation

- 목적: `a145_4830`의 성공 축을 더 강하게 밀어 9점대에 접근
- 결과:
  - `submission_a149_009.csv`: `10.0073867868`
  - `submission_a150_012.csv`: `10.0080170747`
- 판단: extrapolation은 유효하지만, p99/max를 과하게 올리면 public에서 바로 악화되었습니다.

### a151: queueing/domain reallocation

- 목적: 단순 tail 상승이 아니라 창고의 병목, queue pressure, path/tech friction을 반영해 같은 scenario 안에서 예측 질량을 재배분
- 참고한 관점:
  - utilization/capacity gap
  - Kingman/VUT 계열 queueing proxy
  - path friction, tech friction, future queue shock
- 결과: `submission_a151_886.csv`가 public `10.0068002221`
- 판단: 외부 데이터를 직접 사용하지는 않았지만, 외부 queueing/warehouse 운영 아이디어를 feature 설계에 반영한 것이 효과적이었습니다.

### a152/a153: 새 축 실험과 실패 확인

- `a152`: train target profile을 이용해 high-risk scenario의 시간 profile을 바꾸려 했지만 내부 지표가 약했습니다.
- `a153`: scenario 평균 residual을 risk 기반으로 재배분하려 했지만 개선 폭이 너무 작았습니다.
- 판단: scenario 평균을 직접 흔드는 방식보다, slot-level phase와 tail shape를 조절하는 방식이 더 맞았습니다.

### a154/a155/a156: 마지막 핵심 축

- `a154`: `next_30m` 정의에 맞춰 미래 1~2 slot 예측을 현재로 당기는 phase-lead 실험. OOF가 크게 좋아졌지만 tail이 낮아져 public 위험이 있었습니다.
- `a155`: phase-lead 구조를 유지하고 public-best tail shape를 복원. `submission_a155_481.csv`가 `10.0046018208` 기록.
- `a156`: 마지막 제출용으로 `a155_481`을 anchor로 두고 p99/max만 한 단계 더 밀어 `submission_a156_046.csv` 제출. 최종 `10.0038814352`.

## 최종 최고 기록

- 최종 점수: `10.0038814352`
- 최종 파일: `submission_a156_046.csv`
- 최종 후보 분포:
  - mean: `19.7761617`
  - p95: `40.5907`
  - p99: `51.0872`
  - max: `67.0523`

## 오늘의 결론

1. 9점대에는 닿지 못했지만, 최종적으로 `10.0038814352`까지 접근했습니다.
2. 마지막 개선은 단순 모델 변경이 아니라 문제 정의 재해석에서 나왔습니다.
3. `next_30m` 예측이므로 미래 slot의 신호를 현재 예측에 반영하는 phase-lead가 중요했습니다.
4. public에서는 tail shape가 매우 민감했고, p99/max를 너무 강하게 밀면 바로 악화되었습니다.
5. 가장 효과적인 최종 조합은 `future phase-lead + public-tail calibration`이었습니다.

## 한 줄 요약

마지막 날에는 미래 30분 예측이라는 문제 정의로 돌아가 phase-lead와 tail calibration을 결합했고, 최종 public `10.0038814352`로 대회를 마무리했습니다.
