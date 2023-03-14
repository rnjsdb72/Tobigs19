## An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale

### Abstract

- NLP에서 transformer가 표준이 되었다.

- CV에서도 attention이 CNN을 연결하는 것에 자주 사용된다.

- CNN에 의존하지 않고서도 image patch의 sequence에 직접적으로 transformer를 적용함으로써 이미지 분류를 잘 수행할 수 있다.

- ViT는 학습에 더 적은 자원을 사용하고서도 훌륭한 결과 도출

### Introduction

- self attention 기반 아키텍처가 NLP에서 주류 모델이 되었다.
  
  - 주로 커다란 corpus로 pre-train 후 task에 알맞는 dataset으로 fine-tuning
  
  - Transformer의 계산 효율성 덕분에, 전례없는 크기의 모델을 학습할 수 있다.
    
    - 100B parameters
  
  - 그렇기 때문에 데이터셋이 계속하여 커져도, 성능 포화의 징후가 없다.

- 하지만, CV에서는 합성곱 신경망 구조가 지배적이다.
  
  - NLP의 성공에서 영감을 받아 self-attention을 CNN에 결합하려는 시도 등장
  
  - 이후에 등장한 모델들은 이론적으로는 효율적이지만, 특화된 attention pattern을 사용하기 때문에 최신 하드웨어 가속기에서 아직 효과적으로 확장되지 않았음
    
    - 그렇기 때문에 아직도 ResNet기반 모델들이 SOTA

- 해당 연구에서는 Transformer를 직접적으로 이미지에 적용하고자 함
  
  - image를 여러 개의 patch로 나누고 이들에 linear embeddings sequence를 부여
  
  - patch가 NLP에서의 token처럼 작용

- 중간 크기의 dataset에서 강한 regularization 없이 모델을 학습하면, 일반적인 정확도를 보임
  
  - Transformer는 CNN에 존재하는 inductive bias가 부족하기 때문
    
    - translation equivariance & locality와 같은
    
    - 그래서 적은 데이터 양으로 학습되면 잘 일반화하지 못한다.

- 커다란 데이터셋을 활용하면 inductive bias를 이김
  
  - ViT는 충분한 크기로 pre-train하고 약간의 데이터로 전이학습하면 좋은 성능 보임

### Related Work

- Transformer는 NLP 여러 task에서 sota 달성
  
  - 커다란 corpora pre-train 후 각 task에 fine-tuning하는 추세
    
    - BERT, GPT

- CV에서도 각 pixel은 다른 pixel과 연관이 있기 때문에 self-attention이 필요하다.

- Transformer를 CV에 적용하고자 하는 여러 시도 존재
  
  - global이 아닌 각 query pixel의 local 이웃에 self-attention 적용
  
  - Sparse Transformers: global self-attention에 scalable approximations 적용
  
  - scale attention의 대안으로 다양한 크기의 block를 적용
    
    - 또는 극단적으로 각 axes에 적용
  
  - 해당 시도들은 유망한 결과를 가져왔지만, 효과적인 하드웨어 가속화 부분에서 개선이 필요하다.

- 기존에 $2\times2$ patch를 활용해 self-attention을 사용한 연구 존재
  
  - 하지만 해당 연구에서는 pre-train 및 더 높은 해상도의 이미지에도 적용하기 위한 방안 제안

- image GPT(iGPT): image 해상도와 color space를 줄여 Transformer 적용

### Method

- image를 고정된 크기의 patch로 나누고, 각각을 선형 임베딩하고 position embedding을 더함
  
  - 그리고 vector를 Transformer encoder에 입력
  
  - 분류를 위해 cls token 학습

#### Vision Transformer(ViT)

- Transformer는 token embedding의 1차원 sequence vector를 입력받는다.

- patch embedding
  
  - 2차원 image를 다루기 위해, 이미지를 2차원 patch로 flatten한다.
    
    - $x \in \R^{H\times W\times C} \rarr x_p \in \R^{N\times (P^2\cdot C)}$
      
      - $N = \frac{HW}{P^2}$: patch 개수
      
      - $H,W,C,P$: 높이, 넓이, 채널, 패치 크기
    
    - patch를 flatten해서 $D$ 차원 벡터로 linear projection
      
      - $D$: constant latent vector

- cls token
  
  - $z_0^0 = x_{class}$: 학습가능한 embedding 추가
  - Transformer Encoder의 output $z_L^0$은 image representation $y$ 제공
  - cls head
    - pre-train 시에는 1개의 은닉층을 갖는 MLP 사용
    - fine-tuning 시에는 단일 선형 레이어 사용

- position embedding은 patch embedding에 더함
  
  - 학습가능한 1차원 position embedding tkdyd
  - 2차원을 사용해도 성능 향상 보지 못함

- Trasformer Encoder
  
  - $z_0 = [x_{class}; x_p^1 E; x_p^2E; \cdots ; x_p^NE]+E_{pos}$
    - $E \in \R^{(P^2\cdot C)\times D}, E_{pos} \in \R^{(N+1)\times D}$
  - $z_l'=MSA(LN(z_{l-1}))+z_{l-1}$
  - $z_l = MLP(LN(z_l'))+z_l'$
    - $l = 1, \dots, L$
  - $y = LN(z_L^0)$

- **inductive bias**
  
  - ViT는 CNN보다 이미지 inductive bias가 적다.
  
  - CNN은 모든 층에 locality, 2차원 neighborhood 구조, translation equivariance 보유
  
  - ViT는 MLP에 local, translation equivariance 보유
    
    - self-attention은 global
    
    - 2차원 neighborhood 구조는 매우 드물게 사용
      
      - 이미지를 patch로 나눌 때
      
      - fine-tuning 시, 이미지 해상도가 다르다면 이를 조정할 때
  
  - 학습 초기에 position embedding과 공간 관계에 대한 정보가 없다는 단점 보유

- **Hybrid Architecture**
  
  - patch embedding projection $E$를 CNN feature map을 통해 추출
  
  - patch가 $1\times1$ 크기를 갖는다면, 차원을 평평하게 하고 트랜스포머 차원으로 투영하는 것만으로 얻어짐

### 궁금한 것

- translation equivariance
  
  - translation invariance: 한 개의 그림에서 object의 위치가 변화하여도 같은 object라고 분류해야하는 것
  
  - 하지만 CNN 네트워크 자체는 filter로 연산할 때 특정 feature의 위치가 바뀌면 output에서 해당 feature에 대한 연산결과의 위치도 바뀐다.
    
    - **= translation equivariance**
  
  - 하지만 max pooling, weight sharing&learn local features, softmax 로 인해 translation invariance한 특징 보유

- inductive bias
  
  - 일반화 성능을 높이기 위해 만약의 상황에 대한 추가적인 가정을 부여하는 것
  
  - 학습 데이터 이외의 데이터들까지도 정확한 출력에 가까워지도록 하기위해 추가적인 가정
    
    - 따라서, 보지 못한 데이터에 대해서도 추론이 가능하도록 하는 가정의 집합
