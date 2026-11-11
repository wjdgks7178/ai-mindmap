# QLoRA

> QLoRA는 베이스 모델을 4비트로 양자화해 얼려 두고, 그 위에 LoRA 어댑터만 학습해 적은 GPU 메모리로 큰 모델을 파인튜닝하는 방법이다.

## 쉽게 말하면
두꺼운 백과사전을 압축본(4비트)으로 책상에 올려 두고, 포스트잇(LoRA)에만 메모를 쓰는 것과 같다. 책 자체는 안 바꾸니 책상이 작아도 된다.

## 자세히
Dettmers 외 *QLoRA*(arXiv 2305.14314) 초록 기준:
- 얼린 4비트 모델로 기울기를 역전파해 LoRA 어댑터에 전달한다.
- 핵심 3가지: **NF4**(정규분포 가중치에 최적이라고 주장하는 4비트 자료형), **이중 양자화**(양자화 상수까지 양자화), **paged optimizer**(메모리 급증 완화).
- 주장: 65B 모델을 48GB GPU 1장에서 파인튜닝, 16비트 전체 파인튜닝 성능 유지. Guanaco가 Vicuna 벤치마크에서 ChatGPT의 99.3%(논문 주장).
- PEFT에서: `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)`로 로드, `target_modules="all-linear"`로 모든 선형층에 붙이면 전체 파인튜닝에 근접.
- LoftQ 초기화(`init_lora_weights="loftq"`)는 양자화 오차를 줄이는 LoRA 초기화 옵션.

## 그림으로 보기
```mermaid
flowchart LR
  W["원본 모델 16비트"] --> Q["NF4로 4비트 양자화<br/>동결"]
  Q --> F["순전파"]
  L["LoRA 어댑터 16비트"] --> F
  F --> G["손실·기울기"] --> L
```

## 예시
```python
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(name, quantization_config=bnb, device_map="auto")
cfg = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")
```

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| LoRA | 베이스 16비트 |
| QLoRA | 베이스 4비트 + LoRA |
| 양자화 추론(GPTQ 등) | 추론용 압축, 학습 아님 |
| [rsLoRA](#rslora) | 스케일 방식(QLoRA와 함께 가능) |

## 더 읽을거리
- [QLoRA 논문](https://arxiv.org/abs/2305.14314) — 초록.
- [HF PEFT LoRA 가이드](https://huggingface.co/docs/peft/developer_guides/lora) — all-linear, 4비트 예시.
