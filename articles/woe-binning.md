# WoE 구간화

> 숫자 변수를 구간으로 나누고 범주와 구간을 위험 가중치(WoE, Weight of Evidence) 값으로 바꾸는 스코어카드 전처리. 로지스틱 회귀를 설명하기 쉬운 점수표로 만드는 표준 방식이다.

## 쉽게 말하면
"나이 25세 미만"이라는 구간 자체를 "위험 점수 +0.8"처럼 한 숫자로 바꿔서, 모델이 구간별 위험도를 곧바로 쓰게 하는 번역 단계다.

## 자세히
출처: OptBinning 이진 목표 튜토리얼 페이지(2026-11-15 확인). 아래 숫자는 그 페이지의 예시이다.
- **WoE와 사건률**: 사건률(event rate, 부실 비율)이 낮은 구간일수록 WoE가 높다. 페이지는 "사건률이 단조 증가하면 WoE는 단조 감소"라고 설명. 예시 `mean radius`의 가장 낮은 사건률 구간 `[16.93, inf)`는 사건률 0.008475, WoE 5.283323. 부호 규칙(좋음/나쁨 방향)은 도구마다 다를 수 있다. WoE 공식 자체는 이 페이지에 적혀 있지 않았다(통상 ln(비사건 분포/사건 분포)).
- **IV(Information Value)**: 변수의 구분력 요약. 페이지는 Jeffrey 발산으로 설명하며 구간별 IV를 합산. 예시 `mean radius` 총 IV 5.043925. 예시 `NAME_INCOME_TYPE`는 IV 0.0575, Gini 0.1218, KS 0.0836.
- **구간 표**: 열은 Bin, Count, Count(%), Non-event, Event, Event rate, WoE, IV, JS. 특수값·결측 행이 따로 있을 수 있다.
- **단조 추세**: OptBinning의 `monotonic_trend`는 기본 `"auto"`(오름·내림·봉우리·골짜기 중 IV를 최대화할 가능성이 큰 모양 선택), 강제로 `"descending"` 등을 지정 가능. 범주형은 사건률에 대해 항상 단조 증가하는 최적 구간을 만든다.
- **신용 맥락의 이유**: 구간별 위험도가 단조(예: 연체가 늘수록 위험↑)로 정렬되면 점수표 설명과 [이유 코드](#reason-codes)가 쉬워진다. 단조성이 깨지면 [잘못된 부호 진단](#wrong-sign-diagnostic).

## 그림으로 보기
```mermaid
flowchart LR
A["원 변수<br/>예: 나이"] --> B["구간화"]
B --> C["구간별 사건률"]
C --> D["WoE 값으로 치환"]
D --> E["로지스틱 회귀"]
E --> F["점수표"]
```

## 예시
```python
from optbinning import OptimalBinning
optb = OptimalBinning(name="age", dtype="numerical", monotonic_trend="descending")
optb.fit(x, y)
print(optb.binning_table.build())   # Bin, Event rate, WoE, IV ...
x_woe = optb.transform(x, metric="woe")
```

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| WoE | 구간별 위험 가중치 |
| IV | 변수 전체 구분력 |
| 원-핫 인코딩 | 구간마다 별도 더미 |
| [단조 제약](#monotonic-constraints) | 모델 학습 시 방향 강제 |

## 더 읽을거리
- [OptBinning: binary target tutorial](https://gnpalencia.org/optbinning/tutorials/tutorial_binary.html) — WoE·IV·monotonic_trend 예시
