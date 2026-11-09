# 생성 루프 (텍스트 퇴화, Degeneration)

> 모델이 같은 구절이나 문장을 끝없이 되풀이하는 현상으로, 디코딩 방식뿐 아니라 모델·학습 자체에도 원인이 있다고 논의된다.

## 쉽게 말하면
고장 난 레코드가 같은 소절만 반복하는 것과 같다. 한 번 나온 표현이 다음 표현의 "가장 그럴듯한 후보"가 되고, 그 반복이 다시 다음 반복의 근거가 되면서 빠져나오지 못한다.

## 자세히
Hugging Face 블로그(2026-11 확인):
- greedy·beam search는 반복에 빠지기 쉽다. 글은 이것이 디코딩보다 **모델과 학습에서 비롯되는 부분이 크다**는 근거를 인용한다(주장 수준).
- Holtzman 외: 사람이 쓴 고품질 글은 "가장 확률 높은 다음 단어"를 따르는 분포가 아니다 → 확률 최대화만 하면 퇴화한다.
- top-K·top-p 샘플링도 반복이 생길 수 있다.
- 완화책: `no_repeat_ngram_size=2`(같은 n-gram 재등장 금지, "New York" 같은 이름이 한 번만 나오는 부작용 주의), 샘플링(temperature·top-p), [반복 페널티](#repetition-penalty), [빈도·존재 페널티](#frequency-presence-penalty), [대조 탐색](#contrastive-search).
- 에이전트 맥락(일반 관행): 도구 호출 실패를 무한 재시도하는 루프도 비슷한 "퇴화"지만 원인은 다르며, 최대 반복 횟수·종료 조건으로 막는다.

## 그림으로 보기
```mermaid
flowchart LR
  A["구절이 한 번 나옴"] --> B["다음 토큰 후보 중<br/>반복이 가장 그럴듯"]
  B --> C["같은 구절 재생성"]
  C --> B
  C -.-> X["완화: 페널티·샘플링·대조 탐색"]
```

## 예시
로컬 모델이 "그리고 그리고 그리고…"로 끝나지 않음 → temperature·top-p 적용, 반복 페널티 1.1~1.2 시도, `max_new_tokens`로 상한.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| 생성 루프 | 텍스트가 같은 구절을 반복 |
| 에이전트 무한 루프 | 행동 단위의 반복 — 종료 조건 설계 문제 |
| [환각](#hallucination) | 사실과 다른 내용 — 반복과 별개 |

## 더 읽을거리
- [How to generate text (Hugging Face)](https://huggingface.co/blog/how-to-generate) — 반복의 원인과 n-gram 제한.
- [Contrastive search (Hugging Face)](https://huggingface.co/blog/introducing-csearch) — 반복을 줄이는 디코딩.
