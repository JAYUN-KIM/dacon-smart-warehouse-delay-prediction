# Project Overview

## Competition

- 대회명: 데이콘 스마트 창고 출고 지연 예측 AI 경진대회
- 목표: 향후 30분 평균 출고 지연 시간 예측
- 평가지표: MAE

## Data Structure

- Train: 10,000 scenarios x 25 time slots = 250,000 rows
- Test: 2,000 scenarios x 25 time slots = 50,000 rows
- Layout split:
  - train layouts: 250
  - test layouts: 100
  - seen layouts: 50
  - train-only layouts: 200
  - test-only layouts: 50

## Core Research Direction

초기에는 tabular + sequence base model을 만들고, 이후에는 best anchor prediction의 residual을 단계적으로 줄이는 방향으로 발전시켰습니다.

주요 축은 다음과 같습니다.

1. Layout-free sequence modeling
2. Residual CatBoost stack
3. Low-band selective correction
4. Sequence residual branch

## Main Experimental Evolution

- `a18`: EDA threshold + LGBM strong baseline
- `a48`: Transformer + LSTM + LGBM ensemble
- `a56/a66`: STT + TransLF + a48 weighted blend
- `a75`: residual CatBoost branch
- `a76/a77/a78`: anchor-based residual refinement
- `a79`: sequence residual branch
- `a81`: sequence residual V2
- `a82`: layout-aware residual expert
- `a83`: layout-aware sequence residual

## Current View

현재까지는 low-band residual correction + sequence residual branch가 가장 유효했고,  
최근에는 `layout_info.csv`를 직접 쓰는 layout-aware expert와 layout-aware sequence residual까지 확장했습니다.  
다만 10.12 근처에서 improvement가 매우 작아져, 이후에는 regime 분리, representation learning, pretrained/external branch 같은 더 근본적인 축이 필요하다고 판단하고 있습니다.
