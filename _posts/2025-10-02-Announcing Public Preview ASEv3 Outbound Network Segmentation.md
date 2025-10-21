---
layout: post
title:  "미리보기(공개) 발표: ASEv3 아웃바운드 네트워크 트래픽 분리 기능"
author: jyseong
tag: [ Microsoft Agent Framework ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-02-Announcing Public Preview ASEv3 Outbound Network Segmentation/asev3-outbound-network-segmentation.png
---

### 작성자 : [jordanselig](https://techcommunity.microsoft.com/users/jordanselig/1185852)
### 원본 : [Announcing Public Preview: ASEv3 Outbound Network Segmentation](https://techcommunity.microsoft.com/blog/appsonazureblog/announcing-public-preview-asev3-outbound-network-segmentation/4458398)

### App Service Environment v3(ASEv3)에서 아웃바운드 네트워크 트래픽 분리 기능의 미리보기(공개)를 발표합니다. 이 기능은 오랫동안 요구되어온 업데이트로, 격리된 환경에서 아웃바운드 트래픽을 관리할 때 더 강력한 제어, 보안, 유연성을 제공합니다.

## 🔍 아웃바운드 네트워크 트래픽 분리란 무엇인가?
아웃바운드 네트워크 트래픽 분리 기능을 사용하면 **App Service Environment v3 앱에서 나가는 트래픽의 경로를 정의하고 제어**할 수 있습니다.

즉, 이제 앱 단위에서 아웃바운드 트래픽을 구분할 수 있으며, 기업 보안 정책과 규정 준수 요구사항에 맞는 세밀한 제어가 가능합니다.

이전에는 ASEv3에서 나가는 모든 트래픽이 ASE를 호스팅하는 전체 서브넷 범위에서 처리되어, 네트워크 팀이 앱별로 제한을 적용하기 어려웠습니다.

새롭게 업데이트된 기능으로 다음과 같은 작업들이 가능해졌습니다:

- 각 앱에 대해 **아웃바운드 트래픽이 라우팅되는 서브넷 정의**
- NAT 게이트웨이를 통해 앱별 **전용 아웃바운드 IP 할당**
- **커스텀 방화벽 또는 어플라이언스**를 통한 트래픽 라우팅
- **네트워크 보안 그룹(NSG)** 을 더 정밀하게 적용
- 규제 워크로드에 대한 **감사 가능성(Auditability) 및 규정 준수(Compliance) 강화**

App Service Environment에서는 각 워커(Worker)가 서브넷에서 IP를 할당받지만, 네트워크 관점에서 특정 앱 트래픽을 라우팅하거나 차단·허용하기 위해 여러 앱/플랜의 IP를 그룹화하는 방법은 없었습니다.

아웃바운드 네트워크 트래픽 분리 기능을 사용하면 여러 앱에서 나가는 트래픽을 원하는 서브넷이나 가상 네트워크로 모아서 보낼 수 있고, 그 흐름을 직접 제어할 수 있습니다.

예를 들어, App A만 Database A와 통신할 수 있도록 하는 시나리오를 예로 들어보겠습니다.
이를 위해 App A를 **대체 서브넷(vnet-integration-subnet)** 에 연결합니다.
이 대체 서브넷은 NSG를 통해 프라이빗 엔드포인트 서브넷에 네트워크 접근 권한을 갖습니다.
즉, 가상 네트워크 통합 서브넷에서 발생하는 트래픽만 프라이빗 엔드포인트 서브넷에 도달할 수 있으며, 이를 통해 데이터베이스에 접근할 수 있습니다.

![vnet-integration-subnet](../assets/images/jyseong/images/2025-10-02-Announcing Public Preview ASEv3 Outbound Network Segmentation/vnet-integration-subnet.png)

## ✅ 퍼블릭 프리뷰에 포함된 내용
이 기능은 현재 모든 퍼블릭 Azure 지역(region)에서 사용가능 합니다.
새로운 App Service Environment를 생성 시 아래 클러스터 설정을 활성화하면, 사용이 가능합니다.
클러스터 설정은 ARM/Bicep 템플릿을 사용해 구성할 수 있습니다. 자세한 내용은 [Custom configuration settings for App Service Environments.](https://learn.microsoft.com/azure/app-service/environment/app-service-app-service-environment-custom-settings)를 참고하세요.
```json
"clusterSettings": [
        {
            "name": "MultipleSubnetJoinEnabled",
            "value": "true"  
        }
    ]
```
App Service Environment가 생성되고 이 클러스터 설정이 활성화되면, 언제든 앱을 **대체 서브넷(alternate subnet)** 에 연결할 수 있습니다.
단, 생성 시에 해당 설정을 적용하지 않으면 기능을 사용할 수 없으며, 기존 ASE에서는 해당 기능을 활성화할 수 없습니다.

포털에서는 해당 클러스터 설정을 활성화하거나 대체 서브넷을 연결하는 기능을 제공하지 않습니다.
따라서 ARM/Bicep 템플릿을 통하여 ASE를 생성해야 합니다.

대체 서브넷은 다음의 Azure CLI 명령어를 사용하여 연결할 수 있습니다.
**대체 서브넷은 비어 있어야 하며 Microsoft.web/serverfarms에 위임되어야 합니다**.
또한 [application traffic routing 이 앱에서 활성화](https://learn.microsoft.com/en-us/azure/app-service/configure-vnet-integration-routing#configure-application-routing)되어 있는지 확인하시기 바랍니다.
이 설정은 트래픽이 기본 경로가 아닌 대체 서브넷을 통해 라우팅되도록 보장합니다.

```
az webapp vnet-integration add --resource-group <APP-RESOURCE-GROUP> --name <APP-NAME> --vnet <VNET-NAME> --subnet <ALTERNATE-SUBNET-NAME>
```

대체 서브넷이 앱과 다른 리소스 그룹에 있다면, 다음 명령어를 실행하여 도움말에서 리소스 id를 명시하는 방법을 확인해보시기 바랍니다.

```
az webapp vnet-integration add -h
```

## 🔧 기술 사양

멀티 테넌트 App Service에서 제공되는 [멀티 플랜 서브넷 연결](https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration#:~:text=With%20multi%20plan,larger%20subnet%20ranges.) 기능에 익숙하다면, ASE(App Service Environment)와 대체 서브넷 연결 기능은 이와 호환되지 않는다는 점을 알아두세요. ASE에서는 각 앱이 하나의 대체 서브넷만 연결할 수 있습니다.

일반적인 가상 네트워크 통합과 유사하게, 하나의 플랜은 여러 개의 연결을 가질 수 있으며 동일한 플랜의 앱은 두 연결 중 하나를 사용할 수 있습니다.
멀티 테넌트 App Service에서는 플랜당 최대 2개의 연결이 가능하지만, ASEv3에서는 최대 4개의 연결을 지원합니다.

앱의 대체 서브넷 연결은 언제든 변경하거나 제거할 수 있습니다. 기존 연결을 삭제한 후, 이전과 같은 방식으로 새 연결을 추가하면 됩니다.

## 💡 해당 기능이 중요한 이유
ASEv3는 항상 **격리**, **확장성**, **제어**를 중시해왔습니다.
아웃바운드 트래픽 분리 기능을 통해 제어 수준을 한 단계 더 강화할 수 있습니다.
고성능 웹앱을 운영하거나, 민감한 데이터를 처리하거나, 복잡한 환경을 관리하는 경우에도 이 기능은 **성능을 저하시키지 않으면서 아웃바운드 트래픽을 안전하게 보호**할 수 있는 도구를 제공합니다.

## 📚 더 알아보기 
App Service Environment v3의 네트워킹 기능을 더 깊이 살펴보려면 [App Service Environment v3 네트워킹 개요](https://learn.microsoft.com/azure/app-service/environment/networking)를 살펴보세요.

질문이나 피드백은 아래 댓글로 남겨주세요.

----------

- 2025년 10월 2일 업데이트 됨.
- 2025년 10월 3일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))