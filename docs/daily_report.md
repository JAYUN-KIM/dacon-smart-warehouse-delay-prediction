# 일일 리포트

- 생성 날짜: `2026-05-01`
- 현재 최고 public 점수: `10.0920140626`
- 현재 최고 제출 파일: `submission_a131_101.csv`
- 다음 작업: `a132`

## 오늘의 변화

오늘은 `a127_003` 이후의 late/high-stress 보정축을 `a128`, `a129`, `a130`까지 밀어본 뒤, 같은 축의 포화 여부를 확인했습니다. `a128`, `a129`는 아주 작은 폭이지만 연속 개선을 만들었고, `a130`은 scenario offset pivot을 더 크게 넣었을 때 public이 악화되면서 단순한 보정 강화가 한계에 가까워졌다는 신호를 줬습니다.

이후 `a131`에서는 기존 anchor 주변만 만지는 방식에서 벗어나, raw train/test와 layout_info만 사용하는 from-scratch direct LGBM family를 새로 만들었습니다. pure direct 제출은 예측 평균이 기존 최고와 많이 달라 위험했지만, `a129_001` anchor에 direct signal을 1.5%만 흡수한 `a131_101`이 public에서 다시 큰 폭의 개선을 만들었습니다.

오늘 확인된 public 흐름은 다음과 같습니다.

| 제출 | public MAE | 해석 |
| --- | ---: | --- |
| `submission_a128_001.csv` | `10.0939941912` | a127 방향을 더 안전하게 밀어 10.093대 진입 |
| `submission_a129_001.csv` | `10.0939015979` | scenario-relative shift 보정으로 미세하지만 추가 개선 |
| `submission_a130_002.csv` | `10.0946330552` | scenario offset pivot은 public에서 악화. 같은 축의 공격적 확장은 위험 |
| `submission_a131_101.csv` | `10.0920140626` | raw direct LGBM signal을 anchor에 낮은 비율로 흡수해 새 최고점 달성 |

## 오늘의 결론

1. late/high-stress uplift 축은 아직 의미가 있지만, `10.0939` 근처부터는 단순 강화만으로는 개선폭이 작아졌습니다.
2. `a130`의 악화는 scenario offset을 크게 밀면 public/private overfit 위험이 커진다는 경고입니다.
3. `a131`의 pure direct model은 단독 제출로는 위험하지만, 기존 계열과 다른 신호를 제공했습니다.
4. 새 신호를 크게 쓰는 것이 아니라 1~3% 수준으로 매우 작게 흡수했을 때 안정적으로 개선됐습니다.
5. 다음 실험은 기존 anchor 보정과 from-scratch direct signal을 동시에 다루되, test 분포가 무너지는 후보는 제출 후보에서 제외해야 합니다.

## 다음 방향: a132

`a132`는 `a131_101`을 새 anchor로 잡고, 다음 방향을 우선합니다.

- direct row LGBM signal의 alpha를 `0.010~0.035` 범위에서 세밀하게 재탐색
- direct quantile signal은 단독보다 보조 신호로만 제한
- slot-direct 계열은 OOF가 좋아 보여도 test mean이 낮게 무너졌으므로 제출 후보에서 제외
- late/high-stress uplift와 direct signal이 겹치는 구간에서만 selective alpha 적용
- 평균 예측값과 test max가 기존 최고 분포에서 크게 벗어나지 않는 후보 우선

## 한 줄 요약

오늘은 `10.0941228322 -> 10.0920140626`까지 낮췄고, 기존 보정축의 포화 신호를 확인한 뒤 from-scratch direct model signal을 아주 낮은 비율로 흡수하는 새 개선축을 찾았습니다.
