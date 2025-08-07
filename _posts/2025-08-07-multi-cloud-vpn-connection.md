---
layout: post
title:  "VPN 연결로 구성하는 안전한 멀티 클라우드 네트워크"
author: annajeong
tag: [ Azure, Azure Network, VirtualWAN, VPN, MultiCloud ]
category: [ Solution ]
image: assets/images/thumnails/multi-cloud-vpn-connection.png
---

클라우드 도입이 보편화되면서, 최근 많은 기업들이 **멀티 클라우드** 또는 **하이브리드 클라우드 전략**을 적극 채택하고 있습니다. 이처럼 다양한 클라우드 환경을 활용하기 위해 일부 기업은 온프레미스를 허브처럼 활용하여 클라우드 간 연결을 구성하기도 하지만, 각 클라우드 간 **직접적인 VPN 연결** 또는 **전용 회선 연결**을 통해 보다 효율적이고 안정적인 네트워크를 설계할 수도 있습니다.

이번 포스팅에서는 **Azure와 AWS 간 VPN 연결 구성 방법**을 중심으로, 두 클라우드 간에 **안전하고 신뢰할 수 있는 네트워크 아키텍처**를 어떻게 설계할 수 있는지 살펴보겠습니다.

이번 구성에서는 아래와 같은 단계로 **Azure와 AWS 간 Site-to-Site VPN 연결**을 설정해보겠습니다.

1. **네트워크 준비**: Azure VNet과 AWS VPC를 생성하고 서로 다른 IP 대역으로 구성합니다.
2. **Azure - 사이트 간 게이트웨이 구성**: Virtual WAN 환경에서 Virtual Hub를 만든 뒤, AWS VPN의 공인 IP와 VPC CIDR을 기반으로 Local Network Gateway를 생성합니다.
3. **AWS - VPN 게이트웨이 구성**: Virtual Private Gateway를 생성해 VPC에 연결하고, Azure VPN Gateway의 공인 IP와 ASN으로 Customer Gateway를 구성합니다.
4. **Azure - VPN Site 연결 생성**: Virtual Hub에서 Site-to-Site 연결을 생성하고, AWS CGW 정보를 기반으로 PSK 및 BGP 설정을 완료합니다.
5. **터널 정보 동기화**: AWS에서 제공하는 터널 IP, BGP 정보 등을 Azure에 반영합니다.

> **참고:** 독자의 이해를 돕기 위해 본 포스팅에서는 일부 구성 정보(IP 주소, ASN 등)를 **마스킹 없이 그대로 제공**하였습니다.
> 
> 
> 실제 환경 구성 시에는 반드시 보안 정책에 따라 **민감 정보는 철저히 보호**하시기 바랍니다.
> 

## Azure - 사이트 간 게이트웨이 구성

Azure에서는 다양한 방식으로 안전한 VPN 연결을 구성할 수 있도록 지원하고 있습니다. 대표적으로는 **Azure VPN Gateway** 리소스를 통해 기본적인 VPN 연결을 구성할 수 있으며, 보다 확장된 네트워크 시나리오에서는 **Azure Virtual WAN**을 활용할 수도 있습니다.

Virtual WAN은 **Layer 3에서 최적화된 분기 간 연결을 제공하는 네트워킹 서비스**로, VPN은 물론 **전용 회선(ExpressRoute)** 연결도 함께 지원하며, 네트워크 구성과 운영을 더욱 단순화하고 자동화할 수 있는 것이 특징입니다.

이번 포스팅에서는 **Virtual WAN의 VPN 연결 구성 방법**을 중점적으로 소개드리고, 기존 VNet VPN Gateway와의 주요 차이점도 함께 살펴보겠습니다.

- Virtual WAN의 VPN
    - **Microsoft 글로벌 백본망 기반**
        
        Virtual WAN은 Azure가 전 세계적으로 운영하는 고성능 백본망을 기반으로 구성되며, 복잡한 인프라 설정 없이 **논리적 연결 구성만으로 VPN 환경을 구축**할 수 있습니다.
        
    - **중앙집중형 네트워크 관리**
        
        라우팅 테이블, 연결 전파, 경로 구성 등을 **GUI 또는 IaC(Bicep, Terraform 등)** 을 통해 손쉽게 관리할 수 있으며, **클라우드 네이티브 방식의 네트워크 운영**을 실현할 수 있습니다.
        
    - **유연한 과금 구조**
        
        사용한 Virtual Hub 용량(Standard, Basic 등), 연결 수, 전송된 데이터량에 따라 과금되므로 **네트워크 규모에 맞춰 유연한 요금제 구성**이 가능합니다.
        
- 가상 네트워크의 VPN Gateway
    - **사용자 직접 구성 필요**
        
        VNet 내에 **Gateway Subnet**을 생성한 뒤, 해당 위치에 VPN Gateway를 직접 배포해야 하며, **라우팅 및 연결 구성 또한 수동**으로 설정해야 합니다.
        
    - **고정된 요금제**
        
        Gateway SKU(VpnGw1, VpnGw2 등)에 따라 **정해진 처리량, 연결 수, SLA**가 제공되며, **예측 가능한 고정 요금**으로 운영할 수 있습니다.
        

> 이번 포스팅에서는 **Virtual WAN 기반 VPN 연결 구성** 을 중심으로 소개해 드리겠습니다.
> 
> 
> 만약 **가상 네트워크의 VPN Gateway를 이용한 구성 방법** 이 궁금하시다면, 아래 링크를 참고해 주세요.
> 

1. Virtual WAN을 생성하고 Virtual Hub 리소스를 추가 생성합니다.
2. 생성한 Virtual Hub를 선택하고 왼쪽 Connectivity 블레이드에서 VPN (Site to site) 메뉴를 클릭합니다.
3. Create VPN Gateway를 클릭하여 리소스를 생성합니다.
    
    ![image.png](../assets/images/annajeong/image.png)
    
    - AS Number : BGP(Border Gateway Protocol)를 사용하는 경우, 각 네트워크(AS)는 고유한 번호를 가지는데, 이를 **AS Number**라고 합니다.  기본적으로 Azure는 AS 번호 **65515**를 사용합니다.
    - Gateway scale units : Virtual WAN에서 VPN Gateway는 **Scale Unit 단위로 성능을 확장**할 수 있으며, 이는 VPN 게이트웨이의 처리 용량을 결정합니다.  Scale Unit은 **유연하게 조정 가능**하지만, 늘리는 데 몇 분의 시간이 걸릴 수 있습니다.
        - 테스트/개발 환경: 1~2 Scale Unit
        - 중소기업 환경: 2~3 Scale Unit
        - 대기업, 고속 연결: 5 이상
    - Routing Preference : Virtual WAN 허브를 통해 나가는 **인터넷 트래픽에 대해 어떤 경로를 우선적으로 사용할지 지정**하는 옵션입니다. Microsoft Network는 Azure의 글로벌 백본망을 이용하여 인터넷으로 나갑니다.

## AWS - VPN 게이트웨이 구성

앞서 Azure에서 Virtual WAN 기반의 VPN 연결을 살펴보았다면, 이번에는 **AWS 환경에서 Site-to-Site VPN 연결을 생성**하는 방법을 단계별로 소개드리겠습니다.

이 과정을 통해 온프레미스 또는 다른 클라우드 환경과의 안전한 네트워크 터널을 구성할 수 있습니다.

### 가상 프라이빗 게이트웨이 생성

먼저 AWS VPC에 연결될 **가상 프라이빗 게이트웨이(Virtual Private Gateway, VGW)** 를 생성해야 합니다.

1. AWS 콘솔 > VPC > 가상 프라이빗 게이트웨이 메뉴로 이동합니다.
2. “가상 프라이빗 게이트웨이 생성” 버튼을 클릭합니다.
3. 이름 태그 및 ASN(자율 시스템 번호, BGP 사용 시)을 입력하고 생성합니다.
4. 생성 후, 해당 VGW를 연결할 VPC에 연결(Attach) 해줍니다.

### Site-to-Site VPN 연결 생성

이제 VGW를 기반으로 **Site-to-Site VPN 연결**을 생성합니다.

1. VPC > VPN 연결 메뉴로 이동합니다.
2. “VPN 연결 생성” 버튼을 클릭합니다.
3. 아래 항목들을 입력합니다:
    
    ![image.png](../assets/images/annajeong/image%201.png)
    
    - 대상 게이트웨이 유형: 가상 프라이빗 게이트웨이
    - 대상 게이트웨이: 앞서 생성한 VGW 선택
    - 고객 게이트웨이: 새로 생성 또는 기존 CGW 선택
        - 고객 게이트웨이란 Site-to-Site 연결을 만들기 위해 AWS 측에서 외부 네트워크(보통은 온프레미스)를 지정해주는 리소스입니다.
    - 라우팅 옵션: 동적(BGP) 또는 정적 선택
4. 생성이 완료되면, 두 개의 VPN 터널 정보가 생성되며, 이를 기반으로 Azure에서 VPN 구성을 진행합니다.

## Azure - VPN Site 연결 생성

AWS에서 Virtual Private Gateway와 Customer Gateway 구성을 마쳤다면, 이제 다시 **Azure 포털**로 돌아와 **VPN Site 연결(VPN site connection)**을 생성해보겠습니다.

이 단계에서는 Azure Virtual WAN의 Virtual Hub를 기준으로, AWS VPN 터널과의 연결을 위한 **VPN Site와 Link** 를 구성하게 됩니다.

### VPN Site 연결 생성

Virtual WAN > [내 Virtual WAN 이름] > VPN Sites > + Add VPN Site

여기서 새로운 VPN Site를 생성하며, 이름과 함께 **AWS VPC의 CIDR 범위**, **VPN 디바이스의 공인 IP 주소** 등을 입력합니다.

### Link 구성

VPN Site를 생성하는 과정에서 **Link 정보를 함께 입력**해야 합니다.

1. Link는 AWS 측에서 제공한 **VPN 터널 구성 정보**를 기반으로 아래와 같이 설정합니다.
    
    ![image.png](../assets/images/annajeong/image%202.png)
    
    - **Link name**: Tunnel1 (또는 원하는 이름)
    - **Link provider name**: AWS (선택 항목)
    - **Link speed**: 예: 1000 (단위: Mbps, 대략적인 값 입력)
    - **Link IP address / FQDN**: AWS에서 제공한 **Outside IP Address**
    - **Link ASN**: AWS 측의 ASN(Autonomous System Number)
    - **Link BGP address** (예시)
        - `169.254.75.80`은 AWS 측 BGP 피어 주소입니다. (즉, Customer Gateway에서 볼 때 AWS의 VPN 터널 엔드포인트 주소)
        - `169.254.75.81`은 Azure 측 BGP 피어 주소로 설정해야 합니다. (즉, Azure의 Virtual Hub가 이 주소로 BGP를 수행함)
    
    > AWS에서는 기본적으로 두 개의 터널 정보를 제공하므로, 두 개의 Link를 생성하여 **이중화 구성**도 가능합니다.
    > 
    

### 가상 허브에 VPN 사이트 연결

VPN Site와 Link 구성이 완료되었다면, 이제 마지막 단계로 **Virtual Hub에 해당 VPN Site를 연결**해주어야 합니다. 이 과정을 통해 Azure Virtual WAN 허브와 AWS 간의 **IPSec 터널이 실제로 연결**되고, 네트워크 트래픽이 흐를 수 있게 됩니다.

![image.png](../assets/images/annajeong/image%203.png)

### VPN Site Link 수정 – PSK 설정하기

VPN Site 및 Link를 처음 생성할 때, Azure 포털에서는 **PSK(Pre-Shared Key)를 입력하는 항목이 제공되지 않습니다.**

따라서 터널 구성에 필요한 PSK는 **Link 생성 이후에 수동으로 수정하여 입력해야** 합니다.

PSK는 **IPSec 터널의 암호화 및 인증을 위한 핵심 값**으로, AWS 측에서 구성한 값과 반드시 일치해야 합니다.

1. **Azure 포털**에서 **Virtual WAN > VPN Sites > [해당 VPN Site]** 탭으로 이동합니다.
2. 하단의 생성된 **Site**를 선택하고, 해당 항목 오른쪽의 설정 버튼에서 `Edit VPN connection to this Hub` 버튼을 클릭합니다.
3. **각 링크 탭에서 Pre-shared key (PSK)** 항목에 AWS Site-to-Site VPN 구성 시 사용한 **Pre-shared key 값을 정확히 입력**합니다.
4. BGP 설정 등 필요한 값도 함께 검토한 후 **저장(Save)** 을 클릭합니다.
5. 정상적으로 구성이 완료되었다면 Connectivity status가 `Connected`로 변경됩니다.
    
    ![image.png](../assets/images/annajeong/image%204.png)
    

### 마무리하며

이번 포스팅에서는 **Azure Virtual WAN과 AWS를 연결하는 Site-to-Site VPN 구성 방법**을 단계별로 살펴보았습니다.

양쪽 클라우드 환경에 각각의 VPN 엔드포인트를 구성하고, IPSec 터널을 통해 안정적이고 안전한 멀티 클라우드 네트워크를 연결하는 과정을 직접 따라 해보셨다면, 이제 복잡한 하이브리드 클라우드 환경에서도 유연하게 네트워크를 설계하실 수 있을 것입니다.

다음 포스팅에서는 **라우팅 구성**, **연결 상태 모니터링**, 그리고 **트러블슈팅 팁**까지 이어서 다룰 예정이니, 멀티 클라우드 네트워크 운영이 궁금하신 분들은 계속해서 관심 가져주세요!

**[참조]**

- Virtual Hub S2S VPN 구성 : [https://learn.microsoft.com/ko-kr/azure/virtual-wan/virtual-wan-site-to-site-portal](https://learn.microsoft.com/ko-kr/azure/virtual-wan/virtual-wan-site-to-site-portal)
- 가상 네트워크의 VPN Gateway 구성 :  [https://learn.microsoft.com/ko-kr/azure/vpn-gateway/vpn-gateway-howto-aws-bgp](https://learn.microsoft.com/ko-kr/azure/vpn-gateway/vpn-gateway-howto-aws-bgp)