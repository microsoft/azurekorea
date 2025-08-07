---
layout: post
title:  "VNET 및 프라이빗 엔드포인트 환경에서 Azure Database for PostgreSQL Flexible Server 미러링"
author: jyseong
tag: [ Azure Database for PostgreSQL ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-28-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoin/show-private-link-overview.png
---

### 작성자 : [scoriani](https://techcommunity.microsoft.com/users/scoriani/218343)
### 원본 : [Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoint](https://techcommunity.microsoft.com/blog/adforpostgresql/mirroring-azure-database-for-postgresql-flexible-server-behind-vnet-and-private-/4432401)

### Microsoft Fabric은 이제 VNET 통합 또는 프라이빗 엔드포인트(Private Endpoint)로 배포된 Azure Database for PostgreSQL Flexible Server 인스턴스에 대한 미러링을 지원합니다.


Microsoft Fabric에서 Azure Database for PostgreSQL Flexible Server에 대한 미러링 기능이 Public Preview로 제공되며, VNET 통합 또는 프라이빗 엔드포인트로 배포된 서버 인스턴스에서도 지원됩니다.
이번 기능 향상은 Fabric의 실시간 데이터 복제 기능의 적용 범위를 크게 확장하며, 네트워크로 격리된 환경에서도 거버넌스가 유지된 안전하고 원활한 트랜잭션 데이터 분석을 가능하게 합니다.

## Fabric Mirroring이란?
Fabric Mirroring은 저지연, 저비용의 데이터 복제 솔루션으로, 운영 데이터베이스의 데이터를 Microsoft Fabric의 OneLake로 지속적으로 동기화합니다.
PostgreSQL Flexible Server의 경우, 선택된 테이블을 Delta 포맷으로 거의 실시간으로 복제할 수 있어, 트랜잭션 워크로드에 영향을 주지 않으면서 고급 분석, AI, 리포팅을 수행할 수 있습니다.

## VNET 및 프라이빗 엔드포인트 지원이 중요한 이유
많은 엔터프라이즈 고객들은 Azure Database for PostgreSQL Flexible Server 인스턴스를 Azure 가상 네트워크(VNET) 내에 배포하거나, **프라이빗 엔드포인트(Private Endpoint)**를 구성하여 격리된 네트워크 환경에서 데이터베이스에 연결하고 있습니다.
지금까지는 퍼블릭 엔드포인트에 접근 가능한 PostgreSQL Flexible Server만 미러링이 가능했지만, 이번 업데이트를 통해 VNET 또는 프라이빗 엔드포인트로 보호된 보안 네트워크 환경에서도 데이터베이스를 미러링할 수 있게 되었습니다.
이를 통해 데이터 보안이나 컴플라이언스를 저해하지 않으면서도 실시간 데이터 복제를 활용한 분석이 가능해졌습니다.

이 기능은 [VNET Data Gateway](https://learn.microsoft.com/en-us/data-integration/vnet/overview)와의 통합을 통해 구현됩니다. 이를 통해 Fabric의 프런트엔드 서비스가 퍼블릭 노출이나 복잡한 네트워크 재구성 없이도 PostgreSQL 서버에 안전하게 연결할 수 있습니다.

이제 [공식 문서](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/azure-database-postgresql-tutorial)에 제공된 튜토리얼을 따라, 여러분의 환경에서 이 기능을 직접 테스트해볼 수 있습니다.

VNET 또는 프라이빗 엔드포인트 뒤에 있는 PostgreSQL Flexible Server를 미러링하기 위한 첫 번째 단계는, 아래 그림과 같이 Microsoft Fabric 테넌트에서 VNET Data Gateway를 생성하는 것입니다.

![VNET Data Gateway](assets/images/jyseong/images/2025-07-28-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoint/Screenshot 2025-07-11 at 5.27.51 PM.png)

이제 이 패널에서 "Create a virtual network gateway" 버튼을 클릭한 후, Fabric 용량 정보와 Flexible Server가 배포된 Azure 가상 네트워크(VNET) 정보를 입력하여 게이트웨이를 생성할 수 있습니다.
또는, 해당 Azure VNET에 대해 이미 생성된 기존 VNET Data Gateway가 있다면 그것을 그대로 사용할 수도 있습니다.


![New VNET Data Gateway](assets/images/jyseong/images/2025-07-28-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoint/Screenshot 2025-07-11 at 5.29.54 PM.png)

마지막 단계는 Fabric에서 미러링할 PostgreSQL 데이터베이스를 생성하는 과정에서 수행됩니다.
"New source(새 소스)" 페이지에서, 이제 Microsoft Fabric 테넌트 내에 존재하며 해당 Azure 가상 네트워크(VNET)에 있는 PostgreSQL 데이터베이스에 접근할 수 있는 Data Gateway를 선택할 수 있습니다.

![Connection](assets/images/jyseong/images/2025-07-28-Mirroring Azure Database for PostgreSQL flexible server behind VNET and Private Endpoint/Screenshot 2025-07-11 at 5.39.57 PM.png)

이 작업이 완료되면, Microsoft Fabric 서비스는 프라이빗 연결을 통해 Data Gateway를 사용하여 PostgreSQL Flexible Server에 연결하며, 미러링 아티팩트 생성을 지속적으로 수행하게 됩니다.
초기 스냅샷과 이후 변경 배치는 예상대로 PostgreSQL Flexible Server에서 Microsoft Fabric의 OneLake로 정기적으로 전송됩니다.

## 다음 단계는 무엇일까요?
이제 VNET 및 프라이빗 엔드포인트 지원이 적용됨에 따라, Microsoft Fabric 팀은 고가용성(HA)이 활성화된 PostgreSQL 서버에 대한 미러링 기능 지원에 집중하고 있습니다. 이는 많은 엔터프라이즈 고객들이 요청한 핵심 기능 중 하나입니다.
**일반 공급(General Availability)**을 향해 나아가는 과정에서, 향후 업데이트를 기대해 주세요!

----------

- 2025년 7월 16일 업데이트 됨.
- 2025년 7월 28일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))