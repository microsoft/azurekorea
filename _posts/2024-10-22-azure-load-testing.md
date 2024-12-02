---
layout: post
title:  "생성형 AI 앱 성능 관리 방법: Azure Load Testing으로 부하 테스트 하기(1/2)"
author: ilkim
tag: [ Azure Load Testing, Azure OpenAI ]
category: [ Solution ]
image: assets/images/thumnails/1_gXhVHIUxmWKImculHU175Q.webp
featured: true
---
생성형 AI 앱들의 성능 지표들로 [*그라운딩(Groundedness), 관련성(Relevance), 일관성(Coherence), 유창성(Fluency), 유사성(Similarity)*](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/concept-model-monitoring-generative-ai-evaluation-metrics)과 같은 답변의 품질 요소를 매우 중요하게 이야기합니다. 그러나 프로덕션 서비스를 위해서는 기존 앱과 동일하게 AI 답변의 응답 속도(Latency) 및 처리율(Throughtput)이 매우 중요한 성능 지표로 강조되며, 이는 답변 품질에 앞서 사용자가 가장 먼저 체감하는 성능 지표이기 때문입니다.

생성형 AI 앱의 성능에 영향을 미치는 주요 요소로는 Azure OpenAI(AOAI) API 엔드포인트의 리전 위치, 입력 프롬프트의 토큰 크기와 출력 토큰 크기, 모델 크기와 버전 (*gpt-3.5-turbo, gpt-4, gpt-4 등*), 그리고 컨텍스트 및 히스토리 유지를 위한 추가 토큰 사용 등이 있으며, 이러한 요인들이 전반적인 답변 속도 및 처리율에 중대한 영향을 줍니다.

### TPM과 응답 속도

앞서 언급한 주요 성능 요소들을 잘 고려하여 불필요한 토큰 수를 줄이는 것이 응답 속도 최적화에 있어서 매우 중요하며, 추가적으로 AOAI API의 가용 TPM(Token per Minute)에 맞는 요청을 수행해야 기대하는 성능에 만족시킬 수 있습니다. TPM은 API를 호출할 때 분당 처리할 수 있는 토큰 수를 제한하는 속도 제한 기능으로 이 제한을 초과할 경우 HTTP 429 오류로 응답하며, 해당 분 동안 추가적인 요청이 지연되거나 거부되며 전반적인 서비스의 응답속도를 늦추거나 처리율을 저하시킵니다.

![img](https://cdn-images-1.medium.com/max/1200/1*gXhVHIUxmWKImculHU175Q.png)

AOAI API 요청의 429 오류 [source](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/enable-gpt-failover-with-azure-openai-and-azure-api-management/ba-p/4038233)

AOAI 모델 따라 가용 TPM이 다르지만 gpt-4o 모델을 기준으로 최대 TPM은 표준 150K/글로벌 450K로 설정할 수 있으며, EA 고객은 최대 표준 1M/글로벌 30M으로 설정 가능합니다. 일반적인 서비스 시나리오에서는 기본 TPM 값만으로 충분할 수도 있지만, RAG 기반 서비스의 경우 검색 문서의 컨텍스트 불필요하게 크게 사용할 경우 TPM은 빠르게 소비될 수 있습니다. 특히, 최근 LLM 모델들의 context windows가 과거 4, 8, 16K에서 128K로 크게 증가되면서 TPM의 과다 사용을 흔하게 볼 수 있습니다.

최근 성능 이슈로 고민하는 고객의 RAG 기반 생성형 AI 앱의 아키텍처를 리뷰 했었습니다. 이 고객은 사용자가 몰리는 시간 대에 수 초 내에 응답하는 서비스가 수십 초로 응답하는 성능 저하 현상을 이야기하였고 전사 오픈에 앞서 서비스 성능을 높이기 위해서 앱 서버의 수를 늘려야 하는지 문의를 주었습니다. 먼저 AOAI API의 사용 현황을 검토한 결과 고객은 모델 배포 시 30K TPM으로 낮은 TPM으로 설정하였고, 앱은 2K로 청크된 문서 6개(약 8~10K 정도 토큰 크기) 컨텍스트를 사용하는 것을 확인하였습니다. 이런 설정에서 대략 분당 3~5 요청을 처리할 수 있는 것으로 계산되었고, AOAI API의 사용량을 해당 시간대에 확인한 결과 비슷한 응답 속도 결과와 다수의 HTTP 429 오류가 발생한 것을 확인했습니다.

앱 성능을 위해서는 서버 수를 늘리는 것보다 먼저 동시 사용자에 대응하는 최대 TPM으로 설정하는 것을 권장하였고, 이를 좀더 정확하게 검증하기 위해서 부하테스트를 진행하여 적정한 구성을 할 수 있었습니다. 또한, 검색 성능을 개선시켜 컨텍스트 사용량을 줄이는 최적화 작업도 진행하는 것은 권장하였습니다.

### 부하 테스트와 성능 확인

앱 성능 측정하는 여러 부하 테스트 솔루션이 있지만, Azure 환경에서는 신속하고 간편하게 구성하여 부하 테스트를 수행할 수 있는 [Azure Load Testing](https://learn.microsoft.com/ko-kr/azure/load-testing/overview-what-is-azure-load-testing)을 추천합니다. Apache JMeter 기반의 매니지드 서비스로, JMeter의 복잡한 구성 없이 간단한 Curl 기반 스크립트로 쉽게 설정하고 테스트할 수 있습니다. 또한 기본적인 서버 성능 지표뿐만 아니라 관련 Azure 리소스의 주요 모니터링 지표도 함께 확인할 수 있어 전체 서비스의 성능 상태를 한눈에 파악하는 데 유용합니다.

아래는 Azure Load Testing을 통해 실시한 부하 테스트 결과 화면입니다. 이 테스트를 통해 부하가 증가할수록 응답 시간이 길어지고 전반적인 서비스 안정성이 저하되는 것을 알 수 있습니다. 또한, 예를 들어 앱 서버인 Azure Container App (CPU, 메모리, Replica 수)과 같은 관련 Azure 리소스의 주요 지표도 함께 확인할 수 있습니다. 이를 바탕으로 적정 RPM 및 앱 서버의 적절한 크기와 수를 정하여 서비스 성능과 운영 비용을 최적화할 수 있습니다.

![img](https://cdn-images-1.medium.com/max/1200/1*iHnxVL-392AXh8umbk0s2Q.png)

부하 테스트 결과 — 응답 시간, 처리율 및 오류 확인

![img](https://cdn-images-1.medium.com/max/1200/1*9SWgQ5hEo19jI5wl4d7GLQ.png)

부하 테스트 결과 — 관련 서비스(Azure Container Apps)의 성능 지표

Azure Load Testing은 간단한 스크립트뿐만 아니라 좀더 고급 기능을 사용하는 JMX 스크립트 및 JMeter 플러그인도 사용할 수 있으며, 퍼블릭으로 노출된 서비스뿐만 아니라 내부 VNET 환경도 지원됩니다. 그러나 아쉽게도 JMX 스크립트를 직접 작성하는 기능은 제공되지 않아 별도의 JMeter를 설치하여 작성해야 하고, Azure Load Testing 서비스는 한국 리전에는 아직 제공되지 않아 한국 리전의 내부 VNET 환경에서 사용하는데 제약이 있으니 참고하시기 바랍니다.

마지막으로, 앱의 성능 저하 현상은 부하 테스트로 확인할 수 있으나, 구체적인 원인을 파악하기는 어렵습니다. 앱 내부의 성능 저하 원인을 분석하기 위해서는 APM (Application Performance Monitoring) 솔루션이 필요합니다. 다음에는 부하 테스트와 함께 사용할 때 효과적인 Azure의 대표적인 APM 솔루션인 [Azure Application Insight](https://learn.microsoft.com/ko-kr/azure/azure-monitor/app/app-insights-overview)과 End-to-end 분산 트래이스 기능을 이용하여 성능 저하의 원인 분석 방법에 대해서 소개하겠습니다.