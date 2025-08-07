---
layout: post
title:  "Azure Landing Zone에서 DNS best practice 구현하기"
author: jyseong
tag: [ Azure Networking ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-01-DNS best practices for implementation in Azure Landing Zones/New-Azure-Private-DNS.png
---

### 작성자 : [AshishRana](https://techcommunity.microsoft.com/users/ashishrana/2842247)
### 원본 : [DNS best practices for implementation in Azure Landing Zones](https://techcommunity.microsoft.com/blog/azurenetworkingblog/dns-best-practices-for-implementation-in-azure-landing-zones/4420567)

### 이 블로그 게시물에서는 Azure에서 사용할 수 있는 다양한 DNS 구성 요소들(Private DNS Zone, DNS Private Resolvers, DNS Forwarding Rulesets, Conditional Forwarders 등)을 설명하고, 엔터프라이즈급 Azure Landing Zone에 적합한 구조를 위한 구성 방식과 확장성·보안을 모두 고려한 설계에 대해서 살펴봅니다. 가상 네트워크를 구성할 때 사용자 지정 DNS 설정을 어디로 지정해야 하는지(예: 온-프레미스 도메인 컨트롤러, Azure DNS 프라이빗 리졸버 엔드포인트 등) 곤란한 상황을 겪는 경우가 많습니다. 이런 혼선을 줄이기 위해 일반적인 설계 패턴을 살펴보고, 엔터프라이즈 환경에서 DNS를 확장 가능하고 체계적으로 구성하는 방법에 대해서 살펴보게 됩니다.

## 랜딩 존(Landing Zone)에서 DNS 아키텍처가 중요한 이유
DNS 계층을 잘 설계하면, 구독이 서로 다르더라도 워크로드 간의 이름 해석이 빠르고 안전하게 이루어집니다. DNS는 이처럼 다양한 시스템을 유기적으로 연결해주는 핵심 역할을 합니다.
Azure Landing Zone을 구축할 때 DNS를 올바르게 설계해 두면, 향후에 따로 수정하지 않고도 제로 트러스트(Zero-Trust) 보안 모델이나 허브-앤-스포크(hub-and-spoke) 네트워크 구조 같은 복잡한 네트워크 아키텍처를 문제없이 운영할 수 있습니다.

## 전형적인 Landing Zone 토폴로지

| 구독 | 역할 | 주요 리소스 |
| :-------- | :------- | :------- |
| Connectivity (Hub) | Transit, 라우팅, 공유 보안 | 허브(Hub) VNet, Azure Firewall / NVA, VPN/ER 게이트웨이, Private DNS Resolver |
| Security | 보안 도구 및 SOC | Sentinel, Defender, Key Vault (HSM) |
| Shared Services | 조직 전체 공유 앱 | ADO 및 에이전트, 자동화 |
| Management | 운영 및 거버넌스 | Log Analytics, 백업 등 |
| Identity | 디렉터리 및 인증 서비스 | 확장된 도메인 컨트롤러, Azure AD DS |

위에 나열된 다섯 개 구독 각각에 VNet이 하나씩 존재하며, Security, Shared, Management, Identity 구독은 모두 Connectivity VNet과 피어링(peering)되어 클래식한 허브-앤-스포크(hub-and-spoke) 구조를 이룹니다.

## 모든 DNS 트래픽이 방화벽을 반드시 통과하도록 강제하는 아키텍처
**목표**: 각 spoke에서 발생하는 모든 네트워크 통신(예: DNS 포함)을 허브의 방화벽을 무조건 통하게 함.

| 구성 요소                    | 권장 구성                                                                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------------- |
| **Private DNS Zones**    | 연결을 Connectivity VNet에만 연결합니다. Spoke VNet은 직접 연결하지 않습니다.                                                 |
| **Private DNS Resolver** | 허브(Connectivity VNet)에 인바운드 및 아웃바운드 엔드포인트를 배포합니다. 연결 VNet은 아웃바운드 엔드포인트에 연결합니다.                           |
| **Spoke DNS 설정**         | 각 spoke VNet에 사용자 지정 DNS 서버로 인바운드 엔드포인트 IP를 지정합니다.                                                       |
| **Forwarding Ruleset**   | 아웃바운드 엔드포인트에 연관된 규칙 집합 생성 후 포워더 추가:<br>- 특정 도메인 → 온-프레미스 / 외부 서버<br>- 와일드카드 “.” → 온-프레미스 DNS (컴플라이언스 목적) |
| **Firewall 규칙**          | Spoke → Resolver-inbound 간 UDP/TCP 53, 그리고 Resolver-outbound → 대상 DNS 서버 간 UDP/TCP 53을 허용합니다.            |


**참고 사항:**

Azure private DNS Zone은 글로벌 리소스로, 여러 리전에 배포된 리소스에 대한 DNS 조회를 하나의 존으로 해결할 수 있습니다.

DNS private resolver는 지역(리전) 리소스이므로 동일 리전에 있는 VNet에만 연결할 수 있습니다.

## 트래픽 흐름

1. Spoke VM → 인바운드 엔드포인트 (허브)
2. 방화벽은 UDR(사용자 정의 라우팅) 설정에 따라 트래픽을 가로채서 먼저 검사한 후 인바운드 엔드포인트로 전달합니다.
바운드 엔드포인트로 들어온 요청 중 로컬에서 해결되지 않은 DNS 쿼리는, 리졸버가 전달 3. 규칙을 적용하여 아웃바운드 엔드포인트를 통해 외부 DNS 서버로 전송합니다.

DNS 전달 규칙 집합(DNS forwarding rulesets)은 특정 DNS 네임스페이스를 지정된 사용자 지정 DNS 서버로 라우팅할 수 있게 해줍니다.

## 인터넷으로 폴백(Fallback) 및 NXDOMAIN 리디렉션
Azure Private DNS는 하이브리드 및 멀티 테넌트 환경에서 이름 해석 유연성을 높일 수 있는 두 가지 강력한 기능을 지원합니다:

**인터넷으로 폴백 (Fallback to internet)**

**목적**: 프라이빗 DNS 존에서 일치하는 레코드를 찾지 못할 경우, 퍼블릭 DNS를 통해 해석할 수 있게 합니다.
**사용 시나리오**: 프라이빗 DNS 존이 모든 호스트 이름을 포함하지 않는 경우(예: 부분 영역 포함 또는 단계적 마이그레이션 등)에 이상적입니다.
**활성화 방법**:
Azure private DNS zones으로 이동 -> zone 선택 -> Virtual netowrk link -> 편집 옵션

![Configuration options](./assets/images/jyseong/images/2025-07-01-DNS best practices for implementation in Azure Landing Zones/image.png)

**참고 문서**: [https://learn.microsoft.com/en-us/azure/dns/private-dns-fallback](https://learn.microsoft.com/en-us/azure/dns/private-dns-fallback)

## 중앙 집중 DNS - 방화벽 검사가 필요하지 않은 경우

**목표**:
DNS 쿼리를 방화벽을 통해 검사하지 않고, 방화벽을 우회하여 처리할 수 있도록 구성합니다.

**구성 방법**:

- 각 spoke 가상 네트워크에서 필요한 **Private DNS Zones**에 직접 연결하여, spoke에서 PaaS 리소스의 이름을 바로 해석할 수 있도록 합니다.

- 온-프레미스 이름 해석이 필요한 경우를 대비해 **Private DNS Resolver**를 하나만 운영할 수 있습니다(선택사항). 각 spoke는 VNet 피어링이나 프라이빗 연결을 통해 이 리졸버의 인바운드 엔드포인트에 접근할 수 있습니다.

- **Spoke 단계의 사용자 지정 DNS** 설정을 통해, identity 가상 네트워크 내에 배치된 확장 도메인 컨트롤러로 직접 포워딩할 수 있습니다.

이 구성은 **지연 시간과 비용을 줄이면서도 DNS zone 관리는 중앙에서 일관되게 유지**할 수 있는 장점이 있습니다.

## 온-프레미스 Active Directory DNS 통합

- 각 도메인 컨트롤러에 **조건부 전달자(Conditional Forwarder)** 를 생성합니다.  
- 각 Private DNS Zone에 대한 쿼리를 **DNS 프라이빗 리졸버의 인바운드 엔드포인트 IP 주소**로 전달하도록 설정합니다.

예시:  
- `blob.core.windows.net`  
- `database.windows.net`

> ※ 이때, `privatelink`라는 문자 그대로의 라벨은 포함하지 않습니다.

---
이 설정을 통해 온-프레미스 Active Directory DNS와 Azure Private DNS가 원활하게 연동됩니다.

![Conditional forwaders](./assets/images/jyseong/images/2025-07-01-DNS best practices for implementation in Azure Landing Zones/image1.png)

**참고 사항**

여러 Azure 구독과 서로 다른 Azure 환경에 배포된 도메인 컨트롤러가 있는 환경에서는  
  **"Store this conditional forwarder in Active Directory and replicate as follows"** 옵션을 선택하지 않는 것이 좋습니다.

> 이 옵션을 사용하면 조건부 전달자가 Active Directory에 저장되고 복제되는데,  
> 복잡한 멀티 구독·멀티 환경에서 문제를 일으킬 수 있습니다.

![Store this conditional forwarder in Active Directory and replicate as follows](./assets/images/jyseong/images/2025-07-01-DNS best practices for implementation in Azure Landing Zones/image2.png)

**참고 문서** : [https://github.com/dmauser/PrivateLink/tree/master/DNS-Integration-Scenarios#43-on-premises-dns-server-conditional-forwarder-considerations](https://github.com/dmauser/PrivateLink/tree/master/DNS-Integration-Scenarios#43-on-premises-dns-server-conditional-forwarder-considerations)

# 주요 내용 요약 (Key Takeaways)

1. **존(zone)을 연결 구독(connectivity subscription)의 가상 네트워크에만 연결**하면 방화벽 검사와 아웃바운드 제어가 단순해집니다.  
2. **Private DNS Resolver와 전달 규칙 집합(forwarding rulesets)** 을 활용하면, 별도의 맞춤형 장비 없이 하이브리드 이름 해석을 유연하게 관리할 수 있습니다.  
3. 방화벽 검사가 필요 없는 경우, 존을 직접 spoke에 연결하면 네트워크 홉 수와 복잡도를 줄일 수 있습니다.  
4. 온-프레미스 Active Directory DNS 통합 시, 조건부 전달자는 인바운드 엔드포인트 IP를 가리켜야 하며, 조건부 전달자 생성 시 `privatelink` 이름은 제외해야 합니다.  
5. 다수 Azure 테넌트에 환경이 분산된 경우에는 조건부 전달자 존을 AD 복제하지 않는 것이 좋습니다.  
6. DNS 설계를 초기에 신중히 계획하고, 인프라 코드(infrastructure-as-code)에 포함시키면, 이후 스포크(spoke)가 몇 개가 늘어나더라도 Landing Zone이 깔끔하게 확장됩니다.

- 2025년 6월 10일 업데이트 됨.
- 2025년 7월 1일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))