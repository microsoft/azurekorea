---
layout: post
title:  "Microsoft Agent Framework 소개"
author: jyseong
tag: [ Microsoft Agent Framework ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-17-Introducing the Microsoft Agent Framework/AgentFramework.png
---

### 작성자 : [Lee_Stott](https://techcommunity.microsoft.com/users/lee_stott/210546)
### 원본 : [Introducing the Microsoft Agent Framework](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/introducing-the-microsoft-agent-framework/4458377)

## Microsoft Agent Framework 소개: AI 에이전트와 워크플로우를 위한 통합 기반

AI 개발 환경은 빠르게 진화하고 있으며, Microsoft는 개발자가 지능형 멀티 에이전트 시스템을 쉽고 정밀하게 구축할 수 있도록 돕는 오픈 소스 SDK, [Microsoft Agent Framework](https://aka.ms/AgentFramework)를 공개했습니다. 이 프레임워크는 .NET과 Python 모두에서 사용할 수 있으며, Semantic Kernel과 AutoGen의 장점을 결합하고, 에이전트 오케스트레이션과 워크플로 설계를 위한 강력한 신규 기능을 제공합니다.

[Introducing Microsoft Agent Framework: The Open-Source Engine for Agentic AI Apps | Azure AI Foundry Blog](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)

[Introducing Microsoft Agent Framework | Microsoft Azure Blog](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)

## 왜 새로운 에이전트 프레임워크가 필요한가?
Semantic Kernel과 AutoGen은 모두 에이전트 기반 개발을 선도해왔습니다.

Semantic Kernel은 엔터프라이즈급 기능을 제공하고,
AutoGen은 연구 중심의 추상화를 제공합니다.

Microsoft Agent Framework는 이 두 가지의 **차세대 버전**으로, 동일한 팀이 강점을 결합하여 개발하였습니다. 이 프레임워크는 다음과 같은 특징을 갖습니다:

- **AutoGen의 단순함** – 멀티 에이전트 오케스트레이션을 쉽게 구현
- **Semantic Kernel의 안정성** – 스레드 기반 상태 관리, 텔레메트리, 타입 안정성 제공
- **새로운 기능** – 그래프 기반 워크플로우, 체크포인트 기능, Human-in-the-loop 지원

이는 개발자가 실험용 프로토타입과 실제 운영 환경 중 하나를 선택할 필요가 없음을 의미합니다.
Agent Framework는 단일 에이전트 프로토타입부터 복잡한 엔터프라이즈급 시스템까지 확장 가능하도록 설계되었습니다.

## 핵심 기능
### AI 에이전트
AI 에이전트는 대규모 언어 모델(LLM)을 기반으로 동작하는 지능형 프로그램입니다.
이 에이전트는 사용자가 입력한 내용을 이해하고, 그에 따라 결정을 내리며, 필요한 경우 외부 도구를 호출하거나 MCP 서버와 통신합니다. 마지막으로, 이러한 과정을 통해 적절한 응답을 생성합니다.
이들은 **Azure OpenAI**, **OpenAI**, **Azure AI** 같은 제공자를 지원하며, 다음 기능으로 확장할 수 있습니다:

- **에이전트 스레드(Agent threads)** – 상태 관리
- **컨텍스트 제공자(Context providers)** – 메모리 관리
- **미들웨어(Middleware)** – 액션 가로채기
- **MCP 클라이언트(MCP clients)** – 도구 통합

사용 사례: 고객 지원, 교육, 코드 생성, 연구 지원 등 특히 작업이 동적이고 명확히 정의되지 않은 경우에 적합합니다.

### 워크플로우
워크플로우는 그래프 기반 오케스트레이션으로, 여러 에이전트와 기능을 연결해 복잡한 다단계 작업을 수행합니다. 지원 기능은 다음과 같습니다:

- **타입 기반 라우팅(Type-based routing)**
- **조건부 로직(Conditional logic)**
- **체크포인팅(Checkpointing)**
- **Human-in-the-loop 상호작용**
- **멀티 에이전트 오케스트레이션 패턴(Multi-agent orchestration patterns)**(순차, 병렬, 핸드오프, Magentic)

워크플로우는 신뢰성과 모듈성이 필요한 구조화된 장기 프로세스에 이상적입니다.

## 개발자 경험
Agent Framework는 직관적이고 강력하게 설계되었습니다.
- **설치**:
    - Python:
        ```
        pip install agent-framework
        ```
    - .NET:
        ```
        dotnet add package Microsoft.Agents.AI
        ```

**통합:**

- 지원 SDK: Foundry SDK, MCP SDK, A2A SDK, M365 Copilot Agents
- 샘플 및 매니페스트:
    - 선언적 에이전트 매니페스트와 코드 샘플 탐색
- 학습 자료
    - [Microsoft Learn modules](https://learn.microsoft.com/training/paths/develop-ai-agents-on-azure/)
    - [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)
    - [AI Show demos](https://aka.ms/AIShow/NewAgentFramework)
    - [Azure AI Foundry Discord community](https://aka.ms/foundry/discord)

## 마이그레이션 및 호환성

현재 Semantic Kernel 또는 AutoGen을 사용 중이라면, 원활한 전환을 돕기 위한 마이그레이션 가이드가 제공됩니다.
이 프레임워크는 가능한 경우 **하위 호환성(backward-compatible)** 을 유지하도록 설계되었으며, 향후 업데이트에서도 [GitHub 저장소](https://github.com/microsoft/agent-framework)를 통해 커뮤니티 기여를 계속 지원할 예정입니다.

## 중요 고려사항

- Agent Framework는 현재 공개 미리보기(public preview) 상태입니다. 여러 분의 피드백과 이슈는 [GitHub 저장소](https://github.com/microsoft/agent-framework)에 올리실 수 있습니다. 어떠한 피드백이든 환영합니다.
- 서드파티 서버나 에이전트와 연동할 때는 데이터 공유 방식과 규정 준수 범위를 꼼꼼히 확인하세요.

Microsoft Agent Framework는 AI 개발에서 중요한 전환점을 의미합니다.
연구 혁신과 엔터프라이즈 준비성을 하나의 오픈 소스 기반으로 결합하여, 첫 번째 에이전트를 구축하든 여러 에이전트를 오케스트레이션하든, 안전하고 확장 가능하며 지능적으로 작업할 수 있는 도구를 제공합니다.

시작할 준비가 되셨나요?
[SDK를 다운로드](https://aka.ms/AgentFramework)하고, [문서](https://aka.ms/AgentFramework/Docs) 살펴보세요. 그리고 AI 에이전트의 미래를 만들어가는 커뮤니티에 참여해보시기 바랍니다.

----------

- 2025년 10월 1일 업데이트 됨.
- 2025년 10월 17일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))