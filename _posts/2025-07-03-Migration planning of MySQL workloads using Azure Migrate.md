---
layout: post
title:  "Azure Migrate를 활용한 MySQL 워크로드 마이그레이션 계획 수립"
author: jyseong
tag: [ Azure Migrate, Data, Infrastructure , Update ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-03-Migration planning of MySQL workloads using Azure Migrate/header.png
---

### 작성자 : [ankitsurkar](https://techcommunity.microsoft.com/users/ankitsurkar/1930507)
### 원본 : [Migration planning of MySQL workloads using Azure Migrate](https://techcommunity.microsoft.com/blog/azuremigrationblog/migration-planning-of-mysql-workloads-using-azure-migrate/4418623)

### MySQL 워크로드의 Azure로의 원활한 마이그레이션을 지원하기

Azure Migrate에서 OSS 워크로드의 지원 범위를 확대하기 위한 노력의 일환으로, Windows 및 Linux 서버에서 실행 중인 MySQL 데이터베이스에 대한 디스커버리 및 현대화 평가 기능을 새롭게 발표합니다. 기존에는 고객들이 MySQL 워크로드에 대한 가시성이 제한적이었고, 일반적인 VM 리프트 앤 시프트 방식의 권장 사항만을 받는 경우가 많았습니다. 이번 기능을 통해 고객은 이제 MySQL 워크로드를 정확하게 식별하고, **Azure Database for MySQL**로 적절하게 사이징하여 평가할 수 있게 되었습니다.

MySQL 워크로드는 LAMP 스택의 핵심 요소로, 안정성, 성능, 사용 편의성을 바탕으로 수많은 웹 애플리케이션을 지원해 왔습니다. 비즈니스가 성장함에 따라 확장 가능하고 효율적인 데이터베이스 솔루션에 대한 수요는 더욱 중요해지고 있습니다. 바로 이 지점에서 Azure Database for MySQL이 중요한 역할을 합니다. 온프레미스 환경에서 Azure Database for MySQL로 마이그레이션하면 다음과 같은 다양한 이점을 누릴 수 있습니다: 손쉬운 확장성, 비용 효율성, 향상된 성능, 강력한 보안, 높은 가용성, 그리고 다른 Azure 서비스와의 원활한 통합. 완전 관리형 Database-as-a-Service(DBaaS)로서, 데이터베이스 관리의 복잡성을 줄여주며 기업이 혁신과 성장에 집중할 수 있도록 지원합니다.

## Azure Migrate란 무엇인가요?
[Azure Migrate](https://learn.microsoft.com/azure/migrate/migrate-services-overview)는 온프레미스 인프라(서버, 데이터베이스, 웹 애플리케이션 등)를 Azure의 Platform-as-a-Service(PaaS) 및 Infrastructure-as-a-Service(IaaS) 대상으로 대규모로 이전하는 여정을 간소화하기 위해 설계된 종합 허브입니다. 이 플랫폼은 통합된 도구 및 기능 모음을 제공하여 최적의 마이그레이션 경로를 식별하고, Azure 적합성을 평가하며, Azure에서 워크로드를 호스팅하는 데 드는 비용을 예측하고, 최소한의 다운타임과 리스크로 마이그레이션을 실행할 수 있도록 지원합니다.

## Azure Migrate의 MySQL 디스커버리 및 평가 주요 기능

Azure Migrate의 새로운 MySQL 디스커버리 및 평가 기능(프리뷰)은 여러 강력한 기능을 제공합니다:

- **MySQL 데이터베이스 인스턴스 디스커버리**: 이 도구는 사용자의 환경 내에서 MySQL 인스턴스를 효율적으로 탐색할 수 있도록 지원합니다. 이러한 인스턴스의 핵심 속성을 식별함으로써, 정밀한 평가와 전략적인 마이그레이션 계획 수립을 위한 기반을 마련합니다.

- **Azure 적합성 평가**: 이 기능은 MySQL 데이터베이스 인스턴스가 Azure Database for MySQL – Flexible Server로 마이그레이션할 준비가 되어 있는지를 평가합니다. 평가 과정에서는 호환성 및 성능 지표 등 다양한 요소를 고려하여 원활한 전환을 보장합니다.

- **SKU 추천**: 디스커버리된 데이터를 기반으로, Azure Database for MySQL에서 MySQL 워크로드를 호스팅하기 위한 최적의 컴퓨팅 및 스토리지 구성을 추천합니다. 또한 관련 비용에 대한 인사이트를 제공하여 보다 효과적인 재무 계획 수립을 지원합니다.

## 시작방법
Azure Migrate에서 MySQL 디스커버리 및 평가 기능을 사용하려면 다음의 5단계 온보딩 절차를 따라주세요:

1. **Azure Migrate 프로젝트 생성**: Azure 포털에서 프로젝트를 설정하여 마이그레이션 여정을 시작합니다.
2. **Azure Migrate 어플라이언스 구성**: Windows 기반 어플라이언스를 사용하여 서버 인벤토리를 디스커버리하고, 워크로드 탐색을 위한 게스트 자격 증명과 MySQL 데이터베이스 인스턴스 및 속성 정보를 가져오기 위한 MySQL 자격 증명을 제공합니다.
3. **디스커버리된 인벤토리 검토**: 탐색된 MySQL 인스턴스의 상세 속성을 확인합니다.
4. **평가 생성**: Azure Database for MySQL로의 마이그레이션 준비 상태를 평가하고, 상세한 권장 사항을 확인합니다.

자세한 단계별 가이드는 디스커버리 및 평가 튜토리얼에 대한 문서를 참고하세요.

참고문서:
- [Discover MySQL databases running in your datacenter](https://learn.microsoft.com/en-us/azure/migrate/tutorial-discover-mysql-database-instances?view=migrate-classic)
- [Assess MySQL database instances for migration to Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/migrate/assessments-overview-migrate-to-azure-db-mysql?view=migrate-classic)

## 피드백을 공유해주세요!
Azure Migrate의 MySQL 디스커버리 및 평가 기능은 MySQL 데이터베이스 마이그레이션을 Azure로 손쉽게 탐색하고, 평가하며, 계획할 수 있도록 지원합니다. 현재 공개 프리뷰로 제공되고 있으니 직접 사용해보시고, 마이그레이션 여정을 빠르게 시작해보세요!

문의 사항이나 피드백, 제안이 있으신 경우 아래 댓글로 남겨주시거나, AskAzureDBforMySQL@service.microsoft.com 으로 직접 연락해 주세요. 여러분의 의견을 듣고 Azure로의 여정을 지원해드릴 수 있기를 기대합니다.

----------

- 2025년 5월 29일 업데이트 됨.
- 2025년 7월 3일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))