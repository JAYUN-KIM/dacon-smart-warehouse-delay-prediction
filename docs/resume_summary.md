# Resume / Portfolio Summary

## Project

DACON 스마트 창고 출고 지연 예측 AI 경진대회 참여  
향후 30분 평균 출고 지연 시간을 예측하는 MAE 최적화 문제를 해결했습니다.

## My Contributions

- 시나리오 단위(25-step) 시계열 구조를 반영한 sequence modeling pipeline 설계
- layout generalization 문제를 고려한 layout-free feature engineering
- Transformer, STT, LSTM, LightGBM 기반 ensemble 연구
- best anchor prediction의 residual을 단계적으로 줄이는 multi-stage residual modeling 설계
- 저지연 구간(low-band) 전용 correction 전략 설계 및 검증
- sequence residual branch를 추가하여 새로운 error pattern 확보

## Technical Keywords

- Python
- PyTorch
- CatBoost
- LightGBM
- GroupKFold
- Sequence Modeling
- Residual Learning
- Ensemble Optimization
- Feature Engineering
- Experiment Tracking

## Outcome

- 반복적인 실험과 residual ensemble 개선을 통해 public leaderboard score를 지속적으로 개선
- best public score: `10.121418246`
- 단순 가중 평균을 넘어서, scenario-level sequence residual modeling이 실제 점수 개선에 기여함을 확인

