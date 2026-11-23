# PEFT 라이브러리

> Hugging Face의 **파라미터 효율 미세조정(PEFT)** 도구 모음이다. LoRA 같은 방법을 몇 줄로 기존 모델에 붙인다.

## 쉽게 말하면
거대한 모델 전체를 개조하는 대신 "부착형 부품"만 갈아 끼우는 공구함이다. 공구함이 있으면 LoRA를 직접 구현하지 않아도 된다.

## 자세히
(Hugging Face PEFT의 LoRA 개념 가이드를 직접 읽었다. 설치·지원 방법 전체 목록은 읽지 못했다.)
- **기본 흐름(문서)**: ① 기본 모델 생성 ② `LoraConfig` 만들기 ③ `get_peft_model()`로 감싸기 ④ `PeftModel`을 기본 모델처럼 학습.
- **주요 `LoraConfig` 인자(문서)**: `r`(랭크), `target_modules`(LoRA를 붙일 모듈), `lora_alpha`(스케일 인자), `bias`('none'/'all'/'lora_only'), `use_rslora`, `modules_to_save`(함께 학습·저장할 비LoRA 모듈, 예: 새 분류 헤드), `layers_to_transform`·`layers_pattern`, `rank_pattern`·`alpha_pattern`(층별 덮어쓰기).
- **초기화(문서)**: 기본은 A에 Kaiming-uniform, B에 0(시작 시 항등 변환). `init_lora_weights="gaussian"`, 양자화 기본 모델(QLoRA)용 `"loftq"`.
- **유틸(문서)**: `merge_and_unload`, `merge_adapter`, `unmerge_adapter`, `unload`, `delete_adapter`, `add_weighted_adapter`([병합](#lora-merge) 참고).
- **변형(문서)**: DoRA, KaSA, MonteCLoRA, VeLoRA가 변형 페이지로 나열된다. 이 글은 내용을 읽지 않았다. DoRA는 보통 `use_dora=True`(문서 외 일반 지식).

## 그림으로 보기
```mermaid
flowchart LR
  M["기본 모델"] --> C["LoraConfig"]
  C --> G["get_peft_model"]
  G --> T["PeftModel 학습"]
  T --> S["어댑터만 저장"]
```

## 예시
```python
from peft import LoraConfig, get_peft_model
cfg = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj","v_proj"], bias="none")
model = get_peft_model(base_model, cfg)
```

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| PEFT | 파라미터 효율 미세조정 도구 모음 |
| [LoRA](#lora-adapters) | PEFT가 지원하는 방법의 하나 |
| 완전 미세조정 | 모든 가중치 갱신 |

## 더 읽을거리
- [Hugging Face PEFT — LoRA 개념 가이드](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) — 직접 읽음.
