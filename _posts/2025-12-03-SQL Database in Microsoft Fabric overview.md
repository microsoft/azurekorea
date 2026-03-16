---
layout: post
title:  "Microsoft Fabric의 SQL Database: 통합 데이터 플랫폼의 새로운 기준개요"
author: jyseong
tag: [ Microsoft Fabric ]
category: [ Solution ]
---

**해당 글은 [Microsoft Fabric의 SQL Database: 통합 데이터 플랫폼의 새로운 기준](https://github.com/jiyongseong/azure-articles/blob/main/2025-12-03-SQL%20Database%20in%20Microsoft%20Fabric%20overview/2025-12-03-SQL%20Database%20in%20Microsoft%20Fabric%20overview.md)에 등록된 글입니다.**

# Microsoft Fabric의 SQL Database: 통합 데이터 플랫폼의 새로운 기준
### 데이터 관리의 혁신, Fabric의 등장
최근 데이터 환경은 점점 더 복잡해지고 있습니다. 다양한 데이터 소스와 엔진, 그리고 각기 다른 포맷의 데이터가 기업 내외에서 생성되고 활용됩니다. 기존에는 데이터 사일로(silo)와 복사본 관리, 변환 작업 등으로 인해 데이터 일관성과 효율성이 저하되는 문제가 많았습니다.
Microsoft Fabric은 이러한 문제를 근본적으로 해결하기 위해 등장한 통합 데이터 플랫폼입니다. Fabric의 중심에는 OneLake라는 단일 데이터 저장소가 있으며, 모든 데이터는 **Delta Parquet** 포맷으로 저장됩니다. 이로 인해 데이터 엔진 간의 변환 작업이 필요 없고, 데이터 복사본 관리와 데이터 드리프트 문제도 크게 줄어듭니다.

### OneLake와 Delta Parquet: 데이터 통합의 핵심
OneLake는 Fabric의 모든 데이터 서비스가 공유하는 저장소입니다. Delta Parquet 포맷은 데이터의 효율적인 저장과 분석을 가능하게 하며, Azure Data Factory, 데이터 엔지니어링, 데이터 과학, Synapse 기반 데이터 웨어하우스, 실시간 분석 엔진(Kusto, Power BI 등) 모두가 OneLake와 직접 통신할 수 있습니다.
이로써 데이터 복사와 변환의 부담이 줄고, 데이터 일관성과 신뢰성이 크게 향상됩니다. 모든 데이터는 **Compute Unit** 이라는 공통 과금 단위로 관리되어, 비용 관리도 단순화됩니다.

### Fabric SQL Database의 주요 특징
#### 1. 서버리스 자동 확장
Fabric SQL Database는 Azure SQL Database 엔진을 기반으로 하며, **서버리스(Serverless) 모드** 로 동작합니다. 서버리스 환경에서는 16~32 vCore 사이에서 자동으로 확장되며, 15분간 비활성 상태가 지속되면 컴퓨트 리소스가 자동으로 중지되어 비용을 절감할 수 있습니다. 저장소는 계속 과금되지만, 사용하지 않는 컴퓨트 비용은 발생하지 않습니다.

#### 2. 간편한 생성과 관리
Fabric 포털에서 "Create" 버튼을 클릭하고, "SQL Database"를 선택한 후 이름만 입력하면 데이터베이스가 생성됩니다. API를 사용할 경우에도 3번의 호출이면 완료될 정도로 간편합니다. 생성된 SQL DB는 Microsoft 관리 구독에 생성되므로, 사용자의 Azure 구독에서는 보이지 않습니다.

#### 3. 자동 성능 최적화와 고가용성
Fabric SQL Database는 자동으로 인덱스를 생성하고 튜닝하며, 고가용성(HA)과 재해 복구(DR), 백업까지 모두 자동으로 처리합니다. 생성된 지역이 ZRS(Zone Redundant Storage)를 지원한다면, 데이터는 여러 데이터센터에 분산 저장되어 장애에도 안전하게 보호됩니다. Fabric의 워크스페이스 역할(관리자, 기여자, 뷰어)은 SQL DB의 권한으로 자동 매핑되어 관리가 매우 편리합니다.

#### 4. AI 분석 기능 내장
SQL Database는 AI 준비 완료(AI Ready) 상태로 제공됩니다. 특히 벡터 검색 기능이 내장되어 있어, 자연어 기반의 검색과 **RAG(Retrieval Augmented Generation)** 을 지원합니다. Copilot을 통해 쿼리 작성, 테이블 작업 등도 자연어로 수행할 수 있어, 데이터 분석과 활용이 훨씬 쉬워집니다.

### HTAP(하이브리드 트랜잭션/분석 처리) 구조와 실시간 분석
Fabric SQL Database는 HTAP(Hybrid Transactional Analytical Processing) 구조를 지원합니다. 트랜잭션 엔드포인트를 통해 데이터 쓰기 및 운영을 처리하고, Delta Parquet 기반 OneLake와 연결된 분석 엔드포인트를 통해 실시간으로 데이터를 분석할 수 있습니다. 운영과 분석이 분리되지 않고, 실시간으로 데이터가 미러링되어 최신 데이터를 활용할 수 있습니다.
예를 들어, 고객 데이터를 트랜잭션 엔드포인트에서 수정하면, 분석 엔드포인트에서도 거의 실시간으로 반영됩니다. 이를 통해 운영 데이터와 분석 데이터의 일관성을 유지하면서, 빠른 의사결정과 인사이트 도출이 가능합니다.

### 외부 데이터 연동과 확장성
Fabric은 외부 데이터와의 연동도 매우 유연합니다. Shortcut 기능을 통해 Parquet 데이터도 복사 없이 연결할 수 있고, Mirroring을 통해 전통적인 데이터베이스의 데이터를 OneLake에 복사해 사용할 수 있습니다. 또한, Cross-Database Query를 통해 여러 데이터베이스 간 조인과 통합 분석도 가능합니다. 다양한 데이터 소스와의 통합이 매우 쉬워졌습니다.

### 과금 및 라이선스 모델
Fabric SQL Database는 Capacity Unit(CU) 기준으로 과금됩니다. 컴퓨트 비용은 자동으로 계산되며, 15분간 비활성 상태가 지속되면 자동으로 중지되어 비용을 절감할 수 있습니다. 스토리지 비용은 지속적으로 과금되며, 백업 비용은 별도로 과금됩니다.
예를 들어, Pay-as-you-go F2(2 CU) 기준 월 $263부터 시작하며, 용량에 따라 과금이 달라집니다. 모든 자동 관리 기능이 포함되어 있어, 복잡한 비용 관리 없이 효율적으로 운영할 수 있습니다.

### 개발 및 운영 환경
Fabric SQL Database는 다양한 개발 도구와 운영 환경을 지원합니다.
- T-SQL, SSMS, VS Code, Python 등 다양한 개발 도구를 사용할 수 있습니다.
- 웹 기반 쿼리 에디터도 제공되어, 별도의 설치 없이 바로 쿼리 작업이 가능합니다.
- SQL Analytics Endpoint를 통해 분석 쿼리를 실행할 수 있으며, Power BI와 직접 연동해 실시간 데이터 시각화도 가능합니다.

### 보안 및 권한 관리
Fabric SQL Database는 Entra ID 인증을 기반으로 하며, Fabric 워크스페이스의 역할(관리자, 기여자, 뷰어)이 SQL DB의 권한으로 자동 매핑됩니다. Private Endpoint는 현재 테넌트 수준에서만 가능하며, 워크스페이스 수준 지원은 로드맵에 포함되어 있습니다.
Copilot을 통해 쿼리 작성, 테이블 작업 등도 지원되어, 보안과 관리가 더욱 강화됩니다.

### 실제 활용 시나리오
Fabric SQL Database는 다음과 같은 다양한 시나리오에서 활용될 수 있습니다.
- 앱 개발자: 복잡한 설정 없이 SQL 인스턴스를 빠르게 생성하고, 운영과 분석을 동시에 처리할 수 있습니다.
- 데이터 분석가: 실시간 데이터 분석과 시각화, AI 기반 자연어 검색 및 분석이 가능합니다.
- 엔터프라이즈 환경: 다양한 데이터 소스와의 통합, 자동 확장, 고가용성, 재해 복구 등 엔터프라이즈급 요구사항을 충족합니다.
- AI/ML 프로젝트: 벡터 검색과 RAG 기능을 활용해 자연어 기반 AI 분석 및 응용이 가능합니다.

### Fabric SQL Database의 가치와 미래
Microsoft Fabric의 SQL Database는 배포와 관리가 간편하고, 자동 확장, 자동 성능 최적화, AI 분석 기능 내장, 효율적인 과금 모델 등 다양한 장점을 갖춘 차세대 데이터베이스 솔루션입니다.
현재는 Preview 상태이므로, 직접 사용해보며 데이터 전략에 적합한지 평가해볼 수 있습니다.
향후 워크스페이스 수준 Private Endpoint, 기능 확장, 성능 개선 등 다양한 업데이트가 예정되어 있어, 데이터 관리와 분석의 미래를 이끌어갈 핵심 플랫폼으로 자리잡을 것입니다.

## 참고 자료
- [SQL database in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/database/sql/overview)
- [What is the SQL analytics endpoint for a SQL database in Fabric?](https://learn.microsoft.com/en-us/fabric/database/sql/sql-analytics-endpoint)

----------

- 2025년 12월 3일 작성 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))