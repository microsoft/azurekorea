---
layout: post
title:  "Azure에서 제공하는 DB 옵션 확인인"
author: yorha
tag: [ Azure DB ]
category: [ Solution ]
image: assets/images/thumnails/azurestorageoptions.jpg
---

이번 블로그 포스팅은 다음 링크의 내용을 편집 및 각색하였습니다.  
링크 : [데이터 옵션](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-options) 

클라우드 도입을 위한 랜딩존 환경을 준비할 때, 애플리케이션이 사용할 데이터 요구사항 정리가 필요합니다.
랜딩존 환경을 데이터 요구 사항에 맞게 구성하는 방법은 워크로드 관리 요구사항 그리고 기술적 및 비즈니스 관점의 요구사항에 따라 달라질 수 있습니다.

데이터 서비스 요구사항 파악하기
-------------
랜딩존을 배포하기 전 준비하는 단계에서, 애플리케이션이 필요로 하는 데이터 서비스를 먼저 파악해야 합니다. 파악한 필요사항을 문서화한 후 이 부분을 정책으로 적용시켜서 허용한 리소스만 배포하도록 가드레일 정책으로 제한할 수 있습니다.

요구사항을 파악하기 위해 활용할 수 있는 질문
-------------
**OS와 데이터베이스 엔진을 어느 정도로 컨트롤 하길 원하는가?**  
일부 시나리오는 소프트웨어와 호스트 자체에 대해서 높은 수준의 제어권을 필요로 합니다. 이 경우 IaaS 기반 옵션을 고려할 수 있습니다. 만약 소프트웨어와 호스트단에 대한 제어는 필요로 하지 않지만, 아직 PaaS 옵션을 고려하기에는 시기상조라고 판단한다면 managed instance를 고려할 수 있습니다. Managed instance를 사용하게 되면 온프레미스 데이터베이스 엔진과 높은 호환성을 제공하면서도 관리형 플랫폼의 이점을 누릴 수 있습니다.

**관계형 데이터베이스를 사용할 것인가?**  
Azure는 Azure SQL Database, MySQL, PostgreSQL 그리고 MariaDB와 같은 관리형 PaaS 데이터베이스 제품을 제공합니다. Azure CosmosDB는 MongoDB와 PostgreSQL api를 제공하면서 자동 고가용성 확보 및 즉각적인 스케일링같은 이점을 누릴 수 있습니다.

**SQL 서버를 사용할 것인가?**  
Azure에서는 VM 기반의 SQL Server 혹은 PaaS 기반의 Azure SQL Database를 지원합니다. 두 옵션을 나누는 가장 중요한 판단 요소는 데이터베이스를 직접 관리할 것인지, 패치, 백업 등 관리 요소를 직접 관리 혹은 Azure에 위임할 것인지에 따릅니다. 일부 시나리오에서는 호환성 이슈가 있어서 IaaS 기반의 SQL Server만 사용해야 하는 경우도 종종 있습니다.

**Key-value 데이터베이스 스토리지를 사용할 것인가?**  
Azure Cache for Redis를 사용하거나 혹은 일반적인 성능 수준만 필요한 경우 Azure Cosmos DB도 고려하라 수 있습니다.

**도큐먼트 혹은 그래프 데이터를 사용할 것인가?**  
Azure Cosmos DB는 다양한 데이터 타입과 api를 지원하는 멀티모델 데이터베이스 서비스입니다. Azure Cosmos DB는 또한 도큐먼트 및 그래프 데이터를 지원합니다. Mongo DB와 Apache Gremlin은 Cosmos DB에서 지원하는 도큐먼트 및 그래프 API입니다.

**column-family 데이터를 사용할 것인가?**  
Azure Managed Instance for Apache Cassandra는 온프레미스 데이터센터를 클라우드로 확장시키거나 클라우드 유일 클러스터로 사용할 수 있는 완전 관리형 Apache Cassandra 클러스터를 제공합니다.

**대용량의 데이터 분석 기능을 필요로 하는가?**  
그렇다면 Azure Synapse Analytics를 고려할 수 있습니다. 페타바이트 단위의 정형 데이터를 저장 및 쿼리할 수 있습니다.
비정형의 빅데이터 워크로드는 Azure Data Lake서비스를 이용할 수 있습니다.

**시계열 데이터를 사용할 것인가?**  
IoT 디바이스에서 생성한 시계열 데이터 같은 경우, Azure Time Series Insights를 통해 데이터를 저장, 시각화 및 쿼리할 수 있습니다.

데이터베이스 기능 비교
-------------

| **기능**                              | Azure SQL Database               | Azure SQL Managed Instance            | Azure Database for PostgreSQL                    | Azure Database for MySQL                         | Azure Database for MariaDB       | Azure Managed Instance for Apache Cassandra         | Azure Cosmos DB                  | Azure Cache for Redis                                                 | Azure Cosmos DB for MongoDB      |
|:----------------------------------------:|:--------------------------------:|:-------------------------------------:|:------------------------------------------------:|:------------------------------------------------:|:--------------------------------:|:---------------------------------------------------:|:--------------------------------:|:---------------------------------------------------------------------:|:--------------------------------:|
| **데이터베이스 타입**                        | Relational                       | Relational                            | Relational                                       | Relational                                       | Relational                       | NoSQL                                               | NoSQL                            | In-memory                                                             | NoSQL                            |
| **데이터 모델**                           | Relational                       | Relational                            | Relational                                       | Relational                                       | Relational                       | Multimodel: Document, Wide-column, Key-value, Graph | Wide-column                      | Key-value                                                             | Document                         |
| **분산된 멀티마스터의 쓰기 지원**       | No                               | No                                    | No                                               | No                                               | No                               | Yes                                                 | Yes                              | Yes (Enterprise and Flash tiers only)                                 | Yes                              |
| **가상네트워크 연결성 지원** | Virtual network service endpoint | Native virtual network implementation | Virtual network injection (flexible server only) | Virtual network injection (flexible server only) | Virtual network service endpoint | Native virtual network implementation               | Virtual network service endpoint | Virtual network injection (Premium, Enterprise, and Flash tiers only) | Virtual network service endpoint |
| 


