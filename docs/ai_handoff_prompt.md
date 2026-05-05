# 다른 AI에게 전달할 포트폴리오 정리 프롬프트

아래 내용을 그대로 다른 AI에게 전달하면, 데이콘 스마트 창고 출고 지연 예측 프로젝트를 이력서/포트폴리오/면접 답변용으로 다시 다듬는 데 사용할 수 있습니다.

---

## 복붙용 프롬프트

너는 데이터 사이언스 / 머신러닝 포트폴리오를 채용 관점에서 다듬는 전문 AI다.

내가 정리하려는 프로젝트는 **DACON 스마트 창고 출고 지연 예측 경진대회**다.  
목표는 단순한 점수 자랑이 아니라, 내가 어떤 문제 정의를 했고, 어떤 실험을 했고, 실패를 어떻게 해석했고, 최종적으로 어떤 방식으로 개선했는지를 포트폴리오에서 설득력 있게 보여주는 것이다.

아래 프로젝트 정보를 바탕으로 다음 산출물을 만들어줘.

1. GitHub README 상단에 넣을 프로젝트 소개문
2. 이력서 bullet 3개
3. 포트폴리오 상세 설명 섹션
4. 면접에서 말할 수 있는 1분 설명
5. 기술 키워드 정리
6. 너무 과장되어 보이는 표현이 있으면 현실적인 표현으로 다듬기

중요한 톤:

- 결과를 부풀리지 말 것
- 최종 목표였던 9점대에는 도달하지 못했지만, 초기 `11.83`에서 최종 `10.0038814352`까지 개선한 점을 명확히 쓸 것
- “실패 실험을 통해 방향을 바꿨다”는 점을 강점으로 표현할 것
- 단순 모델 나열보다 문제 재정의, feature engineering, OOD/generalization 분석, prediction distribution calibration 역량이 보이게 쓸 것
- 한국어로 자연스럽고 포트폴리오다운 문장으로 작성할 것

---

## 프로젝트 정보

### 대회 개요

- 대회명: DACON 스마트 창고 출고 지연 예측 경진대회
- 문제 유형: tabular + time-series regression
- 예측 대상: `avg_delay_minutes_next_30m`
- 평가 지표: MAE
- 데이터 구조: train 10,000 scenarios x 25 slots, test 2,000 scenarios x 25 slots
- 최종 public MAE: `10.0038814352`
- 최종 제출 파일: `submission_a156_046.csv`
- 초기 기준 public MAE: 약 `11.83`
- 전체 개선폭: 약 `1.8261` MAE 감소

### 내가 한 일

- 전체 실험 파이프라인 설계 및 반복 개선
- scenario/slot 구조를 반영한 feature engineering
- CatBoost, LightGBM, sequence model, residual ensemble, Mixture-of-Experts 실험
- `baseline + scale * routed_z` decomposition 구조 설계
- expected-error 기반 soft routing과 specialist expert 실험
- OOD/generalization 실패 분석
- future-window pressure feature, warehouse pressure feature, queueing-inspired feature 설계
- slot redistribution, phase-lead, tail calibration 후처리 실험
- 날짜별 실험 로그와 public score log 작성

### 핵심 실험 흐름

1. 초기에는 CatBoost/LightGBM/sequence model/residual ensemble로 접근했다.
2. public MAE를 `10.12` 근처까지 낮췄지만 residual correction만으로는 정체가 생겼다.
3. `baseline + scale * routed_z` 구조로 scenario baseline과 standardized deviation을 분리했고, `a101`에서 `10.1064209775`까지 개선했다.
4. DANN, hard routing, aggressive correction, pseudo-group reweighting을 시도했지만 public에서 흔들렸다.
5. 실패 분석을 통해 support/test-like 신호를 hard switch로 쓰면 위험하고, validation residual correction은 noise까지 학습할 수 있다는 판단을 얻었다.
6. 이후 문제를 `next_30m` 미래 지연 예측으로 다시 해석해 future-window, pressure, queueing feature를 설계했다.
7. 10.09 근처에서 미세 조정이 한계에 도달하자 raw-only reboot family를 만들었고 `10.0265`까지 큰 폭 개선했다.
8. 마지막에는 scenario 평균을 크게 흔들기보다 같은 scenario 안에서 어느 slot에 지연을 재분배할지 조정하는 slot redistribution과 phase-lead 접근을 사용했다.
9. 최종적으로 `a156_046`에서 public MAE `10.0038814352`를 기록했다.

### 주요 public score 흐름

| 단계 | public MAE | 의미 |
| --- | ---: | --- |
| 초기 기준 | `11.83` | baseline |
| a88 | `10.1201425252` | representation residual + specialist |
| a94 | `10.1133848903` | scenario baseline + specialist |
| a101 | `10.1064209775` | decomposition + soft router |
| a122 | `10.0967991272` | late/high-pressure uplift |
| a127 | `10.0941228322` | late/high-stress refinement |
| a137 | `10.02829` | raw-only reboot ensemble |
| a138 | `10.0265043299` | raw-only fine grid |
| a145_4830 | `10.010757563` | future-pressure slot redistribution |
| a151_886 | `10.0068002221` | queueing/domain reallocation |
| a155_481 | `10.0046018208` | future phase-lead + tail calibration |
| a156_046 | `10.0038814352` | final public-tail gamble |

### 포트폴리오에서 강조하고 싶은 메시지

- 단순히 모델을 더 많이 쌓는 것보다 문제 정의를 정확히 해석하는 것이 중요했다.
- OOF에서 좋아 보여도 public에서 실패하는 실험이 많았고, 이를 통해 validation mismatch와 OOD/generalization 문제를 분석했다.
- 실패 실험을 버리지 않고 다음 의사결정의 근거로 사용했다.
- 최종 개선은 `next_30m` 타겟 의미를 다시 해석해 future pressure, slot redistribution, phase-lead, tail calibration으로 이어진 과정에서 나왔다.
- 최종 목표였던 9점대에는 도달하지 못했지만, 실험 과정과 문제 해결 방식이 명확히 남아 있는 프로젝트다.

---

## 참고 문서

이 저장소에 있는 다음 문서를 함께 참고하면 좋다.

- `docs/portfolio_case_study.md`: 포트폴리오 상세 케이스 스터디
- `docs/resume_summary.md`: 이력서/포트폴리오 요약
- `docs/final_research_summary.md`: 최종 연구 요약
- `docs/public_score_log.json`: public score 흐름
- `docs/daily_logs/`: 날짜별 작업 기록
