# 데이콘 스마트 창고 출고 지연 예측 기록

데이콘 스마트 창고 출고 지연 예측 AI 경진대회를 진행하면서 만든 실험 기록 저장소입니다.

이 저장소의 목표는 단순히 점수만 남기는 것이 아니라,

- 지금 무엇을 시도하고 있는지
- 왜 그 방향으로 가고 있는지
- 어떤 실험이 실제로 먹혔는지
- 다음에는 무엇을 해볼지

를 날짜별로 남기는 것입니다.

## 현재 최고 기록

- 최고 public 점수: `10.1064209775`
- 제출 파일: `submission_a101_10.csv`
- 기준 날짜: `2026-04-21`

## 현재 핵심 판단

지금은 `a94 family`를 조금씩 더 다듬는 국면이 아니라,

- `scenario baseline`
- `scenario scale`
- `slot deviation`
- `sample별 expert routing`

으로 문제를 다시 나누는 `a100 family`를 주력으로 밀어붙이는 단계입니다.

즉, 이제 핵심은 “평균적으로 가장 잘 맞는 모델 하나”를 찾는 것이 아니라,

**어떤 샘플에서 어떤 expert가 덜 틀리는지를 고르는 시스템**

을 만드는 것입니다.

## 최근 실험 흐름

### 1. 초기 강한 앙상블 축

- LightGBM
- Transformer
- LSTM
- STT
- TransLF

이 축으로 기본 베이스를 만들었습니다.

### 2. residual stack 축

- `a75 ~ a81`
- 강한 앵커 위에 residual correction을 쌓는 방식

이 구간에서 public 점수를 꾸준히 깎았습니다.

### 3. layout / sequence 확장

- `a82`, `a83`
- layout-aware residual / sequence residual

구조적으로 의미는 있었지만 큰 점프까지는 못 갔습니다.

### 4. representation + shift specialist 축

- `a88`
- representation 신호를 shift subset에만 적용

이 구간에서 다시 의미 있는 상승이 나왔습니다.

### 5. integrated shift specialist

- `a94`
- representation residual + scenario baseline + shift/high/unseen combo specialist 통합

이 축에서 큰 점프가 났고, 이후 오랫동안 주력 family가 되었습니다.

### 6. decomposition + routing 축

- `a100`
- `a101`

최근에는 `baseline + scale + routed deviation` 구조로 문제를 다시 정의하고 있으며,
이 축이 실제로 다시 큰 개선을 만들고 있습니다.

## 최근 최고 점수 흐름

- `a88_27`: `10.1201425252`
- `a94_51`: `10.1133848903`
- `a100_05`: `10.1090848449`
- `a101_10`: `10.1064209775`

## 지금 보고 있는 방향

현재 가장 유망한 방향은 아래와 같습니다.

1. `scenario baseline`을 먼저 안정적으로 맞추기
2. `scale(MAD / IQR 기반)`를 별도로 예측하기
3. `z-space`에서 여러 expert가 deviation을 예측하게 하기
4. router가 expert별 expected error를 보고 soft routing 하기
5. confidence가 낮은 샘플은 global 쪽으로 fallback 하기

## 문서 구성

- [프로젝트 개요](</C:/open/dacon-smart-warehouse-portfolio/docs/project_overview.md>)
- [실험 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/experiment_log.md>)
- [일일 리포트](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_report.md>)
- [일자별 기록](</C:/open/dacon-smart-warehouse-portfolio/docs/daily_logs>)
- [public 점수 로그](</C:/open/dacon-smart-warehouse-portfolio/docs/public_score_log.json>)
