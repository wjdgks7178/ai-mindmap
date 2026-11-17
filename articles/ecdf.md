# 경험적 누적분포함수

> 표본에서 "값이 x 이하인 관측의 비율"을 x의 함수로 나타낸 계단 함수(ECDF, Empirical CDF). 분포 모양을 가정 없이 표본 그대로 요약하며, KS 검정의 통계량이 이 함수들 사이의 최대 차이다.

## 쉽게 말하면
반 학생들의 시험 점수를 작은 순서로 세워 두고 "이 점수 이하가 몇 퍼센트인가?"를 그린 계단이다. 점수가 있는 곳에서 한 칸씩 올라가 마지막에 100%에 닿는다.

## 자세히
출처: SciPy 공식 문서 `scipy.stats.ecdf`(열어서 읽음, 문서는 SciPy 1.18.0 기준이라고 표기) + 이 세션의 직접 실행(SciPy 1.17.1).
- **함수**: `scipy.stats.ecdf(sample)`는 `ECDFResult`를 돌려주며 `cdf`(경험적 누적분포함수)와 `sf`(경험적 생존 함수, CDF의 여집합)를 담는다. 입력은 1차원 배열이거나 우측 중도 절단 자료(`CensoredData`)이며, 중도 절단이면 ECDF는 Kaplan-Meier 추정량이 된다.
- **속성(문서)**: `quantiles`(계단을 정하는 고유 표본 값), `probabilities`(각 분위수의 확률 추정), `evaluate(x)`(x에서의 값), `plot(ax)`, `confidence_interval(confidence_level=0.95)`(Greenwood 계열 공식을 쓴다고 문서가 적음).
- **문서 예**: 1마일 달리기 시간 다섯 개의 `quantiles`는 [5.2, 5.58, 6.23, 6.42, 7.06], `probabilities`는 [0.2, 0.4, 0.6, 0.8, 1.0].
- **직접 실행(이 세션)**: 표본 [2, 3, 3, 5, 8]의 ECDF는 `quantiles` [2, 3, 5, 8], `probabilities` [0.2, 0.6, 0.8, 1.0]. 중복된 값 3은 한 칸에서 0.4만큼 올라간다(0.2 → 0.6). F(3)=0.6, F(4)=0.6(계단 사이에서는 그대로), F(10)=1.0.
- **KS 통계량과의 관계(직접 확인)**: 평균이 0.5 다른 두 정규 표본(각 1,000건)의 ECDF를 모든 관측점에서 평가해 **절대 차이의 최댓값을 직접 계산**한 값 0.237이 `ks_2samp`의 통계량 0.237과 같았다. 한 번의 난수 시드 결과다([Kolmogorov-Smirnov 검정](#ks-test)).
- **쓰임**: 분포 비교, 이상치·꼬리 확인, 드리프트 감지의 KS 통계량 계산, 생존 분석(Kaplan-Meier). 분포를 가정하지 않는 요약이라는 장점이 있고, 표본이 작으면 계단이 거칠다.

## 그림으로 보기
```mermaid
flowchart LR
A["표본 [2,3,3,5,8]"] --> B["고유값 정렬 2,3,5,8"]
B --> C["각 값에서 비율 누적<br/>0.2 → 0.6 → 0.8 → 1.0"]
C --> D["계단 함수 F(x)"]
D --> E["두 표본 ECDF의 최대 차이 = KS 통계량"]
```

## 예시
```python
from scipy import stats
r = stats.ecdf(sample)
r.cdf.evaluate(3.0)      # 값이 3 이하인 관측의 비율
r.cdf.confidence_interval(0.95)
```
- 점검: 기준 기간과 현재 기간의 ECDF를 같은 그래프에 겹쳐 가장 크게 벌어지는 구간을 눈으로 확인.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| ECDF | 표본 기반 누적 비율의 계단 함수 |
| 히스토그램 | 구간별 빈도, 구간 설정에 민감 |
| [Kolmogorov-Smirnov 검정](#ks-test) | 두 ECDF의 최대 차이를 통계량으로 사용 |
| 생존 함수 sf | CDF의 여집합(1−F) |

## 더 읽을거리
- [scipy.stats.ecdf (SciPy 문서)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ecdf.html) — 정의·속성·예(열어서 확인)
