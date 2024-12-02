---
layout: post
title:  "Azure 네트워크 이해하기 (2/3)"
author: annajeong
categories: [ Solution ]
image: assets/images/thumnails/azure_network_2.png
---

> 지난 포스트에서는 Azure가 어떻게 광범위한 네트워크 백본을 제공하고 있는지에 대해서 알아보았습니다. 이번 포스트에서는 Azure의 네트워크 인프라스트럭처를 기반으로 제공되는 Azure 네트워크 기본 구성에 대해 알아보도록 하겠습니다.
> 

### 가상 네트워크

앞서 Azure는 글로벌에 광범위한 네트워크 백본을 가지고 있다고 말씀드렸습니다. Virtual Network는 Azure 네트워크 상에 고객의 격리된 가상 네트워크 부분입니다. Azure 네트워크 상의 계층 3 오버레이 구성이라고 생각하시면 됩니다.

![img](https://cdn-images-1.medium.com/max/1200/1*q3IEfDNmKITJCI-l-FEwlQ.png)

[그림1] Azure Virtual Network

**첫번째로 주소 범위 지정입니다.** CIDR를 사용한 주소 범위를 지정하여 사용하실 수 있고 이 때 RFC1918에 명시된 사설 네트워크 대역을 사용하는 것이 권고되지만 **CIDR의 범위는 고객이 임의로 지정할 수 있습니다.**

![img](https://cdn-images-1.medium.com/max/1200/1*ia3-6xt4q8x7gvlDKNPk1A.png)

[그림2] CIDR 주소 체계

기존 IP 체계를 언급할 때 A, B, C.. 클래스에 대해서 들어보셨을텐데요. CIDR(Classless Inter-Domain Routing)은 기존의 네트워크 클래스의 단점(A 클래스의 경우 ²²⁴-2개의 호스트 IP가 할당되며 대다수의 IP가 낭비되는 문제 등)을 보완하는 라우팅 기법으로 기존 방식에 비해 유연성을 제공합니다.

이 CIDR 주소 체계를 사용하여 가상 네트워크의 주소 범위를 지정할 수 있습니다. 예를 들어 그림2의 경우 **10.0**.0.0을 이진수로 표현했을 때 **00001010 00000000** 00000000 00000000으로 표기할 수 있고 / 뒤의 숫자인 **16비트**를 고정으로 하여 10.0.0.0 ~ 10.0.255.255 주소 범위를 사용할 수 있습니다. **가상 네트워크는 /16 ~ /24 주소 범위까지 사용 가능합니다.**

두번째로 가상 네트워크는 타 CSP들과 다르게 **리전의 모든 가용성 영역에 걸쳐서 만들어지는 리저널 리소스**입니다.

마지막으로 가상 네트워크의 모든 리소스는 기본적으로 **인터넷으로의 아웃바운드 통신이 가능**합니다. 가상 네트워크가 격리된 가상 공간이라고 말씀드렸는데요. 기본 아웃바운드 같은 경우는 Azure가 가지고 있는 Elastic IP를 통해 이루어지게 됩니다.

기본 아웃바운드를 제한하기 위해서는 뒤에서 설명드릴 **네트워크 보안 그룹**을 사용하실 수 있고, 현재 공개 미리보기 상태의 **프라이빗 서브넷**으로 구성하실 수 있습니다. (2025년 9월 GA 예정)

### 서브넷

![img](https://cdn-images-1.medium.com/max/1200/1*Kr5lY9EkVS7qftN3TUFCFA.png)

[그림3] Azure Subnet

다음으로 알아볼 기능은 서브넷입니다. 가상 네트워크를 하나 이상의 하위 네트워크로 분할하는 서비스입니다. 앞서 말씀드린 것처럼 가상 네트워크와 서브넷넷은 가용성 영역에 걸쳐서 배포되게 됩니다. 따라서 다른 CSP들처럼 가용성 역영에 서브넷이 종속되지 않음으로써 온프레미스에서 단순히 서브넷팅만 하는 서브넷의 용도와 더 가깝다고 볼 수 있습니다.

최대 ~/29 주소 범위를 지정할 수 있으며, IPv6의 경우 정확히 /64 주소 범위를 사용해야 합니다.

그리고 서브넷의 첫번째와 마지막 주소는 호스트 주소, 브로드캐스트 주소로 예약되어 있으며 추가로 DNS, 관리의 목적으로 3개의 주소가 Azure에서 더 예약되어 있어서 총 5개의 주소를 제외한 주소 범위를 사용할 수 있습니다.

### 인/아웃바운드 구성

앞서 설명 드린 것처럼 Azure는 기본 아웃 바운드 액세스를 제공합니다. 제로 트러스트 네트워크 보안 원칙에 기반하여 기본 액세스를 사용하는 것은 권장되지 않으며 가상 머신에 대한 명시적 아웃바운드를 구성할 수 있습니다.

![img](https://cdn-images-1.medium.com/max/1200/0*IW79N-V3iJLJqTZ0.png)

[그림4] 명시적 아웃바운드 액세스 구성

1. 기본 아웃바운드 액세스 : 별도의 Gateway 등을 구성할 필요없이 기본적으로 제공됩니다.
2. Load Balancer 사용 : 공용 Load Balancer (L4)를 사용하여 포트 기반의 NAT를 구성할 수 있습니다.
3. NAT Gateway 사용 : NAT Gateway를 사용하여 명시적 NAT를 구성할 수 있습니다. 이 구성은 SNAT 포트 고갈을 피하기 위한 방법으로 권장됩니다.

반면 인바운드 액세스를 구성하기 위해서는 명시적 구성이 필요합니다.

![img](https://cdn-images-1.medium.com/max/1200/1*HWAnXxd13FlRpFHseVdd6w.png)

[그림5] 명시적 인바운드 구성

간단하게 구성할 수 있는 옵션 두 가지는 가상 머신에 Public IP를 할당하는 방법과 Public IP를 가진 Load Balancer를 사용하는 방법입니다.

Public IP를 가진 Load Balancer를 통해 부하 분산을 구성하게 되면 인터넷으로부터의 트래픽이 Load Balancer가 가진 Public IP를 통해 액세스 되고, Load Balancer가 가지고 있는 Private IP로 SNAT 됩니다. 이 Private IP를 통해 가상 네트워크 내의 가상 머신의 Private IP로 트래픽이 전달됩니다.

### 경로 테이블

![img](https://cdn-images-1.medium.com/max/1200/1*yh3qRpLvdpPy-GQ5C9dsPQ.png)

[그림6] Route Table 구성

경로 테이블(혹은 사용자 지정 경로)은 가상 네트워크내외부의 트래픽의 흐름을 제어하기 위해 사용할 수 있는 방법입니다. 아래와 같이 세 가지 유형으로 구성됩니다.

![img](https://cdn-images-1.medium.com/max/1200/1*yh3qRpLvdpPy-GQ5C9dsPQ.png)

[그림7] Route Table

- **시스템 경로 (기본값)**

기본적으로 가상 네트워크 주소 공간에 속한 주소 범위 간에 트래픽을 라우팅하기 위해 가상 네트워크 고유 접두사 구성과 0.0.0.0/0 인터넷으로의 라우팅 항목이 포함됩니다.

- **선택적 기본 경로**

VNet 피어링, Virtual Network Gateway, VirtualNetworkServiceEndpoint 등 해당 기능을 사용하는 경우에 추가됩니다.

- **사용자 지정 경로**

Azure의 기본 시스템 경로를 재정의하거나 서브넷의 경로 테이블에 더 많은 경로를 추가하기 위해서 사용자가 구성할 수 있는 경로 테이블입니다.

가상 어플라이언스, 가상 네트워크 게이트웨이, 없음(None), 가상 네트워크, 인터넷 등의 경로를 지정하거나 재정의 할 수 있습니다.

경로 테이블은 서브넷에 연결할 수 있습니다.

### 네트워크 보안 그룹

![img](https://cdn-images-1.medium.com/max/1200/1*qqSHWjWTJurV4hmBu5murg.png)

[그림8] Network Security Group

마지막으로 살펴볼 개념은 Azure 네트워크 상에서 리소스 간의 네트워크 트래픽을 필터링 할 수 있는 개념은 네트워크 보안 그룹입니다. 서브넷과 가상 머신의 네트워크 인터페이스에 연결할 수 있으며, 방화벽과 같은 Stateful한 필터링 규칙을 적용할 수 있습니다.

여러 종류의 Azure 리소스에서 오는 인바운드 트래픽 또는 아웃바운드 트래픽을 허용하거나 거부하는 보안 규칙을 작성할 수 있습니다. 보안 규칙은 5-tuple (원본, 원본 포트, 대상, 대상 포트, 프로토콜)을 기반으로 평가 및 적용됩니다. 각 규칙은 100~4096 사이의 숫자를 지정할 수 있으며 낮은 번호의 우선 순위가 더 높기 때문에 규칙이 **낮은 번호가 높은 번호보다 먼저 처리됩니다.**

![img](https://cdn-images-1.medium.com/max/1200/1*8_JvGE2S2wGCT0filWzmyA.png)

[그림9] Network Security Group 예제 구성

예를 들어 [그림9]와 같은 예제 구성이 존재한다고 가정해 보겠습니다.

- NSG1은 규칙 300번에 인터넷으로부터 들어오는 80번 포트를 허용하는 규칙을 가지고 있습니다.
- NSG1은 Subnet1과 Subnet2에 연결되어 있습니다.
- NSG2는 가상 머신이 가진 네트워크 인터페이스에 연결되어 있습니다.

이 때 80번 포트를 통해 접속할 수 있는 가상 머신은 두번째가 되게 됩니다. NSG가 중첩으로 구성되어 있을 때 평가 순서는 트래픽의 흐름을 생각하면 됩니다. 첫번째의 경우 인바운드 트래픽은 인터넷 → NSG1 → NSG2 → 가상 머신 순서대로 흐르기 때문에 NSG1이 80번 포트를 허용하더라도 NSG2번에서 거부되게 됩니다. 마찬가지로 세번째의 경우도 NSG2에서 80번 포트를 허용하지 않기 때문에 트래픽이 거부되게 됩니다.

### 애플리테이션 보안 그룹

![img](https://cdn-images-1.medium.com/max/1200/1*4o_h7iX2thSQ8mYnq7y9YQ.png)

[그림10] Application Security Group

네트워크 보안 그룹의 경우 원본 또는 대상으로 IP 주소, CIDR 블록 또는 서비스 태그 등을 지정할 수 있습니다. 전통적인 3-tier (Web/WAS/DB) 애플리케이션을 구성할 때, Web 서브넷은 인터넷으로 부터 들어오는 트래픽을 WAS서브넷은 Web 서브넷으로부터 전달된 트래픽을 DB 서브넷은 WAS 서브넷으로부터 전달된 트래픽을 허용하면 됩니다.

이를 구성할 수 있는 서비스가 애플리케이션 보안 그룹입니다. 원본 또는 대상에 애플리케이션 보안 그룹을 적용할 수 있습니다. 애플리케이션 보안 그룹을 사용하면 네트워크 보안을 애플리케이션 구조의 자연 확장으로 구성하여 가상 머신을 그룹화하고 해당 그룹에 따라 네트워크 보안 정책을 정의할 수 있습니다. 또 명시적 IP 주소를 수동으로 유지 관리하지 않고 대규모 보안 정책을 재사용할 수 있습니다.

이번 포스트에서는 Azure 네트워크를 구성하는 기본 서비스들에 대해서 알아보았습니다. 마지막 포스트에서는 Azure 네트워크를 다른 가상 네트워크와 연결하거나 온프레미스 등으로 확장하여 하이브리드 네트워크를 구성하는 법에 대해서 알아보도록 하겠습니다.

---

참조:

[가상 네트워크] [https://learn.microsoft.com/ko-kr/azure/virtual-network/virtual-networks-overview](https://learn.microsoft.com/ko-kr/azure/virtual-network/virtual-networks-overview)

[프라이빗 서브넷] [https://azure.microsoft.com/ko-kr/updates/public-preview-private-subnet/](https://azure.microsoft.com/ko-kr/updates/public-preview-private-subnet/)

[기본 아웃바운드 액세스] [https://learn.microsoft.com/ko-kr/azure/virtual-network/ip-services/default-outbound-access](https://learn.microsoft.com/ko-kr/azure/virtual-network/ip-services/default-outbound-access)

[경로 테이블] [https://learn.microsoft.com/ko-kr/azure/virtual-network/manage-route-table](https://learn.microsoft.com/ko-kr/azure/virtual-network/virtual-networks-udr-overview)

[네트워크 보안 그룹] [https://learn.microsoft.com/ko-kr/azure/virtual-network/network-security-groups-overview](https://learn.microsoft.com/ko-kr/azure/virtual-network/network-security-groups-overview)

[애저 네트워크 기본 설계] [https://youtu.be/LBtFx0ijnD4](https://youtu.be/LBtFx0ijnD4)