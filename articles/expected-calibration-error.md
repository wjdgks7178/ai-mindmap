# ECE(기대 보정 오차)

> ECE(Expected Calibration Error)는 [신뢰도 곡선](#reliability-diagram)의 "확신도 대 실제 정답률" 격차를 구간별로 가중 평균해 숫자 하나로 만든 지표다. 0에 가까울수록 모델이 말한 확신도를 믿을 수 있다.

## 쉽게 말하면
예보관의 "비 올 확률"과 실제 적중 비율의 어긋남을 날마다 재서 평균 낸 점수다. 어긋남이 평균 5%포인트면 ECE≈0.05. 단 어긋남을 구간별로 모은 뒤 구간에 든 날 수만큼 가중하므로, 자주 나오는 확신도 구간의 오차가 더 크게 반영된다.

## 자세히
- 정의: `ECE = Σ_b (n_b / N) · |acc_b − conf_b|` — b는 구간, n_b는 그 구간 샘플 수, acc_b는 실제 정답(양성) 비율, conf_b는 평균 확신도.
- scikit-learn에는 ECE 함수가 없다. `calibration_curve` 출력으로 직접 계산한다(위 공식).
- **구간 설정에 민감**: 구간 수(예: 10, 15)와 `uniform`/`quantile` 방식에 따라 값이 달라진다. 서로 다른 논문의 ECE를 단순 비교하면 안 된다.
- 한계: 확신도가 한 값에 몰린 모델은 한두 구간만 채워져 신뢰도가 낮고, 오차의 부호(과신인지 과소 확신인지)도 사라진다. 곡선을 함께 본다.
- Brier 점수와 달리 보정만 본다. Brier는 보정+변별력+잡음이 섞여 있다.
- LLM 응용: 정답이 있는 QA 벤치마크로 모델이 말한 확신도의 ECE를 잰다([LLM의 말로 한 확신도](#llm-verbalized-confidence)).
- 개선: 온도 스케일링 등 사후 보정으로 ECE를 줄인다([온도 스케일링](#temperature-scaling)). 보정이 좋아져도 정확도는 보통 변하지 않는다(순위가 유지되는 방식일 때).

## 그림으로 보기
```mermaid
flowchart LR
  A["예측 N개"] --> B["확신도 구간 나누기"]
  B --> C["구간별 |정답률 − 확신도|"]
  C --> D["샘플 비중으로 가중 평균"]
  D --> E["ECE"]
```

## 예시
10구간(각 100개), 어떤 구간의 확신도 0.9·실제 정답률 0.7이면 그 구간 기여 = 0.1 × 0.2 = 0.02. 모든 구간을 더한 값이 ECE.
```python
ece = sum(len(idx)/N * abs(acc[idx] - conf[idx]) for idx in bins)
```

## 헷갈리는 것과 비교
| 개념 | 차이 |
| --- | --- |
| ECE | 보정 격차의 가중 평균 |
| [신뢰도 곡선](#reliability-diagram) | 같은 격차를 그림으로 |
| 정확도 | 맞힌 비율 — 확신도와 무관 |
| [과신](#overconfidence) | ECE가 높은 한 형태 |

## 더 읽을거리
- [Probability calibration (scikit-learn)](https://scikit-learn.org/stable/modules/calibration.html) — 곡선·Brier·ECE 설명
