---
layout: post
title:  "VNET 및 프라이빗 엔드포인트 뒤에 배치된 Azure Database for PostgreSQL Flexible Server 미러링"
author: jyseong
tag: [ Azure Database for PostgreSQL , Mirroring ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-08-27-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoin/show-private-link-overview.jpg
---

### 작성자 : [scoriani](https://techcommunity.microsoft.com/users/scoriani/218343)
### 원본 : [Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoint](https://techcommunity.microsoft.com/blog/adforpostgresql/mirroring-azure-database-for-postgresql-flexible-server-behind-vnet-and-private-/4432401)

Microsoft Fabric은 VNET 통합 또는 프라이빗 엔드포인트 뒤에 배포된 Azure Database for PostgreSQL Flexible Server 인스턴스로의 미러링 기능을 지원하게 되었습니다.

Microsoft Fabric은 퍼블릭 프리뷰(public preview)로 Azure Database for PostgreSQL Flexible Server에 대한 미러링 기능을 지원하게 되었습니다. 이 기능은 VNET 통합 또는 프라이빗 엔드포인트 뒤에 배포된 서버 인스턴스에도 사용할 수 있습니다.
이번 기능 향상은 Fabric의 실시간 데이터 복제 기능의 적용 범위를 크게 확장하며, 네트워크로 격리된 환경에서도 안전하고 원활한 트랜잭션 데이터 분석을 가능하게 합니다.

# Fabric 미러링이란?
Fabric 미러링은 저지연, 저비용의 데이터 복제 솔루션으로, 운영 데이터베이스의 데이터를 Microsoft Fabric의 OneLake로 지속적으로 동기화합니다.
PostgreSQL Flexible Server의 경우, 선택된 테이블을 Delta 형식으로 거의 실시간으로 복제함으로써, 트랜잭션 워크로드에 영향을 주지 않고 고급 분석, AI, 리포팅을 수행할 수 있도록 지원합니다.

# VNET 및 프라이빗 엔드포인트 지원이 중요한 이유
많은 엔터프라이즈 고객들이은 Azure Database for PostgreSQL Flexible Server 인스턴스를 Azure Virtual Network(VNET) 내에 배포하거나, 프라이빗 엔드포인트를 구성하여 격리된 네트워크 환경에서 데이터베이스에 연결하고 있습니다.
지금까지는 퍼블릭 엔드포인트에 접근 가능한 PostgreSQL Flexible Server만 미러링이 가능했지만, 이번 업데이트를 통해 데이터 보안이나 컴플라이언스 요건을 위배하지 않으면서, VNET 또는 프라이빗 엔드포인트로 보호된 보안 네트워크 환경에 호스팅된 데이터베이스도 미러링할 수 있게 되었습니다.

이 기능은 [VNET Data Gateway](https://learn.microsoft.com/en-us/data-integration/vnet/overview)와의 통합을 통해 구현되었으며, 이를 통해 Fabric의 프론트엔드 서비스가 퍼블릭 노출이나 복잡한 네트워크 재구성 없이 PostgreSQL 서버에 안전하게 연결할 수 있습니다.

해당 기능에 대한 테스트 방법은 [공식 문서](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/azure-database-postgresql-tutorial)를 참고하시기 바랍니다.

VNET 또는 프라이빗 엔드포인트 뒤에 배치된 PostgreSQL Flexible Server를 미러링하기 위한 첫 번째 단계는, Microsoft Fabric 테넌트에서 VNET Data Gateway를 생성하는 것입니다.

![manage connection and gateways](../assets/images/jyseong/images/2025-08-27-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoin/manageconnectionandgateways.png)

그다음에는, 해당 패널에서 "가상 네트워크 게이트웨이 생성(Create a virtual network gateway)" 버튼을 클릭하여, Flexible Server가 배포된 Azure Virtual Network의 세부 정보와 Fabric 용량 정보를 입력하면 됩니다.
또는 해당 Azure Virtual Network에 대해 이미 존재하는 VNET 데이터 게이트웨이를 사용할 수도 있습니다.

![new vnet data gateway](../assets/images/jyseong/images/2025-08-27-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoin/newvnetdatagateway.png)

Fabric에서 미러링된 PostgreSQL 데이터베이스를 생성의 마지막 단계는 다음과 같습니다.
"새 소스(New source)" 페이지에서, 이제 Microsoft Fabric 테넌트에 이미 존재하며 동일한 Azure Virtual Network 내의 Azure Database for PostgreSQL에 접근 가능한 데이터 게이트웨이를 선택할 수 있습니다.

![new source](../assets/images/jyseong/images/2025-08-27-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoin/newsource.png)

이 작업이 완료되면, Microsoft Fabric 서비스는 프라이빗 연결을 통해 데이터 게이트웨이를 거쳐 PostgreSQL Flexible Server에 접속하며, 미러링 아티팩트의 생성을 지속적으로 수행합니다.
초기 스냅샷과 이후의 변경 배치들은 예상대로 PostgreSQL Flexible Server에서 Microsoft Fabric의 OneLake로 정기적으로 전송됩니다.

# 다음 단계
VNET 및 프라이빗 엔드포인트 지원이 완료됨에 따라, 팀은 이제 고가용성(HA)이 활성화된 PostgreSQL 서버에 대한 미러링 기능 지원에 집중하고 있습니다.
이는 많은 엔터프라이즈 고객들이 요청한 핵심 기능 중 하나입니다.
정식 출시(General Availability)를 향해 나아가는 과정에서의 업데이트를 계속 지켜봐 주세요!

----------

- 2025년 7월 15일 업데이트 됨.
- 2025년 8월 27일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))