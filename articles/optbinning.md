# OptBinning

> 수치형 변수를 이진·연속형·다중 클래스 타깃에 맞춰 **수리 최적화로 최적 구간화**하고, WoE·IV 표와 스코어카드까지 만들어 주는 Python 라이브러리(저자 Guillermo Navas-Palencia, 문서 기준 최신 1.0.0).

## 쉽게 말하면
키를 "작다/보통/크다"로 나눌 때 경계를 감으로 정하면 사람마다 다르다. OptBinning은 "구간마다 위험 순서가 어긋나지 않게, 구간 크기는 너무 작지 않게" 같은 규칙을 주면 가장 잘 가르는 경계를 계산해 준다.

## 자세히
출처: OptBinning 공식 문서 첫 페이지와 이진 타깃 튜토리얼(본문 확인, 2026-11-18). 설치 절차·라이선스는 읽은 페이지에 없어 확인하지 못했다.
- **문제 유형**: 이진, 연속형, 다중 클래스 타깃. 그 밖에 2D 구간화, 구간별 선형 모델(피스와이즈), 스케치 기반 배치·스트림 처리, 불확실성을 반영한 확률적 구간화, MDLP 이산화, 이상치 탐지를 문서가 소개한다.
- **방식**: 제약이 있는 수리 최적화로 구간 경계를 풀어, 단조성 같은 제약 아래 정보값(IV)을 높이는 방향으로 나눈다(문서 요약 기준 서술).
- **구간표**: `binning_table.build()`는 Bin, Count, Non-event, Event, Event rate, WoE, IV, JS를 준다. 구간 IV의 합이 Totals와 일치한다([IV](#information-value)).
- **스코어카드**: `Scorecard` 클래스가 구간화 프로세스와 추정기(로지스틱 회귀 등)를 묶는다. 반사실적 설명(counterfactual) 기능도 문서에 소개된다([스코어카드 점수화](#scorecard-points)).
- **쓰임**: 신용평가 등 설명 가능한 모형(WoE 변환 + 로지스틱 회귀)의 전처리([WoE 구간화](#woe-binning)).

## 그림으로 보기
```mermaid
flowchart LR
A["원시 변수 x와 타깃 y"] --> B["OptimalBinning.fit"]
B --> C["구간 경계 최적화"]
C --> D["binning_table<br/>WoE·IV"]
D --> E["transform: WoE 치환"]
E --> F["로지스틱 회귀"]
F --> G["Scorecard 점수표"]
```

## 예시
```python
from optbinning import OptimalBinning
optb = OptimalBinning(name="mean radius", dtype="numerical", solver="cp")
optb.fit(x, y)
print(optb.binning_table.build())
x_woe = optb.transform(x, metric="woe")
```
튜토리얼 예: `mean radius`의 가장 낮은 사건률 구간 `[16.93, inf)`는 사건률 0.008475, WoE 5.283323.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| OptBinning | 최적화 기반 구간화·스코어카드 라이브러리 |
| 동일 폭·동일 빈도 구간화 | 단순 규칙, 타깃 정보 미사용 |
| 트리 기반 구간화 | 결정 트리 분할로 구간 생성 |
| [WoE 구간화](#woe-binning) | 개념, OptBinning은 그 구현 도구 |

## 더 읽을거리
- [OptBinning 문서](https://gnpalencia.org/optbinning/) — 기능 목록과 튜토리얼 모음
- [이진 타깃 튜토리얼](https://gnpalencia.org/optbinning/tutorials/tutorial_binary.html) — 구간표 해석
- [스코어카드 튜토리얼](https://gnpalencia.org/optbinning/tutorials/tutorial_scorecard_binary_target.html) — 점수 스케일링
