# MMDiT

> MMDiT(Multimodal Diffusion Transformer)는 Stable Diffusion 3가 쓰는 확산 트랜스포머로, 이미지 토큰과 텍스트 토큰에 각각 별도 가중치를 주면서 어텐션 단계에서 둘을 하나로 합쳐 양방향으로 정보를 주고받게 한다.

## 쉽게 말하면
통역사 두 명(이미지 담당, 글 담당)이 각자 자기 언어 전용 노트를 갖고 있다가, 회의(어텐션)에서는 한 테이블에 앉아 서로 말을 주고받는 모습이다. 기존 방식은 글 쪽이 일방적으로 "이렇게 그려라"고 알려 주는 것(교차 어텐션)이었다면, MMDiT는 그림 쪽 정보도 글 쪽으로 흘러가 서로 영향을 준다.

## 자세히
- 논문: *Scaling Rectified Flow Transformers for High-Resolution Image Synthesis* (arXiv 2403.03206, 2024-03). 이미지와 텍스트에 **별도 가중치**를 쓰고, 두 토큰 사이에 **양방향 정보 흐름**을 허용한다. 저자들은 이것이 텍스트 이해·글자 표현(타이포그래피)·사람 선호도 평가를 개선했다고 보고한다.
- 구조: 이미지 잠재를 패치로 자르고([DiT](#dit-diffusion-transformer)와 같음), 텍스트는 인코더 임베딩으로 만든다. 블록 안에서 두 시퀀스를 **이어 붙여 하나의 어텐션**을 계산하고(joint attention), 나머지 MLP·정규화는 모달리티별로 따로 둔다.
- 학습은 [Flow Matching](#flow-matching) 계열(rectified flow)이다. 같은 논문에서 노이즈 샘플링을 지각적으로 중요한 구간에 몰아 주는 방식을 제안했다.
- diffusers v0.42.1 `SD3Transformer2DModel` 기본값: 패치 2, 입력 잠재 16채널, 레이어 18, 헤드 18개 × 헤드 차원 64, `joint_attention_dim` 4096, `pooled_projection_dim` 2048, `qk_norm` 옵션, `dual_attention_layers` 옵션.
- 텍스트는 두 갈래로 들어간다: 시퀀스 임베딩(`encoder_hidden_states`)은 이미지 토큰과 함께 어텐션에, 요약 벡터(`pooled_projections`)는 시간 단계와 함께 조건 주입에 쓰인다.

## 그림으로 보기
```mermaid
flowchart LR
  I["이미지 패치 토큰"] --> A["Joint Attention<br/>두 시퀀스를 이어 붙임"]
  T["텍스트 토큰"] --> A
  A --> I2["이미지 전용 MLP"]
  A --> T2["텍스트 전용 MLP"]
```
```mermaid
flowchart TD
  X["교차 어텐션 U-Net: 글 → 그림 한 방향"]
  Y["MMDiT: 글 ↔ 그림 양방향"]
```

## 예시
```python
from diffusers import StableDiffusion3Pipeline
pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers")
image = pipe("간판에 'HELLO'라고 쓰인 카페", num_inference_steps=28).images[0]
```
(일반적 사용 예이며 이번에 실행하지 않았다.) 글자가 들어간 이미지를 잘 그리는 이유를 구조로 설명할 때 쓴다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| [DiT](#dit-diffusion-transformer) | 클래스 라벨 조건의 원형. 텍스트 토큰 처리가 없다 |
| MMDiT | 텍스트·이미지 토큰 별도 가중치 + 공동 어텐션 |
| [교차 어텐션](#cross-attention-diffusion) | 텍스트가 이미지에 일방향으로 주입 |
| [U-Net](#unet-denoiser) | 합성곱 기반 구형 뼈대 |

## 더 읽을거리
- [Scaling Rectified Flow Transformers (arXiv 2403.03206)](https://arxiv.org/abs/2403.03206) — MMDiT 제안 논문 초록.
- [HF SD3Transformer2DModel](https://huggingface.co/docs/diffusers/api/models/sd3_transformer2d) — 매개변수 문서.
