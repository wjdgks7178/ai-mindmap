# 바서슈타인 거리

> 바서슈타인 거리(Earth Mover's Distance)는 한 확률분포를 다른 분포 모양으로 "옮기는 데 드는 최소 비용"으로 재는 거리다. 두 분포가 겹치지 않아도 얼마나 먼지 알려 주므로 GAN 학습을 안정시키는 WGAN에 쓰인다.

## 쉽게 말하면
흙더미(분포 P)를 다른 자리의 흙더미(분포 Q) 모양으로 옮기는 일이라고 생각한다. "흙의 양 × 옮긴 거리"의 합이 가장 작은 옮기기 계획의 비용이 바서슈타인 거리다. 두 더미가 멀리 떨어져 있어도 "얼마나 멀다"는 숫자가 나오고, 가까워지면 그 숫자가 부드럽게 줄어든다.

## 자세히
- 정의: `W(p_r, p_g) = inf_{γ∈Π(p_r,p_g)} E_{(x,y)~γ}[‖x−y‖]` — 모든 "옮기기 계획" γ 중 최소 비용.
- 예: P는 0, Q는 θ에 놓인 점 분포라면 W = |θ|로 θ에 대해 매끄럽다. 같은 상황에서 JS는 θ≠0이면 log 2로 상수다.
- 직접 계산은 어렵다. **Kantorovich-Rubinstein 쌍대식**: `W = (1/K) sup_{‖f‖_L ≤ K} E_{p_r}[f(x)] − E_{p_g}[f(x)]` — K-립시츠 함수 f를 찾는 문제로 바뀐다.
- **WGAN**: 판별자를 확률 대신 점수를 내는 "critic"으로 바꾸고 로그 없이 `E[f(진짜)] − E[f(가짜)]`를 최대화한다. 립시츠 조건은 가중치를 [−c, c](예: ±0.01)로 자르는 weight clipping으로 맞췄고, 옵티마이저는 Adam 대신 RMSProp을 권장했다.
- 한계: 저자들 스스로 weight clipping을 "clearly terrible way"라 했다. 창이 크면 수렴이 느리고 작으면 기울기가 사라진다. 후속(Gulrajani 외 2017)이 **gradient penalty**로 대체했다(이번 조사에서 식은 확인하지 않음).
- 다른 쓰임: 최적 수송(optimal transport), 분포 이동 측정 등.

## 그림으로 보기
```mermaid
flowchart LR
  P["분포 P<br/>흙더미 A"] -->|"옮기는 계획 γ<br/>비용 = 양×거리"| Q["분포 Q<br/>흙더미 B"]
  Q --> W["W = 최소 비용"]
  W --> C["critic f 로 근사<br/>립시츠 제약"]
```

## 예시
```python
# WGAN critic 단계 (개념 코드)
loss_c = -(critic(real).mean() - critic(fake.detach()).mean())
for p in critic.parameters(): p.data.clamp_(-0.01, 0.01)   # weight clipping
```
요즘은 clipping 대신 gradient penalty(WGAN-GP)를 쓰는 구현이 많다.

## 헷갈리는 것과 비교
| 개념 | 차이 |
| --- | --- |
| 바서슈타인 | 옮기는 비용, 안 겹쳐도 의미 있음 |
| [JS 발산](#gan-js-divergence) | 안 겹치면 상수 |
| [KL 발산](#kl-divergence) | 비대칭, 지지집합 밖에서 무한대 |
| [flow matching](#flow-matching) | 수송 개념과 가깝지만 다른 학습법 |

## 더 읽을거리
- [From GAN to WGAN (Lilian Weng)](https://lilianweng.github.io/posts/2017-08-20-gan/) — 쌍대식, WGAN, weight clipping의 한계
