# SHAP 사유 코드

> 각 입력 변수가 한 신청자의 점수를 얼마나 밀어 올리거나 내렸는지(SHAP 기여도)를 계산해, 그 순위로 대출 거절의 사유 코드를 만드는 방법.

## 쉽게 말하면
시험 총점이 70점일 때 "수학 +10, 영어 −15, 국어 −5"처럼 과목별 기여를 보여 주는 성적 분해표와 같다. 가장 점수를 깎은 과목 2~3개를 "주된 이유"로 적으면 거절 통지서의 이유가 된다.

## 자세히
- **SHAP**: 게임이론의 Shapley 값을 이용해 예측값을 변수별 기여의 합으로 나눈다. 트리 모델(GBM)에는 shap 라이브러리의 TreeExplainer로 빠르게 계산한다.
- **절차**: 기준 집단 대비 부정적 기여가 큰 변수 상위 m개(예: 3개) → 변수를 [ECOA·Reg B](#ecoa-reg-b)식 이유 문구로 매핑 → 통지.
- **조건과 한계(검색한 업체·특허·예제 코드 기준, 근거 약함)**:
  - 단조 제약(monotonic)·상호작용 제약을 걸고 학습해야 기여가 이해 가능하다는 주장. 2022년 Shapley 연구는 단조 제약이 Shapley 값도 단조로 만든다고 하면서 동시에 의존도에선 성립하지 않는다고도 적어, 원 논문 확인이 필요하다.
  - 변수 간 상호작용이 크면 효과를 단순 합으로 설명하기 어렵다.
  - 변수 단위 이유는 실제 통지문(여러 변수를 하나의 이유로 묶음)과 다를 수 있다. 특허는 그룹 단위 PDP와 SHAP을 함께 쓰는 방식을 제안한다.
- 대안: B-Shap(2022 arXiv)은 두 지점 사이의 부도 확률 변화를 모델 무관하게 분해.

## 그림으로 보기
```mermaid
flowchart LR
  A["신청자 입력"] --> B["GBM 점수"]
  B --> C["SHAP 기여도 계산"]
  C --> D["부정 기여 상위 m개"]
  D --> E["이유 문구 매핑"]
  E --> F["거절 통지서"]
```

## 예시
신청자 A의 SHAP: 최근 연체 −0.8, 카드 사용률 −0.5, 소득 +0.3 → 통지 이유 "최근 연체 이력", "신용카드 사용 비율".
같은 점수라도 기준 집단이 다르면 이유가 바뀔 수 있어 기준을 문서화한다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
| --- | --- |
| SHAP | 사후 기여도 계산, 블랙박스에 적용 |
| [해석 가능한 신용 모델](#interpretable-credit-models) | 처음부터 구조가 이해 가능 |
| [설명 가능성](#explainability) | 상위 개념 |
| 반사실 설명 | "무엇을 바꾸면 승인?" 형식, SHAP은 기여 형식 |

## 더 읽을거리
- [Explaining Adverse Actions in Credit Decisions Using Shapley Decomposition (arXiv 2204.12365)](https://arxiv.org/pdf/2204.12365) — B-Shap 제안(검색 요약 확인)
- [Provenir: Constraining ML Credit Decision Models](https://www.provenir.com/blog-constraining-machine-learning-credit-decision-models/) — 단조·상호작용 제약(업체 블로그)
- [adverse_action_explainer (GitHub)](https://github.com/rehmaanvhr-code/adverse_action_explainer) — SHAP→Reg B 이유 매핑 예제(합성 데이터)
