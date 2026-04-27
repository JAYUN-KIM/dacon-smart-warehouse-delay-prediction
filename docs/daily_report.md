# 일일 리포트

- 생성 날짜: `2026-04-27`
- 현재 최고 public 점수: `10.1005923422`
- 현재 최고 파일: `submission_a117_09.csv`
- 내일 우선 확인 후보: `submission_a118_01.csv`

## 오늘의 핵심 변화

- `a114_09 = 10.103316418`을 기준 앵커로 두고, 새로운 direct family를 탐색했습니다.
- `a116`에서 25개 슬롯을 한 번에 예측하는 `ridge seq2seq` 계열을 실험했습니다.
- `a116` direct 모델 자체는 OOF 기준 약했지만, `a114` 앵커와 다른 방향의 delta 정보를 갖고 있다는 점을 확인했습니다.
- `a117`에서 ridge direct prediction을 그대로 쓰지 않고, `a114` 앵커와의 차이만 clipped blend했습니다.
- `submission_a117_09.csv`가 public `10.1005923422`를 기록하며 기존 최고였던 `a114_09`를 갱신했습니다.
- 더 강한 반영 계열은 `10.1014682069`로 `a117_09`를 넘지 못해, 이 방향은 “더 세게”가 아니라 “더 안전하게” 조절해야 한다는 결론을 냈습니다.
- `a118`에서는 `a117_09`의 안전한 평균/최댓값 대역을 유지하면서 delta를 비대칭 클리핑하는 후보를 만들었습니다.

## 오늘 얻은 해석

1. `a114`의 future-window scenario baseline/scale 해석은 여전히 유효합니다.
2. `a116` ridge seq2seq는 단독 모델로는 약하지만, 기존 앵커가 놓치는 방향의 정보를 일부 갖고 있습니다.
3. public 개선은 direct 모델을 크게 섞을 때가 아니라, delta를 작게 잘라서 얇게 반영할 때 나왔습니다.
4. `a117_09`의 성공 구간은 대략 `q98 clip + alpha 0.08` 수준입니다.
5. 평균 예측값과 최댓값이 `a117_09`보다 올라가는 후보는 OOF가 좋아도 public에서 흔들릴 수 있습니다.
6. 따라서 다음 탐색은 OOF 1등을 고르는 방식이 아니라, public에서 먹힌 shape를 유지하는 안정성 중심 후보 선택이 맞습니다.

## 현재 최고 기록

- 최고 public: `submission_a117_09.csv = 10.1005923422`
- 이전 최고: `submission_a114_09.csv = 10.103316418`
- 개선폭: 약 `0.002724`

## 내일 확인할 후보

### `submission_a118_01.csv`

- 방식: `a114/a117` 앵커 기반 asymmetric clipped ridge delta blend
- OOF MAE: `7.7275009155`
- test mean: `18.356560`
- test max: `44.054348`
- `a117_09` 대비 평균 변화량: 약 `0.0244`
- 판단: 한 번에 크게 흔드는 후보가 아니라, `a117_09`의 안전한 분포를 유지하면서 일부 delta shape만 바꾼 후보

## 다음 방향

현재 기준으로 가장 합리적인 다음 방향은 아래와 같습니다.

1. 내일 `submission_a118_01.csv` public 점수를 먼저 확인
2. `a118_01`이 개선되면 asymmetric clipping 계열을 더 좁게 탐색
3. `a118_01`이 밀리면 `a117_09`가 현재 안전 앵커라는 판단을 유지
4. direct ridge prediction은 단독 모델로 제출하지 않고 delta provider로만 사용
5. correction layer, hard mask, aggressive fallback은 계속 보류
6. 10.00대 진입을 위해서는 큰 새 family보다 public-valid delta band를 더 정밀하게 찾는 쪽이 우선

## 한 줄 요약

오늘은 `a114` 이후 정체를 깨고 `a117_09 = 10.1005923422`로 새 최고 기록을 만들었습니다. 핵심은 새 direct 모델을 믿고 크게 갈아타는 것이 아니라, 약한 direct 모델의 방향성만 clipped delta로 얇게 흡수하는 것이었습니다.
