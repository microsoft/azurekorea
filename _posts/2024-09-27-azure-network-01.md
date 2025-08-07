---
layout: post
title:  "Azure 네트워크 이해하기 (1/3)"
author: annajeong
tag: [ Azure, Azure Network, Azure Global Network, Azure Virtual Network ]
category: [ Solution ]
image: assets/images/thumnails/azure_network_1.png
---

> 많은 기업들이 확장성, 고가용성, 비용 등 다양한 이유로 클라우드를 채택하고 사용하는 것이 보편화되고 있습니다. 클라우드를 시작할 때 가장 먼저 구성하게 되는 요소가 바로 네트워크인데요. 이번 포스트에서는 Azure의 네트워크에 대해 소개 드리도록 하겠습니다.
> 

### Microsoft의 글로벌 네트워크

![img](https://cdn-images-1.medium.com/max/1200/1*sWIrXsJM9Wm0M98hZwUSIA.png)

[그림1] Microsoft의 글로벌 네트워크

Microsoft는 전 세계에서 가장 큰 백본 네트워크 중 하나를 소유하고 운영중입니다. 미국 버니지아와 스페인 발바오를 가로지르는 대서양 케이블인 MAREA 해저 케이블(업계 최초의 OLS; Open Line System)을 보유하고 있으며, Microsoft의 데이터 센터를 전 세계에 전략적으로 배치된 대규모 에지 노드에 메시 형태로 구성하고 있습니다. 이 에지 노드들은 4000개가 넘는 고유한 인터넷 파트너(피어)와 상호 연결되어 글로벌에 광범위한 네트워크 백본을 구축합니다.

예를 들어 한국의 사용자가 Azure의 서비스에 엑세스하려고 시도하는 경우 인터넷 트래픽이 한국에 있는 Microsoft의 에지 중 하나에 진입하여 Microsoft WAN을 통해 서비스가 상주하는 데이터 센터까지 이동합니다. 이 네트워크 백본을 사용하여 네트워크 트래픽을 안전하게 전송하거나 한국의 다양한 규제들에 대응할 수 있습니다.

### Azure의 인프라 스트럭처

![img](https://cdn-images-1.medium.com/max/1200/1*0HqIK2VFhOhsNC733x5RTA.png)

[그림2] Azure의 인프라 스트럭처

먼저 Azure의 인프라 스트럭처를 알아보도록 하겠습니다. Azure의 물리적 인프라는 크게 **리전 페어(Region Pair), 리전(Region), 가용성 영역(Availability Zone)**으로 이루어지게 됩니다.

먼저 **가용성 영역**은 하나 이상의 데이터 센터의 집합입니다. 각 데이터 센터는 독립적인 전원, 냉각 및 네트워킹 시스템을 가지게 됩니다. 데이터 센터 장애로부터 워크로드를 보호하기 위한 내결함성을 제공합니다.

다음으로 **리전**은 대도시 내의 데이터 센터의 집합입니다. 가용성 영역을 지원하는 리전은 3개 이상의 가용성 영역으로 구성됩니다. 이 때 리전 내 가용성 영역 간의 네트워크 지연 시간은 < 2ms 입니다. 리전 내 가용성 영역을 통해 워크로드를 구성함으로써 보다 높은 고가용성을 구성할 수 있습니다.

마지막 개념은 **리전 페어**로써, 타 CSP 들과 차이점을 가지는 요소입니다. 리전 페어는 두 개 이상의 리전으로 구성됩니다. 한국의 경우 **한국 중부 리전**과 **한국 남부 리전**을 제공하고 있습니다. 리전 장애로부터 워크로드를 보호하기 위한 높은 가용성을 제공하고 리전 페어를 통해 국내의 다양한 규정 준수 요구 사항을 충족할 수 있습니다.

### 리전 네트워크

![img](https://cdn-images-1.medium.com/max/1200/1*Tj7cMO2Rukk8JFXwf32WHg.png)

[그림3] 리전 네트워크

Azure는 대규모 병렬 처리, 하이퍼스케일을 제공하기 위해 위의 [그림3]과 같이 리전 네트워크가 구성되어 있습니다. 리전 내부에 리전의 크기에 따라 T-shirt Sized의 RNG(Regional Network Gateway)가 메시 형태로 존재합니다. 최상단에는 RNG 페어가 존재하는데 이 RNG가 Microsoft의 WAN과 메시 형태로 연결되어 있습니다. 리전 내 각 데이터 센터 또한 메시로 구성되어 있으며 리전 내 네트워크 대역폭은 1.6Pb/s가 지원됩니다. 또 RNGs는 앞서 설명드린 Microsoft의 에지와 연결됩니다. 각 에지는 전용선 연결인 Express Route나 인터넷 제공 업체(ISP; Internet Service Provider)와 연결되어 인터넷과 연결됩니다.

만약 한국 중부 리전과 연결된 에지가 모두 다운되면 어떻게 될까요? 앞서 RNGs가 MS WAN과 연결된다고 말씀드렸는데요. 리전과 연결된 에지가 모두 다운되더라도 RNGs와 연결된 MS WAN을 통해 다른 리전의 에지를 타고 트래픽이 이동함으로써 백본의 가용성이 유지됩니다.

### Software Defined Network (SDN)

![img](https://cdn-images-1.medium.com/max/1200/1*A-mto7pecwr5dxyVye0lWQ.png)

[그림4] Software Defined Network]

SDN(소프트웨어 정의 네트워킹)은 데이터 센터에서 전환, 라우팅 및 부하 분산과 같은 네트워크 및 네트워크 서비스를 중앙에서 구성하고 관리하는 방법을 제공합니다. SDN을 사용하여 변화하는 앱 요구 사항에 맞게 네트워크를 동적으로 만들고, 보호하고, 연결할 수 있습니다. 매일 수만 개의 네트워크 변경을 효율적으로 수행하는 Azure와 같은 서비스에 대해 글로벌 규모의 데이터 센터 네트워크를 운영하는 것은 SDN으로 인해서만 가능합니다.

SDN은 매니지먼트, 컨트롤 및 데이터 플레인으로 구성됩니다. 예를 들어 매니지먼트 플레인은 테넌트를 만듭니다. 그리고 컨트롤 플레인은 테넌트 ACL을 스위치로 연결합니다. 마지막으로 데이터 플레인은 호스트의 흐름에 ACL을 적용합니다. 이 아이디어는 많은 구성을 호스트로 푸시하고 그 위에 확장 가능한 관리 아키텍처를 두는 것입니다.

Azure에는 네트워킹에 중점을 둔 리소스 공급자(Resource Provider), 특히 네트워크 리소스 공급자가 있으며 그 아래에는 리소스를 관리하는 네트워크 리전 매니저가 있으며 리저널 리소스입니다. Network RP는 Compute RP와 함께 작동하여 가상 네트워크, 로드 밸런서 및 가상 플랫폼을 관리하는 도드 에이전트와 그 안의 네트워크 에이전트를 통해 서버에서 함께 작동합니다.

이 개념대로라면 호스트로 푸시 다운되면서 처리해야 할 많은 작업이 생깁니다. 이는 많은 CPU Cycle을 소모하므로 Microsoft는 vSwitch를 FPGA 기반 SmartNics로 교체했습니다. 이는 CPU 부하를 제거하고 지연 시간을 115μs에서 30μs로 줄여 FPGA가 라인 속도에 가까운 처리량을 달성할 수 있도록 합니다.

여기까지 Azure의 네트워크 인프라에 대해 알아보았습니다. 다음 포스트에서는 **Azure 네트워크 기본 구성**에 대해 알아보도록 하겠습니다.

---

참조:

[Microsoft 글로벌 네트워크] [https://azure.microsoft.com/ko-kr/explore/global-infrastructure/global-network](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/global-network)

[Azure 리전 선택] [https://azure.microsoft.com/ko-kr/explore/global-infrastructure/geographies](https://azure.microsoft.com/ko-kr/explore/global-infrastructure/geographies)

[Azure 가용성 영역] [https://learn.microsoft.com/ko-kr/azure/reliability/availability-zones-overview?tabs=azure-cli](https://learn.microsoft.com/ko-kr/azure/reliability/availability-zones-overview?tabs=azure-cli)

[애저 네트워크 기본 설계] [https://youtu.be/LBtFx0ijnD4](https://youtu.be/LBtFx0ijnD4)
