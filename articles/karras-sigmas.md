# Karras sigmas

> Karras sigmas는 확산 모델 샘플링에서 "노이즈 크기(σ)를 어떤 간격으로 줄여 나갈지" 정하는 스케줄로, Karras 등(2022)이 제안했고 노이즈가 작은 구간의 단계를 촘촘하게 배치한다.

## 쉽게 말하면
조각상을 깎을 때 처음엔 큰 망치로 크게 덜어내고, 막바지엔 작은 끌로 세밀하게 다듬는다. 단계 수가 같다면 후반부 세밀 작업에 단계를 더 몰아주는 쪽이 결과가 좋다는 발상이다. 균등 간격이 아니라 "처음엔 성기게, 끝으로 갈수록 촘촘하게" 노이즈 눈금을 매긴다.

## 자세히
- 출처: *Elucidating the Design Space of Diffusion-Based Generative Models* (arXiv 2206.00364, 2022). 샘플링·학습·전처리 설계를 분리해 정리했고, 35회 네트워크 평가로 CIFAR-10 클래스 조건부 FID 1.79를 보고했다(초록 기준).
- 스케줄 공식 자체는 이번에 초록으로 확인하지 못했다. 일반적으로 알려진 형태는 σ_max~σ_min 사이를 ρ제곱근 공간에서 균등 분할하는 것(ρ=7)이다. *주장: 이는 기억에 의한 설명이며 본문 미확인.*
- diffusers v0.42.1 `EulerDiscreteScheduler`는 `use_karras_sigmas`(기본 False)로 켠다. 같은 계열의 `use_exponential_sigmas`, `use_beta_sigmas`(논문 2407.12173)도 있고, `sigma_min`/`sigma_max`로 범위를 지정한다.
- Euler 스케줄러는 보통 20~30단계에서 좋은 결과를 낸다고 문서에 적혀 있다.
- 스케줄러는 모델을 다시 학습하지 않고 추론 때 바꿀 수 있는 부품이다([diffusion-scheduler](#diffusion-scheduler)).

## 그림으로 보기
```mermaid
flowchart LR
  A["σ 큼<br/>구조 결정"] --> B["중간"] --> C["σ 작음<br/>디테일"]
```
```mermaid
flowchart TD
  U["균등 간격: 단계가 고르게 분포"] --> R["같은 단계 수"]
  K["Karras: 작은 σ 구간에 단계 집중"] --> R
```

## 예시
```python
from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler
pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
```
(일반적 사용 예, 실행 확인은 하지 않았다.) 같은 시드로 켜고 끄며 디테일 차이를 비교해 보면 감이 온다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
|---|---|
| Karras sigmas | σ를 어느 간격으로 샘플링할지(스케줄) |
| 솔버(Euler, DPM++) | 한 단계에서 어떻게 계산할지(수치해법) |
| [few-step-generation](#few-step-generation) | 증류로 단계 수 자체를 줄임 |
| exponential/beta sigmas | 다른 간격 규칙 |

## 더 읽을거리
- [Karras 등 2022 (arXiv 2206.00364)](https://arxiv.org/abs/2206.00364) — 설계 공간 논문 초록.
- [HF EulerDiscreteScheduler](https://huggingface.co/docs/diffusers/api/schedulers/euler) — `use_karras_sigmas` 옵션 문서.
