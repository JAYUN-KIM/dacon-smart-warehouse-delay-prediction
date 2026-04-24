# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하면서, 실험 흐름과 판단 근거를 한국어로 정리해두는 저장소입니다.

이 저장소의 목적은 단순히 점수만 적는 것이 아니라 아래 내용을 날짜별로 남기는 것입니다.

- 지금 어떤 방향으로 실험하고 있는지
- 왜 그 방향을 선택했는지
- 어떤 실험이 실제 public 점수 개선으로 이어졌는지
- 어떤 실험이 로컬 OOF에서는 좋아 보여도 public에서 실패했는지

## 현재 최고 기록

- 최고 public 점수: `10.1064209775`
- 제출 파일: `submission_a101_10.csv`
- 기록 날짜: `2026-04-21`

## 현재 핵심 판단

지금 메인 방향은 `a94 family` 미세조정이 아니라 `a100 family`입니다.

현재 가장 중요한 구조는 아래와 같습니다.

1. `scenario baseline`
2. `scenario scale`
3. `standardized deviation`
4. `soft routing`
5. `expert 재학습`

즉 지금은 “평균적으로 잘 맞는 모델 하나”를 더 찾는 문제보다, 어떤 샘플에서 어떤 expert를 믿어야 하는지를 더 안정적으로 결정하는 문제가 핵심입니다.

## 최근 실험 요약

### 1. specialist 계열

- `a88`: representation 기반 shift expert
- `a94`: representation residual + scenario baseline + shift/high/unseen combo specialist

이 구간에서는 `shift/high/unseen` 같은 어려운 구간을 따로 보는 specialist 방향이 실제로 잘 먹혔습니다.

### 2. decomposition + routing 계열

- `a100`: `baseline + scale + routed deviation`
- `a101`: soft expected-error router + fallback

이 구조가 현재 최고 기록인 `a101_10 = 10.1064209775`를 만들었습니다.

### 3. a101 이후 correction layer 실패

`a102`, `a104`, `a105`, `a106`은 모두 `a101` 위에 correction을 더 얹는 방향이었습니다.

공통점:
- 로컬 OOF는 좋아 보이는 경우가 있었음
- public에서는 전부 `a101_10`을 넘지 못함

해석:
- `a100 family`가 틀린 것이 아니라
- correction layer가 local OOF에 과적합되고 있다고 판단 중

### 4. a107에서 얻은 교훈

`a107`은 correction layer를 더 얹지 않고, `shift-heavy expert` 자체를 다시 학습한 실험이었습니다.

- `a101` direct router OOF: `7.4224`
- `a107` direct router OOF: `7.4162`
- public: `10.1067154934`

해석:
- correction layer 추가보다 expert 재학습이 더 건강한 방향임
- 다만 아직 `a101_10`을 넘길 정도로 강하지는 않음

### 5. a108에서 얻은 교훈

`a108`은 pseudo-group 기반 `shift-heavy expert` 재학습 실험이었습니다.

중간에 중요한 문제를 한 번 잡았습니다.

- scenario hardness를 feature에 직접 넣었더니 비정상적으로 좋은 로컬 성능이 나옴
- 이건 실제 개선이 아니라 leakage-like 착시로 판단
- hardness는 feature가 아니라 weight에만 쓰도록 수정 후 다시 검증

수정 후:
- `a108` direct router OOF: `7.4219`
- public: `10.1122539111`

해석:
- pseudo-group 방향은 완전히 틀린 것은 아님
- 하지만 현재 구현은 아직 public 제출용 카드가 아님
- hardness를 직접 feature로 쓰는 건 매우 위험함

## 현재 방향

지금 기준으로 다음 방향은 아래처럼 정리하고 있습니다.

1. `a100 family` 유지
2. `a101_10`을 메인 public 앵커로 유지
3. correction layer 추가는 당분간 중단
4. `shift-heavy expert` 자체를 더 잘 학습시키는 방향으로 이동
5. `support/testlike`는 주연 신호가 아니라 보조 feature로만 사용
6. average OOF보다 `worst-group / adversarial subset` 중심 검증 강화

즉 지금은 새 family로 갈아탈 때라기보다, `a100 family`를 더 안정적으로 운영할 수 있게 validation과 expert 학습 기준을 바꾸는 단계입니다.

## 문서 구성

- [프로젝트 개요](</C:/open/dacon-smart-warehouse-portfolio/docs/project_overview.md>)
- [실험 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/experiment_log.md>)
- [일일 리포트](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_report.md>)
- [날짜별 작업 기록](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_logs>)
- [public 점수 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/public_score_log.json>)
