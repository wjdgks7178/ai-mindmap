# 클래스 가중치 (Class Weights)

> 소수 클래스의 오류에 더 큰 벌점을 주도록 학습 손실을 가중해, 데이터를 바꾸지 않고 불균형을 보정하는 방법이다.

## 쉽게 말하면
시험에서 드문 유형 문제의 배점을 크게 주는 것이다. 그러면 학생(모델)이 드문 유형을 틀리지 않으려 더 신경 쓴다.

## 자세히
scikit-learn `compute_class_weight` 문서(2026-11 확인):
- `class_weight="balanced"`: 클래스 빈도에 **반비례**하여 가중. 공식 `weight[c] = n_samples / (n_classes × bincount(y)[c])`.
- 예: y=[1,1,1,1,0,0] → 클래스 0 가중치 6/(2×2)=1.5, 클래스 1은 6/(2×4)=0.75. 희소 클래스가 더 큰 가중.
- `class_weight`에는 `"balanced"`, 사용자 지정 dict, `None`을 줄 수 있다. 이 휴리스틱은 King & Zeng(2001, 희귀 사건 로지스틱 회귀)에서 영감을 받았다고 문서가 밝힌다.
- 많은 사이킷런 분류기(`LogisticRegression`, `SVC`, 트리 계열 등)가 `class_weight` 인자를 지원(일반 사실, 모델별 확인 권장). PyTorch에서는 손실 함수의 `weight` 인자로 같은 효과.
- 효과의 한계: 가중치가 너무 크면 소수 클래스 오탐이 늘고 정밀도가 떨어질 수 있다 → 임계값·[F-beta](#f-beta)로 함께 조절(일반 조언).

## 그림으로 보기
```mermaid
flowchart LR
  D["다수 90 : 소수 10"] --> W["가중치 계산<br/>소수 ≫ 다수"]
  W --> L["손실 = Σ 가중치 × 샘플 오류"]
  L --> M["소수 오류에 더 민감한 모델"]
```

## 예시
```python
LogisticRegression(class_weight="balanced").fit(X_train, y_train)
```
고장 예측처럼 양성이 2%인 문제에서 첫 시도로 쓴다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| 클래스 가중치 | 손실에 가중, 데이터 불변 |
| [SMOTE](#smote) | 데이터에 합성 샘플 추가 |
| 임계값 조정 | 예측 단계에서 균형 조정 |
| [정밀도-재현율 트레이드오프](#precision-recall-tradeoff) | 가중 후 결과를 보는 틀 |

## 더 읽을거리
- [compute_class_weight (scikit-learn)](https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html) — balanced 공식과 예제.
