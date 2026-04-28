# 일일 리포트

- 생성 날짜: `2026-04-28`
- 현재 최고 public 점수: `10.0967991272`
- 현재 최고 제출 파일: `submission_a122_1045.csv`

## 오늘의 핵심 변화

오늘은 `a117_09` 근처의 단순 micro tuning이 거의 포화됐다는 사실을 확인한 뒤, high-error scenario를 다시 뜯어보는 방향으로 전환했습니다.

가장 큰 성과는 `a121` 분석과 `a122` 후보입니다.

- `a121`에서 `a117_09`의 오차 상위 시나리오를 분석했습니다.
- high-error group은 랜덤한 노이즈가 아니라 late slot, high pack pressure, high pack utilization, future stress 구간에서 강한 과소예측 패턴을 보였습니다.
- 이 해석을 바탕으로 `a122`에서는 `a117_09`를 앵커로 유지하고, stress risk가 높은 일부 행에만 작은 양수 uplift를 적용했습니다.
- `submission_a122_1045.csv`가 public `10.0967991272`를 기록하며 기존 최고 `10.1005923422`를 갱신했습니다.

## 오늘 확인한 실험

| 실험 | 결과 | 해석 |
| --- | ---: | --- |
| `a118_01` | `10.1018318718` | asymmetric clipped delta. OOF는 좋아 보였지만 public 개선 실패 |
| `a119_03` | `10.1010915332` | `a117_09` 근처 microgrid. 거의 같은 분포도 public 개선 실패 |
| `a120` | 미제출 | scenario bias calibrator. local 개선폭이 너무 작아 제출 가치 낮음 |
| `a121` | 분석용 | high-error group이 late/high-stress 과소예측이라는 점 확인 |
| `a122_1045` | `10.0967991272` | late/high-stress small uplift가 public에서 검증됨 |

## 현재 판단

1. `a117_09`는 여전히 매우 강한 앵커입니다.
2. `a118`, `a119`, `a120` 결과상 clipped ridge delta 자체를 더 미세하게 조절하는 방향은 포화에 가깝습니다.
3. `a121` 분석으로 public이 반응하는 새로운 오차 축을 찾았습니다.
4. `a122_1045`는 그 축이 실제 public에서도 통한다는 증거입니다.
5. 다음 단계는 `a122_1045` 주변에서 risk score, bin, shrink, uplift cap을 더 조심스럽게 탐색하는 것입니다.

## 다음 방향

다음 실험은 `a123`으로 이어가는 것이 좋습니다.

- `a122_1045`를 새 앵커로 삼기
- `all_stress_small` risk score 주변을 더 정밀하게 조정
- uplift 평균과 최대값을 과하게 키우지 않기
- late/high-pressure/high-utilization 구간의 양수 보정만 유지
- public-safe 후보와 조금 더 공격적인 후보를 분리해서 생성

## 한 줄 요약

오늘은 `a122_1045 = 10.0967991272`로 처음 10.10 벽을 깼고, late/high-stress 과소예측 보정이라는 다음 주력 방향을 확보했습니다.
