---
layout: post
title:  "OpenAI o1 : Azure에서의 새로운 추론 모델의 시작"
author: junginlee
tag: [ Artificial Intelligence ]
category: [ Solution ]
image: assets/images/thumnails/0_JKw8r1AuSAw9Qv8r.gif
featured: true
---

*본 글은 [Introducing o1: OpenAI’s new reasoning model series for developers and enterprises on Azure](https://azure.microsoft.com/en-us/blog/introducing-o1-openais-new-reasoning-model-series-for-developers-and-enterprises-on-azure/) 의 많은 내용을 참고하여 씌여졌습니다.*

9/12일 OpenAI의 o1-preview 모델 및 o1-mini 모델이 OpenAI를 통해 출시 되었고, 거의 동시에 Azure 위에서도 Azure OpenAI Service, Azure AI Studio 그리고 Github을 통해 사용할 수 있게 되었습니다. 이는 OpenAI 와 마이크로소프트 간의 긴밀한 협업과 파트너십을 보여주는 단적인 예 입니다.

o1 시리즈는 기존 모델들 대비 복잡한 코딩, 추론, 여러 복잡한 비교 분석을 더욱더 잘하게 하는데 초점이 맞춰져 있고, AI 기반 애플리케이션들을 위한 한 차원 높은 기준을 바라보게 한 것 같습니다.

아래 동영상을 보시면, 맞춤법은 물론 일반 사람이 읽기에도 쉽지 않은 (garbled) 한국어 문장을 어떻게 o1-preview 모델이 고쳐 나가고, 추론해 나가는지를 데모로 재미있게 보여주고 있습니다.

마치 사람이 무언가 복잡한 일을 해내야 할 때 일의 순서를 생각하 듯이 똑같이 순서를 생각하고, 차근차근 생각하고, 처리해 나가는 것이죠. 예를 들어 이 동영상에서는 Decoding -> Deciphering -> Enhancing -> Translating 등의 과정을 15초에 걸쳐서 이뤄 냅니다.

이전 모델 보다는 Latency가 오래 걸리긴 하지만, 일의 순서를 정의하고, 수행하고, 검증하고, 생각하고 하는 것들을 반복하여 훨씬 높은 정확도를 보여주게 되는 것이죠.

[![Video Label](http://img.youtube.com/vi/eZDmDn6Iq9Y/0.jpg)](https://youtu.be/eZDmDn6Iq9Y)

자, 이제 Azure로 조금 이야기를 옮겨 보겠습니다.

Azure AI Studio playground 와 Github Models을 통해 새로운 모델들을 사용해 볼 수 있습니다. 현재는 Preview 형태이기 때문에 신청이 필요한데요. [Azure AI Studio](https://ai.azure.com/) 의 모델 카탈로그를 통해 Access를 신청하셔야 합니다.

![img](https://cdn-images-1.medium.com/max/1200/0*JKw8r1AuSAw9Qv8r.gif)
![img](https://cdn-images-1.medium.com/max/1200/1*SRp219V2oDNLTub5_06zCQ.png)

### **Azure의 모델 라인업 정리**

전체 Azure Open AI Service에서의 [모델 라인업](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)에서 o1-preview 및 o1-mini의 포지션을 더 잘 이해하기 위해 아래와 같이 정리했습니다.

- o1-preview: 고급 추론과 수학 및 과학 작업을 포함한 복잡한 문제 해결에 중점을 둡니다. 심층적인 상황 이해와 에이전트 워크플로가 필요한 응용 프로그램에 적합합니다.
- o1-mini: o1-preview보다 작고 빠르며 80% 저렴하며 코드 생성 및 작은 컨텍스트 작업에서 우수한 성능을 발휘합니다.
- GPT-4o: 텍스트와 이미지 처리 모두에서 탁월한 다용도 멀티모달 모델로, 다국어 및 비전 작업에서 우수한 성능을 발휘합니다. 향상된 정확도와 다국어 기능이 필요한 응용 분야에 적합합니다. 또한 이 모델은 일관되고 잘 정의된 데이터 형식을 위한 JSON 구조화된 출력을 제공하여 사후 처리 필요성을 줄이고 애플리케이션 효율성을 개선합니다. 최소한의 비용으로 빠르고 안정적인 텍스트 응답이 필요한 실시간 애플리케이션을 위해 설계되었습니다.
- GPT-4o Mini: 리소스가 제한적이거나 비용 제약이 높은 환경에 최적화된 GPT-4o의 더 작고 비용 효율적인 버전입니다. 텍스트 및 이미지 처리 기능을 유지하여 경량 응용 프로그램에 이상적입니다.
- DALL-E: 텍스트 프롬프트에서 안전하게 이미지를 생성하여 창의적인 콘텐츠 및 마케팅에 이상적입니다.
- Whisper: 음성을 텍스트로 전사하고 번역하여 실시간 번역 및 다국어 기반의 커뮤니케이션에 적합합니다.

### 마지막으로

전 세계적으로 60,000 개 이상의 고객이 이미 OpenAI 모델을 Azure를 통해 사용하고 있습니다. 또한, 이러한 Scale의 AI 를 제공하기 위한 엔터프라이즈급보안, 데이터 컴플라이언스, 글로벌 Region 에 대한 최대 가용성, 전용 Capacity 등 고객의 목소리를 반영하고 산업을 리딩하고 있습니다. Azure를 통해 모든 사람과 조직이 소외됨 없이 이러한 Cutting-Edge 기술 발전의 혜택을 누릴 수 있는 기회를 갖기를 소망합니다.