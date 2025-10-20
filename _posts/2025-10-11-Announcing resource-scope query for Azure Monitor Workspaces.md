---
layout: post
title:  "Azure Monitor 작업 영역을 위한 리소스 범위 쿼리"
author: jyseong
tag: [ application insights, azure managed grafana, azure monitor, azure monitor managed service for prometheus, opentelemetry, updates ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-11-Announcing resource-scope query for Azure Monitor Workspaces/blog post resource 4.png
---

### 작성자 : [Tyler_Kight](https://techcommunity.microsoft.com/users/tyler_kight/818335)
### 원본 : [Announcing resource-scope query for Azure Monitor Workspaces](https://techcommunity.microsoft.com/blog/azureobservabilityblog/announcing-resource-scope-query-for-azure-monitor-workspaces/4460567)

**Azure Monitor 작업 영역(Azure Monitor Workspaces, AMW)** 에서 **리소스 범위 쿼리**의 공개 미리보기를 시작합니다. 이 기능은 모니터링을 더 단순화하고, 액세스 제어를 강화하며, Azure 환경과의 일관성을 강화해 줍니다.

이 새로운 기능은 **Log Analytics 작업 영역(Log Analytics Workspaces, LAW)** 에서 성공적으로 도입된 리소스 범위 쿼리를 기반으로 합니다. LAW에서는 로그 접근을 Azure 리소스 범위와 연계해 혁신했습니다. 이제 해당 기능의 강력함과 유연성을 AMW 메트릭에서도 활용할 수 있습니다.

## 리소스 범위 쿼리란 무엇인가요?
[리소스 범위 쿼리](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/azure-monitor-workspace-manage-access)는 그 동안 많이 요청된 기능으로, 사용자가 메트릭이 저장된 AMW(작업 영역)를 알 필요 없이 특정 리소스, 리소스 그룹, 또는 구독 범위에서 메트릭을 조회할 수 있도록 해줍니다. 즉,

- **더 간단한 쿼리:** 메트릭이 어디에 저장되어 있는지 몰라도, 사용자는 하나 이상의 리소스 컨텍스트를 직접 지정해 쿼리할 수 있습니다.
- **세분화된 Azure RBAC 제어:** AMW가 리소스 중심 액세스 모드로 설정된 경우, 권한 검사는 작업 영역 자체가 아니라 사용자가 쿼리하는 리소스에 대해 수행됩니다. 이는 현재 [LAW](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/manage-access?tabs=portal)에서 작동하는 방식과 동일하며, 최소 권한 원칙을 준수하는 보안 모범 사례를 지원합니다.

## 왜 리소스 중심 쿼리를 사용해야 할까요?
기존의 AMW 쿼리 방식에서는 사용자가 다음과 같은 작업을 해야만 했습니다:

- 메트릭이 저장된 정확한 AMW를 알아야 함
- 해당 AMW에 대한 액세스 권한을 보유해야 함
- 리소스 컨텍스트에서 벗어나 메트릭을 쿼리해야 함

이로 인해, 알림에 대응하는 DevOps 팀이나 온콜 엔지니어는 어떤 AMW를 쿼리해야 하는지 알기 어려워 불편함이 있었습니다.

리소스 중심 쿼리를 사용하면:

- 사용자는 **리소스의 Metrics 블레이드**에서 직접 메트릭을 쿼리할 수 있습니다.
- **최소 권한 원칙**이 적용되어, 사용자는 쿼리하려는 리소스에 대한 권한만 있으면 됩니다.
- 중앙 팀은 AMW에 대한 제어를 유지하면서, 애플리케이션 팀이 자체 모니터링을 할 수 있도록 지원할 수 있습니다.

## 어떻게 동작하나요?
**Azure Monitor Agent**를 통해 수집된 모든 메트릭에는 Microsoft.resourceid, Microsoft.subscriptionid, Microsoft.resourcegroupname과 같은 차원이 자동으로 추가되어 이 기능을 지원합니다. 이러한 차원의 추가는 최종 사용자에게 비용 영향을 주지 않습니다.

**리소스 중심 쿼리**는 다음과 같이 새로운 엔드포인트를 사용합니다:

```
https://query.<region>.prometheus.monitor.azure.com
```

쿼리는 필요에 따라 어떤 지역에서든 재라우팅되지만, 최적의 성능을 위해 AMW와 가장 가까운 엔드포인트를 선택하는 것을 권장합니다.

사용자는 다음과 같은 도구들을 통해 쿼리할 수 있습니다:

- **Azure Portal PromQL Editor**
- **Grafana 대시보드 ([데이터 원본 구성](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/azure-monitor-workspace-manage-access) 포함)**
- **쿼리 기반 메트릭 알림**
- **Azure Monitor 솔루션** (예: Container Insights, App Insights – OTel 메트릭을 AMW 데이터 소스로 사용할 때)
- **Prometheus HTTP API**

프로그래밍 방식으로 쿼리할 때는 HTTP 헤더를 추가합니다:
```
x-ms-azure-scoping: <ARM Resource ID>
```

다음과 같은 범위들이 지원됩니다:

- 개별 리소스
- 리소스 그룹
- 구독

현재는 단일 리소스 수준에서만 스코핑이 지원되지만, 쉼표로 구분된 다중 리소스 스코핑은 2025년 말에 추가될 예정입니다.

## 누가 이 기능의 혜택을 받을까요?

- **애플리케이션 팀:** AMW 접근 권한 없이도 자신들의 리소스 메트릭을 바로 조회할 수 있습니다.
- **중앙 모니터링 팀:** AMW에 대한 제어는 유지하면서, 앱 팀에는 보안이 강화된 제한적 접근 권한을 제공합니다.
- **DevOps 엔지니어:** 알림에 대응하거나 특정 리소스를 문제 해결할 때, 어떤 AMW에 메트릭이 있는지 몰라도 바로 작업할 수 있습니다.
- **Grafana 사용자:** AMW를 지정할 필요 없이, 구독이나 리소스 그룹 범위에 동적 변수를 적용해 대시보드를 쉽게 구성할 수 있습니다.


## 언제부터 사용할 수 있나요?

- *Microsoft. dimension* 스탬핑은 이미 완료되어 모든 AMW에서 적용 중입니다.
- 리소스 중심 쿼리 엔드포인트의 **공개 미리보기**는 **2025년 10월 10일**에 시작됩니다.
- 해당 날짜 이후 **새로 생성되는 모든 AMW**는 기본적으로 **리소스 컨텍스트 액세스 모드(resource-context access mode)** 로 설정됩니다.

## AMW의 "액세스 제어 모드"란 무엇인가요?
*액세스 제어 모드*는 각 작업 영역에서 권한이 어떻게 결정되는지를 정의하는 설정입니다.

1. **작업 영역 권한 필요 (Require workspace permissions)**
이 모드에서는 세분화된 Azure RBAC(리소스 수준 권한)를 지원하지 않습니다.
작업 영역에 접근하려면 반드시 해당 작업 영역 권한이 있어야 합니다.

쿼리 범위를 작업 영역으로 지정하면, 작업 영역 권한이 적용됩니다.
쿼리 범위를 리소스로 지정하면, 작업 영역 권한과 리소스 권한이 모두 확인됩니다.

이 설정은 2025년 10월 이전에 생성된 작업 영역의 기본값입니다.

2. **리소스 또는 작업 영역 권한 사용 (Use resource or workspace permissions)**
이 모드는 세분화된 Azure RBAC를 지원합니다.
사용자는 자신이 접근 권한을 가진 리소스와 관련된 데이터만 볼 수 있습니다.

쿼리 범위를 작업 영역으로 지정하면, 작업 영역 권한이 적용됩니다.
쿼리 범위를 리소스로 지정하면, 리소스 권한만 확인되고 작업 영역 권한은 무시됩니다.

이 설정은 2025년 10월 이후에 생성되는 작업 영역의 기본값입니다.

👉 [작업 영역의 제어 모드를 변경하는 방법](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/azure-monitor-workspace-manage-access)은 링크를 참고하시기 바랍니다.

## 마무리 
리소스 중심 쿼리는 AMW를 Azure 네이티브 경험과 일치시켜, 보안성, 확장성, 직관적인 가시성을 제공합니다. 수천 개의 VM을 관리하거나, AKS 클러스터를 배포하거나, OpenTelemetry를 활용해 커스텀 앱을 구축하는 경우에도 이 기능을 통해 AMW를 먼저 쿼리하고 필터링할 필요 없이, 워크로드나 리소스의 컨텍스트에서 바로 모니터링할 수 있습니다.

시작 방법:
- 2025년 10월 10일 이후에는 리소스의 Metrics 블레이드로 이동하거나, Grafana 데이터 소스를 새 쿼리 엔드포인트로 설정하면 됩니다.

----------

- 2025년 10월 10일 업데이트 됨.
- 2025년 10월 11일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))