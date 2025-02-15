---
layout: post
title:  "RAG 기본 파이프라인 구현: Smart Resume Matching with Azure SQL Database"
author: t-suzyvaque
tag: [APIM, Azure OpenAI, Azure Document Intelligence, RAG, Azure SQL Database, Vector Search]
category: [Solution]
image: assets/images/thumnails/suzy_basic_rag.png
---

# RAG 기본 파이프라인 구현: Smart Resume Matching with Azure SQL Database

## Overview

### RAG

RAG(Retrieval-Augmented Generation)은 외부 데이터 검색을 통해 LLM의 응답을 보완하는 방법입니다. 일반적인 LLM은 학습 데이터 내에서만 답변을 생성하지만, RAG를 통해 추가적인 검색 과정을 거쳐 최신 데이터, 맥락에 적합한 데이터를 활용할 수 있게 됩니다.

파인 튜닝(Fine Tuning)과 비교하자면, 파인 튜닝은 LLM을 특정한 도메인의 데이터로 재학습해 모델을 개선하는 방법입니다. RAG는 모델 재학습의 필요 없이 실시간으로 새로운 데이터를 활용한다는 차이점을 가집니다.

RAG는 여러 시나리오로 구현 및 활용될 수 있습니다. 본 블로그에서는 그 중 리크루팅 과정에서의 Smart Resume Matching을 구현하며 기본적인 RAG 파이프라인을 이해하고자 합니다.

### RAG Use Case: Smart Resume Matching

기업의 채용 과정에서는 수많은 지원자 중 적합한 후보를 찾는 데 많은 시간과 비용이 소요됩니다. 이를 해결하기 위해 Microsoft를 비롯한 여러 기업들은 **AI 기반 Smart Resume Matching** 시스템을 도입하고 있습니다. 이는 AI가 지원서의 내용을 분석하고, 요구 사항과의 유사도를 평가하여 적합한 지원자를 추천하는 방식입니다.

본 글은 *Microsoft Dev Blog의 Smart Resume Matching ([Smart Resume Matching: Document RAG with Azure SQL DB & Document Intelligence - Azure SQL Devs’ Corner](https://devblogs.microsoft.com/azure-sql/smart-resume-matching-with-azure-sql-db-document-intelligence/))*을 기반으로, **Azure SQL Database를 활용한 RAG**를 다룹니다. 또한 기존의 내용에 더해, **Azure OpenAI를 사용해 Sample Data**를 준비하는 과정과 **API Management를 통한 트래픽 관리** 방법까지 함께 살펴보겠습니다.

### RAG 기본 파이프라인

전반적인 흐름은 아래와 같습니다.

1. API Management 설정
2. Resume PDF Sample Data 생성 (Azure OpenAI)
3. PDF Chunking (Azure Document Intelligence)
4. Embedding 생성 (Azure OpenAI)
5. Vector 저장 및 Similarity 검색 (Azure SQL Database)
6. RAG 기반 답변 생성 (Azure OpenAI)

사용한 노트북은 *RAG_with_Resumes.ipynb ([microsoft-azure-tutorials/RAG-SQLDB-Resumes/RAG_with_Resumes.ipynb at main · suzyvaque/microsoft-azure-tutorials](https://github.com/suzyvaque/microsoft-azure-tutorials/blob/main/RAG-SQLDB-Resumes/RAG_with_Resumes.ipynb))*에서 확인 가능하며, 실행 시에는 *레포지터리 ([microsoft-azure-tutorials/RAG-SQLDB-Resumes at main · suzyvaque/microsoft-azure-tutorials](https://github.com/suzyvaque/microsoft-azure-tutorials/tree/main/RAG-SQLDB-Resumes))* 전체를 Clone하는 방법이 편리합니다.

### Prerequisites

1. **Azure Subscription**
2. **Azure Resources**: 배포해야 하는 리소스 목록은 다음과 같습니다.
    1. ***Azure OpenAI** ([방법: Azure OpenAI Service 리소스 만들기 및 배포 - Azure OpenAI | Microsoft Learn](https://learn.microsoft.com/ko-kr/azure/ai-services/openai/how-to/create-resource?pivots=web-portal))* — **Chat Completion** 모델과 **Embedding** 모델이 필요하며, ****APIM 사용을 위해 **각 모델을 최소 2개 이상의 Region에 동일한 이름으로 배포**해야 합니다.
    2. ***API Management** ([openai-apim-lb/docs/manual-setup.md at main · Azure-Samples/openai-apim-lb](https://github.com/azure-samples/openai-apim-lb/blob/main/docs/manual-setup.md)) —* 한국어 가이드는 본 블로그의 APIM 설정 항목을 참고하세요.
    3. ***Document Intelligence** ([문서 인텔리전스 리소스 만들기 - Azure AI services | Microsoft Learn](https://learn.microsoft.com/ko-kr/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0))*
    4. ***Azure SQL Database** ([무료로 배포 - Azure SQL Database | Microsoft Learn](https://learn.microsoft.com/ko-kr/azure/azure-sql/database/free-offer?view=azuresql#create-a-database))*
3. **.env 파일**: 앞서 배포한 리소스의 Endpoint와 API Key 정보를 작성해야 합니다. 노트북 내의 셀을 실행해 작성 가능합니다.
4. **Jupyter Notebook**: 코드 테스트는 Azure Machine Learning Notebook을 기준으로 합니다.
5. **Python**: 코드 테스트는 3.10.11 버전을 기준으로 합니다.

## 0️⃣ 트래픽 관리를 위한 준비 (Azure API Management)

*APIM 배포 및 Policy 설정을 위한 레퍼런스 ([openai-apim-lb/docs/manual-setup.md at main · Azure-Samples/openai-apim-lb](https://github.com/azure-samples/openai-apim-lb/blob/main/docs/manual-setup.md))*

Azure의 PaaS형 리소스를 배포하면 해당 리소스를 호출할 수 있는 Endpoint가 생성됩니다. 이때 각 리소스의 사용 Quota가 설정되어 있어, 초과 호출 시 **HTTP 429 (Too Many Requests) 오류**가 발생할 수 있습니다.

예를 들어 Azure OpenAI는 **TPM(Tokens Per Minute)**이 제한되어 있습니다. 따라서 Azure OpenAI API를 짧은 시간 내에 반복적으로 호출한다면, 허용된 토큰 사용량을 초과해 HTTP 429 오류가 발생해 원하는 결과를 얻지 못할 가능성이 있습니다.

이를 해결하기 위해 Azure API Management(APIM)를 활용할 수 있습니다. APIM에 Policy를 등록하면, 특정 리소스를 통한 요청 처리 실패 시 다른 리소스로 요청 대상을 전환하는 Failover, 트래픽을 여러 인스턴스에 분산하는 Load Balancing을 수행할 수 있습니다. 이를 통해 **RAG 파이프라인에서 API 호출 안정성을 향상하고 일정한 성능을 유지**할 수 있습니다.

### Step 1. APIM 사용을 위한 Azure OpenAI 모델 배포

모델 배포의 절차는 *가이드 ([Azure AI Foundry를 사용하여 Azure OpenAI 모델을 배포하는 방법 - Azure AI Foundry | Microsoft Learn](https://learn.microsoft.com/ko-kr/azure/ai-studio/how-to/deploy-models-openai#deploy-an-azure-openai-model-from-your-project))*에서 확인할 수 있습니다. 이때 APIM 사용을 위해서는 모델의 Location과 Deployment Name에 주의해야 합니다.

1. Resource Location
    
    
    Azure OpenAI 모델의 **Quota는 TPM(Tokens Per Minute)** 단위로 정의되며, **Subscription 및 Region마다 할당**됩니다.