# AI 개념 지도 — 루틴 운영 규칙 (Claude용)

사용자(AI 교육 설계자)가 **혼자 공부하려고** 읽는 AI 용어·개념 마인드맵이다. 입문에서 시작하지만 깊이 들어가도 된다(명령어·코드 예시 포함 가능).
사이트: GitHub Pages(`index.html`이 `data/graph.json`과 `articles/<id>.md`를 읽어 그린다). 매일 점심(12:00, 13:00 KST) 클라우드 루틴이 노드를 채우고 가지를 뻗는다.

## 데이터
- `data/graph.json` `nodes[]`: `{"id","label","parent","domain","status":"planned|done","priority":1-9,"summary","aka":[],"related":[],"added":"YYYY-MM-DD","done":"YYYY-MM-DD"}`
  - `id`: kebab-case 영문, 파일명과 같다. `domain`: 그 노드가 속한 **큰 가지(depth 1) 노드의 id**(루트는 `root`, 큰 가지 자신은 자기 id). 하위 노드는 부모의 domain을 물려받는다. 큰 가지 목록은 고정이 아니다(아래 "큰 가지 넓히기").
  - `priority`: 작을수록 먼저. 큰 가지(depth 1) = 1, 사용자가 이름을 댄 노드 = 2, 그 밖 = 3~9.
  - `related`: 다른 가지에 있는 관련 노드 id(가로 연결). 같은 부모의 형제는 넣지 않는다.
- `articles/<id>.md`: 노드 글. `status: done`인 노드만 글이 있다.
- `changelog/YYYY-MM-DD.md`: 그날 새로 정리한 노드와 새로 뻗은 가지 목록(밤 책 루틴이 읽어 책에 기사로 싣는다).

## 한 번 실행할 때
1. `python scripts/check.py stats`로 큰 가지를 점검("큰 가지 넓히기")한 뒤 `python scripts/check.py next 5` → 다음에 정리할 planned 노드(우선순위·얕은 깊이 순).
2. 노드 하나씩 끝까지: 조사 → 글 쓰기 → graph.json 갱신(`status: done`, `done` 날짜) → **새 가지 3~8개를 planned로 추가**(글에 나온 핵심 용어·하위 개념·자주 헷갈리는 짝) → `python scripts/check.py` 통과 → 커밋·push.
   - **노드 하나 끝날 때마다 커밋·push**한다. 사용량 한도에 닿아 중간에 끊겨도 끝낸 것은 남는다.
3. 그날 `changelog/YYYY-MM-DD.md`에 `- [done] <label> (<id>)`, `- [new] <label> (<id>) ← <parent label>` 줄을 덧붙인다(노드마다 같이 커밋).
4. 한도·시간까지 반복. 너무 넓게만 퍼지지 않게, 한 가지를 2~3단계 깊이까지 판 뒤 다른 가지로 간다(우선순위로 조절).

## 큰 가지 넓히기 (항상 열어 둔다)
처음 7개(리터러시·자동화·바이브코딩·LangGraph·아키텍처·방법론·멀티모달)는 사용자가 **예시로 든 출발점**일 뿐 정답이 아니다. 사용자는 AI 전체 지형을 모르므로, 빠진 큰 분야를 찾아 넓히는 것도 이 루틴의 일이다.
- 실행마다 처음에 `python scripts/check.py stats`로 큰 가지 목록을 보고, "AI 입문자가 전체 지형을 이해하려면 꼭 있어야 하는데 빠진 분야"가 있는지 따져 본다. 판단 근거: 공신력 있는 AI 입문 커리큘럼·로드맵(대학 강의, Anthropic·Google·Microsoft 등의 학습 과정, AI 리터러시 프레임워크), 그날 정리하다 기존 큰 가지 어디에도 자연스럽게 안 들어가는 개념.
- 빠진 분야가 있으면 루트(`ai`) 바로 아래에 새 큰 가지를 planned, `priority: 1`, `domain: <자기 id>`로 추가한다. 하루 최대 2개, 기존 큰 가지와 겹치면 만들지 않는다. changelog에 `- [new] <label> (<id>) ← AI`로 남긴다.
- 새 큰 가지가 생기면 기존 planned 노드 중 그쪽이 더 맞는 것은 옮겨도 된다(`parent`와 하위 전체의 `domain`을 함께 바꾸고 check 통과). done 노드는 옮기지 않고 `related`로 잇는다.
- 사이트는 큰 가지 이름·색을 graph.json에서 자동으로 만든다. index.html은 고치지 않아도 된다.

## 글 형식 (`articles/<id>.md`)
```
# <label>

> 한두 문장 정의. 처음 보는 사람이 이것만 읽어도 뜻을 안다.

## 쉽게 말하면
일상 비유 하나. 3~5문장.

## 자세히
핵심 원리·구성 요소. 짧은 문단과 목록. 숫자·버전·날짜를 적는다(AI 정보는 빨리 낡는다).

## 그림으로 보기
```mermaid 흐름도(flowchart)·순서도(sequenceDiagram)·관계도 중 내용에 맞는 것 1~2개. 라벨은 한국어, 짧게.

## 예시
실제로 쓰는 장면 1~2개(업무 예시, 프롬프트 예, 명령어나 짧은 코드).

## 헷갈리는 것과 비교
| 개념 | 차이 | 표 하나. 비슷한 노드는 [링크](#node-id)로.

## 더 읽을거리
- [제목](url) — 한 줄 설명. 실제로 열어 본 출처만. 2~5개.
```
- 다른 노드를 말할 때는 `[이름](#node-id)`로 링크한다(사이트에서 클릭하면 그 노드가 열린다). 아직 없는 개념이면 planned 노드로 만들고 링크한다.
- 분량: 600~1,500자 안팎(한국어). 길게 베끼지 말고 요약·재구성한다(인용은 한 줄 이내).
- mermaid 주의: 노드 라벨에 괄호·따옴표가 있으면 `A["라벨 (설명)"]`처럼 큰따옴표로 감싼다. 줄바꿈은 `<br/>`.
- 주장과 사실을 구분한다. 확인 못 한 내용은 "주장:"으로 적는다.

## 자료
- 웹 검색으로 잘 정리된 공식 문서·깃북·블로그·강의 자료를 찾아 1차 출처 위주로.
- 바이브코딩: 유튜브 채널 **Vibecoding University**(https://www.youtube.com/@VibecodingUniversity/videos, 사용자 추천)와 https://youtu.be/P3jFI-VpyLg 를 우선 참고. 자막이 막히면 `GEMINI_API_KEY`로 Gemini 영상 분석(ai-knowledge 저장소의 `scripts/fetch.py --gemini` 방식)을 쓰거나 영상 설명·다른 정리 글로 대신한다.
- 사용자의 AI 지식 기반 `wjdgks7178/ai-knowledge`의 `wiki/`에 이미 정리된 내용이 있으면 먼저 참고한다(`python scripts/kb.py search` — 그 저장소에서).
