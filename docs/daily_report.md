# 일일 리포트

- 생성 날짜: `2026-05-02`
- 현재 최고 public 점수: `10.0265043299`
- 현재 최고 제출 파일: `submission_a138_147.csv`
- 다음 작업: `a139`

## 오늘의 변화

오늘은 기존 late/high-stress 보정축을 계속 미세 조정하는 방식에서 벗어나, raw train/test와 layout 정보를 중심으로 다시 시작하는 방향을 강하게 시도했습니다. 초반 `a132`, `a133`, `a135`는 10.09대 초반에서 소폭 개선에 그쳤지만, 외부에서 받은 ranker 코드의 정렬 로직을 점검하고 raw-only domain reboot ensemble로 재구성하면서 큰 점프가 나왔습니다.

가장 중요한 변화는 기존 best anchor나 이전 제출 예측을 모델 입력으로 쓰지 않고, raw feature와 scenario-level/future-window/domain feature만으로 새 신호를 만든 점입니다. 이 신호를 ranker 계열과 결합한 `a137_011`이 public `10.02829`를 기록했고, 이후 같은 raw-only family 안에서 분포를 크게 흔들지 않는 fine grid 후보 `a138_147`이 `10.0265043299`로 오늘 최고점을 갱신했습니다.

## 오늘 확인한 public 점수

| 제출 | public MAE | 해석 |
| --- | ---: | --- |
| `submission_a132_002.csv` | `10.0913986125` | direct signal refinement로 전일 best 대비 소폭 개선 |
| `submission_a133_104.csv` | `10.0905078248` | alpha gamble 계열이 10.090대까지 접근했지만 여전히 미세 개선 |
| `submission_a135_003.csv` | `10.0901537375` | ranker signal을 섞어 10.0901까지 개선 |
| `submission_a137_011.csv` | `10.02829` | raw-only reboot ensemble이 대형 개선을 만들며 방향 전환 성공 |
| `submission_a138_147.csv` | `10.0265043299` | a137 성공 분포를 유지한 fine grid로 현재 최고점 갱신 |

## 오늘의 핵심 실험

### ranker 코드 점검

- 받은 코드: `dacon_236696_ranker.py`
- 확인 내용: 명시적인 time/slot column이 없을 때 운영 변수인 `wms_response_time_ms` 같은 컬럼을 시간 정렬 기준으로 잘못 잡을 위험이 있었습니다.
- 조치: 명시적 시간 컬럼이 없으면 `ID` 순서를 우선 사용하도록 정렬 로직을 수정했습니다.
- 검증:
  - smoke fixed OOF MAE: `9.11882`
  - LGB 5-fold ranker OOF MAE: `8.89765`

### a136/a137 raw-only reboot

- 생성 코드:
  - `model_a136_domain_reboot.py`
  - `model_a137_raw_reboot_ensemble.py`
- 핵심 아이디어:
  - 기존 제출 예측을 feature로 쓰지 않음
  - raw train/test/layout_info 기반의 scenario aggregate, future-window, pressure/load, ranker signal을 새로 구성
  - a136 domain reboot와 fixed ranker를 ensemble
- 검증:
  - a136 OOF MAE: `8.609878597985363`
  - ranker OOF MAE: `8.89765201581869`
  - a137 candidate OOF MAE: `8.58505361649153`
- public 결과:
  - `submission_a137_011.csv`: `10.02829`

### a138 fine grid

- 생성 코드: `model_a138_raw_reboot_finegrid.py`
- 대표 후보:
  - `submission_a138_147.csv`
  - 설명: `w_a136_0.82_center_p80_alpha_1.010`
  - OOF MAE: `8.584451426707153`
  - 예측 평균: `19.776156630979433`
  - p50: `15.697762928549192`
  - p99: `48.534802809912904`
  - max: `64.41252113067038`
- 선택 이유:
  - `a137_011`과 예측 분포가 매우 가까움
  - 중복 후보인 `a138_108`은 제외
  - OOF는 개선되면서 public-hit 분포에서 크게 벗어나지 않음
- public 결과:
  - `submission_a138_147.csv`: `10.0265043299`

## 오늘의 결론

1. 기존 late/high-stress uplift 축은 유효했지만 10.09대에서는 개선폭이 작아졌습니다.
2. 오늘의 큰 점프는 기존 anchor 미세 조정이 아니라 raw-only reboot family에서 나왔습니다.
3. public code나 외부 아이디어를 그대로 믿지 않고 시간 정렬, 데이터 사용 범위, 누수 가능성을 점검한 것이 중요했습니다.
4. 이전 제출 예측을 모델 입력으로 쓰지 않는 raw-only 구조가 public에서 크게 먹힌 만큼, private 안정성 관점에서도 기존 microblend보다 더 건강한 축으로 보입니다.
5. `a138_147`은 `a137_011`의 성공 분포를 유지하면서 한 번 더 개선했기 때문에, 다음 실험도 이 family를 중심으로 하되 단순 fine grid만 반복하면 9점대 진입까지는 부족할 수 있습니다.

## 다음 방향: a139

`a139`에서는 raw-only reboot family를 유지하되, 단순 alpha grid가 아니라 다음 중 하나 이상을 추가합니다.

- ranker family를 하나 더 다양화해 error correlation을 낮추기
- scenario-level queue/load/capacity 관점의 domain feature 확장
- future-window feature를 slot별 예측이 아니라 scenario pressure regime 분류에도 사용
- high-delay tail에서만 작동하는 별도 raw-only specialist를 만들되 hard switch는 금지
- public-hit 분포를 지키는 범위 안에서 p95~p99 tail을 조금 더 정밀하게 보정

## 한 줄 요약

오늘은 기존 축을 과감히 내려놓고 raw-only reboot ensemble로 방향을 바꿨고, `submission_a138_147.csv`가 public `10.0265043299`를 기록하면서 9점대 진입 직전까지 크게 전진했습니다.
