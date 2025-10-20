---
layout: post
title:  "SAP Business Data Cloud와 Azure Databricks 연결 기능, 이제 정식 지원(GA)"
author: jyseong
tag: [ azure, azure databricks ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-15-SAP Business Data Cloud Connect with Azure Databricks is now generally available/Announcing the SAP BDC Connector for Azure Databricks OG 1.png
---

### 작성자 : [AnaviNahar](https://techcommunity.microsoft.com/users/anavinahar/803999)
### 원본 : [SAP Business Data Cloud Connect with Azure Databricks is now generally available](https://techcommunity.microsoft.com/blog/analyticsonazure/sap-business-data-cloud-connect-with-azure-databricks-is-now-generally-available/4459490)

SAP Business Data Cloud(SAP BDC) Connect for Azure Databricks가 정식 지원(GA) 되었습니다.
이제 Azure Databricks 고객은 데이터를 복사하지 않고도 SAP BDC 환경을 기존 Azure Databricks 인스턴스에 연결해 양방향 실시간 데이터 공유를 구현할 수 있습니다.

SAP 데이터를 다른 엔터프라이즈 데이터와 연결하면 거버넌스 리스크, 컴플라이언스 문제, 데이터 사일로를 방지할 수 있습니다.
또한 유지 관리 비용이 줄어들고, 수작업으로 의미 체계를 구축할 필요도 없어집니다.
이제 SAP 데이터 제품은 Delta Sharing을 통해 기존 Azure Databricks 인스턴스로 직접 공유할 수 있어, 비즈니스에 필요한 완전한 컨텍스트를 보장합니다.

이제 Azure Databricks와 SAP BDC 전반에 걸쳐서서 데이터 자산을 통합할 수 있습니다.
이를 통해 다음의 내용들이 좀 더 쉬워집니다:

- 거버넌스 강화
- 분석, 데이터 웨어하우징, BI 및 AI 활용

SAP BDC를 Azure Databricks에 연결하는 과정은 간단하면서, 안전하고, 빠르기까지 합니다.이 연결은 신뢰를 기반으로 양쪽 플랫폼에서 승인이 필요하며, 이를 통해 데이터 제품의 양방향 공유가 가능합니다.

승인이 완료되면 SAP BDC의 데이터 제품은 Azure Databricks Unity Catalog에 직접 마운트되며, Delta Sharing을 통해 공유되는 다른 자산과 동일하게 취급됩니다.

이로 인해, 팀은 기존 비즈니스 데이터와 SAP 데이터를 하나의 통합된 방식으로 쿼리하고 분석하며 인사이트를 얻을 수 있습니다.
데이터를 한곳에 모으는 데 시간을 쓰지 않고, 팀은 통합된 데이터에서 빠르고 안전하게 인사이트를 도출하는 데 집중할 수 있습니다.

![demo](../assets/images/jyseong/images/2025-10-15-SAP Business Data Cloud Connect with Azure Databricks is now generally available/Azure-Databricks-Demo.gif)


이번 정식 지원으로 Azure에서 실행되는 SAP BDC 내 SAP Databricks 기능이 더욱 강화됩니다. 이를 통해 SAP 환경 내에서 AI, ML, 데이터 엔지니어링, 데이터 웨어하우징 기능을 직접 활용할 수 있습니다. 또한 Azure에서 실행되는 SAP BDC의 SAP Databricks [지원 지역](https://docs.databricks.com/sap/en/#supported-azure-regions)이 늘어나게 되었습니다.
자세한 내용을 확인하고 시작하려면 SAP BDC Connect with Azure Databricks 문서([Share data between SAP Business Data Cloud (BDC) and Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/sap-bdc/), [Create and manage the SAP Business Data Cloud (BDC) connector](https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/sap-bdc/create-connection))를 참고하시기 바랍니다.

----------

- 2025년 10월 15일 업데이트 됨.
- 2025년 10월 16일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))