---
layout: post
title:  "앱 서비스(App Service) 인바운드 IPv6 지원(IPv6 Support) 정식 공개(General Availability)"
author: jyseong
tag: [ Azure App Service , IPv6 ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-09-03-Announcing General Availability of App Service Inbound IPv6 Support/appserviceipv6.png
---

### 작성자 : [jordanselig](https://techcommunity.microsoft.com/users/jordanselig/1185852)
### 원본 : [Announcing General Availability of App Service Inbound IPv6 Support](https://techcommunity.microsoft.com/blog/appsonazureblog/announcing-general-availability-of-app-service-inbound-ipv6-support/4423358)

공용 멀티 테넌트 앱 서비스(App Service)에서의 인바운드 IPv6 지원(Inbound IPv6 Support)은 한동안 [공개 미리 보기(Public Preview)](https://azure.github.io/AppService/2024/11/08/Announcing-Inbound-IPv6-support) 상태였으나, 이제 모든 공용 Azure 지역(Azure Regions), Azure Government, 그리고 21Vianet에서 운영하는 Microsoft Azure에서 멀티 테넌트 앱(Multi-tenant Apps)에 대해 [정식 공개(General Availability)](https://azure.microsoft.com/en-us/updates/?id=499998)되었습니다. 해당 기능은 모든 Basic, Standard, Premium SKU, Functions 소비 요금제(Functions Consumption), Functions 탄력적 프리미엄(Functions Elastic Premium), Logic Apps 표준(Logic Apps Standard) 등의 SKU에서 모두 지원 됩니다. 이전 블로그 게시물에서 언급된 제약 사항은 대부분 해결되었으며, 현재로는 IP-SSL IPv6 바인딩(IP-SSL IPv6 Bindings)미지원이 유일한 제약 사항입니다.

## 동작 방식  
IPv6 인바운드(Inbound)를 사용하려면 두 가지가 필요합니다. 
- 트래픽을 수신할 수 있는 IPv6 주소(IPv6 Address)
- IPv6(AAAA) 레코드를 반환하는 DNS 레코드(DNS Record)입니다.

또한 IPv6 트래픽을 송수신할 수 있는 클라이언트(Client)도 필요합니다. 오늘날 아직은 많은 네트워크가 IPv4만 지원하기 때문에, 로컬 머신에서 테스트가 어려울 수도 있습니다.  

모든 스탬프(배포 단위, Deployment Units)에는 IPv6 주소가 추가되어 있어, IPv4와 IPv6 주소 모두로 트래픽을 전송할 수 있습니다. 하위 호환성을 보장하기 위해 기본 호스트 이름(app-name.azurewebsites.net)에 대한 DNS 응답은 IPv4 주소만 반환합니다. 이를 변경하려면 IPMode라는 사이트 속성(Site Property)을 IPv6 또는 IPv4AndIPv6로 설정할 수 있습니다. IPv6 전용으로 설정하면, 클라이언트는 응답을 받기 위해 IPv6를 "이해"해야 합니다. IPv4AndIPv6로 설정하면 기존 클라이언트는 IPv4를 사용하고, IPv6를 지원하는 클라이언트는 IPv6를 사용할 수 있습니다.  

클라이언트가 IPv6를 지원한다면, 다음과 같이 curl을 사용해 IPv6 연결을 테스트할 수 있습니다:  

```bash
curl -6 https://<app-name>.azurewebsites.net
```

사용자 지정 도메인(Custom Domain)을 사용하는 경우에도 동일한 방식으로 사용자 지정 DNS 레코드(DNS Records)를 정의할 수 있습니다. IPv6(AAAA) 레코드만 추가하면, 클라이언트는 반드시 IPv6를 지원해야 합니다. IPv4와 IPv6를 모두 추가할 수도 있으며, 이 경우 사이트의 기본 호스트 이름(Default Hostname)에 대한 CNAME을 사용할 수 있습니다. 이렇게 설정하면 IPMode의 동작 방식이 적용됩니다.


```
IPMode는 DNS 전용 기능(DNS-only Feature)입니다. 중요한 점은, IPv6가 이제 광범위하게 제공되므로 **구성된 IPMode와 관계없이** 모든 앱 서비스(App Service) 사이트는 IPv4와 IPv6 엔드포인트(Endpoints)를 통해 요청을 받을 수 있다는 것입니다.  

IPMode는 오직 DNS가 엔드포인트를 어떻게 해석하는지에만 영향을 주며, 따라서 DNS 해석(DNS Resolution)에 의존하는 클라이언트(대부분의 클라이언트)에 영향을 줍니다. 그러나 IPMode는 어떤 프로토콜 엔드포인트에 접근할 수 있는지를 제한하지는 않습니다.  
```

이 기능을 더 자세히 살펴보려면 [앱 서비스(App Service) 인바운드 IPv6 문서(App Service inbound IPv6 documentation)](https://aka.ms/app-service-inbound-ipv6)를 참고하세요.

## 향후 계획  
- **곧 제공 예정!** - Linux(멀티 테넌트)용 IPv6 비-VNet 아웃바운드 지원(Outbound Support) 공개 미리 보기(Public Preview) ([Windows는 이미 공개 미리 보기 중](https://techcommunity.microsoft.com/blog/appsonazureblog/announcing-app-service-outbound-ipv6-support-in-public-preview/4423368))  
- **백로그(Backlog)** - IPv6 VNet 아웃바운드 지원(멀티 테넌트 및 App Service Environment v3)  
- **백로그(Backlog)** - IPv6 VNet 인바운드 지원(App Service Environment v3 - 내부 및 외부 모두)  

----------

- 2025년 8월 13일 업데이트 됨.
- 2025년 9월 3일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))