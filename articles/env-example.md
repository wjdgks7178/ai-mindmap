# env.example 견본

> `.env.example`은 실제 값을 비운 채 "이 앱에 어떤 환경 변수가 필요한지"만 적어 git에 올리는 견본 파일이다. 실제 `.env`는 올리지 않는다.

## 쉽게 말하면
서류 양식의 빈 칸 견본이다. 어떤 칸을 채워야 하는지는 모두에게 보여 주되, 채운 내용(비밀번호)은 각자 자기 서랍에만 둔다.

## 자세히
- 12-Factor App의 Config 원칙: 배포마다 달라지는 값(DB 주소, 외부 서비스 자격 증명, 호스트명)은 코드와 엄격히 분리해 환경 변수에 둔다. 판별법: "코드베이스를 지금 당장 공개해도 자격 증명이 새지 않는가?"
- 환경 변수는 실수로 저장소에 커밋될 가능성이 낮고 언어·OS에 무관하다는 것이 이유. 반면 dev/staging/prod 같은 묶음을 만들면 배포가 늘수록 조합이 폭발하므로 변수를 개별로 관리하라고 권한다.
- 견본 파일은 이 원칙을 팀에서 쓰기 위한 관례다(12-Factor 문서에 파일 이름 규정은 없음 — 일반 관례). 새 팀원은 `cp .env.example .env` 후 값만 채운다.
- 작성 요령: 변수 이름과 주석(용도·발급처)만 쓰고 값은 비우거나 `your-key-here`처럼 명백한 자리표시자로 둔다. 진짜처럼 보이는 값은 넣지 않는다. `.env`는 [.gitignore](#dotenv-gitignore)에 넣고 `.env.example`만 추적한다.
- 새 변수를 추가하면 견본도 같이 갱신해야 한다. 안 그러면 다른 사람 환경에서 앱이 조용히 실패한다.

## 그림으로 보기
```mermaid
flowchart LR
  E1[".env.example<br/>이름만, git에 올림"] --> CP["복사"]
  CP --> E2[".env<br/>실제 값, git 제외"]
  E2 --> APP["앱 실행"]
```
```mermaid
flowchart TD
  G[".gitignore"] -- "제외" --> X[".env"]
  G -- "추적" --> Y[".env.example"]
```

## 예시
```bash
# .env.example
# OpenAI 키: https://platform.openai.com 에서 발급
OPENAI_API_KEY=your-key-here
DATABASE_URL=postgres://user:pass@localhost:5432/app
```
```bash
cp .env.example .env   # 그 뒤 실제 값을 채운다
```
AI 코딩 도구로 앱을 만들 때 "필요한 환경 변수는 .env.example로 만들어 줘"라고 요청하면 키가 코드에 박히는 것을 줄인다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| `.env` | 실제 값, 절대 커밋 금지 |
| `.env.example` | 이름만, 커밋 O |
| [.gitignore](#dotenv-gitignore) | 어떤 파일을 제외할지 지정 |
| [커밋 전 스캔](#pre-commit-secret-scan) | 실수로 값이 들어갔는지 검사 |

## 더 읽을거리
- [The Twelve-Factor App: Config](https://12factor.net/config) — 설정을 환경 변수로 분리하는 원칙.
