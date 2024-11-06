---
layout: post
title:  "Azure 네트워크 이해하기 (3/3)"
author: rose
categories: [ Azure, Azure Networking, Hybrid Cloud ]
image: assets/images/thumnails/azure_network_3.png
---

> 우리 주변의 기업과 기관의 인프라는 더 이상 자체 데이터센터에 국한되지 않고, 다양한 혁신 기능으로 발전하고 있는 클라우드의 영역으로 확장되고 있습니다. 이번 포스트에서는 온프레미스 환경과 Azure 클라우드 환경을 안전하게 연결해, 하이브리드 클라우드 환경을 구축하는 방법을 소개합니다.
> 

### Microsoft Azure 하이브리드 클라우드 네트워크 옵션

Microsoft는 온프레미스 환경과 클라우드 환경을 연결할 때, 보안이 갖춰진 네트워크를 구성하는 방법으로 3가지 옵션을 제공합니다.

### VPN

VPN (Virtual Private Netwok) 은 인터넷 등의 WAN (Wide Area Network) 를 사용해서 전용선을 만드는 기술입니다. 인터넷 상 암호화된 터널 안에서 두 지점 사이의 사용자들이 안전하게 데이터를 주고 받을 수 있게 합니다.

어릴 적 많이 만들던 종이컵 실전화기 기억 나시나요? 마치 수많은 사람들이 있는 공간에서 종이컵 전화기로 비밀 이야기를 하는 그림이 떠오르네요!

![img](https://cdn-images-1.medium.com/max/1200/1*mH829uwHL_TdJ_K-mtHhzg.jpeg)

VPN은 고가의 전용선이 없이도 가용하며, 원격 업무 PC에서 사내 시스템에 접근할 때에도 적용 가능한 옵션이기에, **비용 효율적인 옵션**이라고 알려져 있습니다.

Azure VPN은 인터넷 상에서 암호화된 터널을 어떻게 만들까요? 바로, IPSec/IKE (IKEv1 — basic SKU, IKEv2 — basic 외의 SKU) 프로토콜로 VPN 터널의 인증 및 암호화를 수행합니다. 이 두 가지가 함께 작동하여 터널 내에서 주고 받는 데이터를 암호화하고 인증합니다. IPSec/IKE 에서 지원하는 암호화 알고리즘과 파라미터 조합(AES, SHA, DHGroup) 은 VPN 터널마다 다르게 커스텀 설정이 가능합니다. 연결 대상 디바이스에 따라, 권장하는 스펙은 이 [링크](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-devices#devicetable)를 참조하세요.

여기서 IPsec은 인터넷 프로토콜 보안(Internet Protocol Security)을 의미하고, 전송 데이터를 암호화하여 전송 중에 도청이나 변조되는 것을 방지합니다. IKE는 인터넷 키 교환(Internet Key Exchange)을 의미하고, 두 네트워크 장치 간 IPsec 터널 설정에 사용됩니다.

VPN Gateway를 사용하여 온프레미스 환경과 클라우드 환경의 가상 네트워크에 암호화된 연결을 구성하며, 다음과 같이 연결 대상에 따라 3가지 유형으로 생성할 수 있습니다.

- 온프레미스 환경의 LAN을 연결하는 **Site-to-Site VPN 연결 (S2S VPN)**
- 온프레미스 환경의 특정 엔드포인트를 대상으로 연결하는 **Point-to-Site VPN 연결 (P2S VPN)**
- 가상 네트워크끼리 연결하는 **VNet-to-VNet VPN 연결**

예시와 함께 조금 더 쉽게 풀어볼까요? Site-to-Site VPN 연결은 거점 간 연결의 개념으로, 하이브리드 환경을 구성할 때 이외에도 서울에 있는 본사 오피스와 지방 지역에 있는 지사 오피스를 연결할 때에도 쓰입니다.

![img](https://cdn-images-1.medium.com/max/1200/0*uXipgAcxBG_B4sFb.png)

Point-to-Site VPN 연결은 원격 접근 VPN의 개념으로, 재택 근무를 하는 재택 근로자나 해외 연구원 등 지리적으로 멀리 떨어진 곳의 사용자를 연결할 때 사용합니다.

그림과 같이, VPN Gateway 는 여러 VPN 터널 연결이 가능합니다. 이 때 회선의 개수가 늘어날 수록 VPN Gateway 에서 처리할 데이터의 용량도 늘어나는데요. 개수에 비례하여 처리 용량이 확장되는 것은 아닙니다. 회선 1개에 대해서 1Gbps의 처리 용량을 지원하고, 여러 개의 회선에 대해 최대 1.25Gbps의 총처리량 (Aggregate Throughput) 을 제공합니다.

![img](https://cdn-images-1.medium.com/max/1200/0*IwgH3mxhMkVVJkfP.png)

---

### ExpressRoute (ER)

ExpressRoute는 회선 사업자가 제공하는 전용선으로 온프레미스 환경과 Azure 클라우드 환경을 직접 연결하는 기술입니다. 다른 옵션에 비해 가격이 높은 만큼, 인터넷 경유없이 회선 대역을 점유 (최대 10GB) 할 수 있어서 고품질의 통신이 가능합니다.

보통 인터넷을 통해 데이터를 송수신할 때는 일반 도로를 이용하는 것과 비슷해요. 여러 차량들 (데이터)이 섞여서 다니기 때문에 교통 체증 (지연, latency)이 발생할 수 있죠. 하지만 Azure ExpressRoute를 사용하면, 전용 고속도로를 이용하는 것과 같은 효과로 훨씬 빠르고 안정적인 데이터 송수신이 가능해요.

![img](https://cdn-images-1.medium.com/max/1200/1*JjxcNTzxNXXCALx_ntwXxg.jpeg)

ExpressRoute는 ER Circuit을 사용하여 전용회선을 설치할 수 있습니다. 연결 구조는 온프레미스 환경 — 회선 사업자 엣지 — ER Circuit — Microsoft 엣지로 구성됩니다.

![img](https://cdn-images-1.medium.com/max/1200/0*O8DxZarexa5dB_VN.png)

Azure ExpressRoute는 네트워크 장애 위험을 최소화하고 높은 가용성을 갖춘 설계를 위해 ER Circuit 의 Primary와 Secondary Connection 의 Active-Active 연결 모드로 운영하도록 구성되어 있습니다. 이중화된 경로를 통해, Microsoft 의 네트워크가 연결 간 트래픽을 부하분산 (Load Balancing) 하며 운영합니다.

### VPN과 ER의 시너지!

S2S (Site-to-Site VPN) 과 ER 연결을 함께 사용하면 더욱 유연하고 안전한 네트워크를 구성할 수 있습니다. 먼저, S2S VPN 연결이 ER 작동에 문제가 발생했을 때 failover의 개념으로 대신 작동하여 온프레미스 환경과 클라우드 간의 연결 끊김 문제를 방지할 수 있습니다. 다음으로는, ER 전용선으로 직접적으로 연결이 어려운 사이트를 S2S VPN으로 추가 연결함으로서, 더 많은 거점을 유동적으로 Azure 에 확장할 수 있는 장점이 있습니다.

![img](https://cdn-images-1.medium.com/max/1200/0*Kz_CaaP4dGy0BZni.png)

---

### Virtual WAN (VWAN)

Virtual WAN 은 네트워크 보안과 라우팅의 총 집합체라고 표현할 수 있는 옵션입니다. Virtual WAN을 하나의 허브처럼 두면, 위에서 소개한 여러 지사를 ExpressRoute로 연결 거점 간 VPN을 연결하는 등의 여러가지 네트워크 구성을 Mesh 형태로 **하나의 인터페이스로 통합할 수 있어서 관리 포인트를 줄일 수 있는 장점**이 있습니다.

Virtual WAN은 계층 3 오버레이 (Layer 3 Overlay) 네트워크를 통해 서로 다른 물리적 네트워크에 있는 장치들을 마치 하나의 네트워크에 있는 것처럼 가상의 연결을 구성합니다. 이는 네트워크 복잡성을 줄이고 단순화하는 효과가 있습니다. 여기서 Virtual WAN의 구성 요소인 Virtual Hub가 가상의 라우터 역할을 지원합니다. 이를 통해 다양한 네트워크 연결을 중앙에서 관리할 수 있습니다.

Virtual WAN을 온프레미스와의 연결 뿐 아니라, Azure VNet 간의 연결의 일관성 유지에도 활용할 수 있습니다. 일반적인 VNet Peering에서는 transit 연결 (데이터를 주고 받을 때 중간 경로를 제공하는 연결 방식)을 지원하지 않아, 여러 개의 Peering 을 사용한다면 복잡도가 증가합니다. 이러한 문제를 VNet과 Virtual WAN의 1:1로 연결하여 효율적인 연결 방식을 구현할 수 있습니다.

![img](https://cdn-images-1.medium.com/max/1200/0*HxkPnKla5qlOmVTF.png)

여기까지 Azure 네트워크의 하이브리드 연결 옵션에 대해 알아보았습니다. 온프레미스와 Azure의 연결로 더 넓은 인프라 영역을 고민하고 있는 여러분에게 도움이 되었기를 바라며, Azure 네트워크 이해하기 포스팅을 마칩니다!

---

참조:

[Azure VPN Gateway topology and design] [About Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways)

[IPSec/IKE policy] [Configure custom IPsec/IKE connection policies for S2S VPN & VNet-to-VNet: Azure portal — Azure VPN Gateway | Microsoft Learn](https://learn.microsoft.com/en-us/azure/vpn-gateway/ipsec-ike-policy-howto)

[Azure ExpressRoute] [Azure ExpressRoute Overview: Connect over a private connection | Microsoft Learn](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction)

[ER High Availability] [Azure ExpressRoute: Designing for high availability | Microsoft Learn](https://learn.microsoft.com/en-us/azure/expressroute/designing-for-high-availability-with-expressroute)

[Azure Virtual WAN] [Azure Virtual WAN Overview | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about)