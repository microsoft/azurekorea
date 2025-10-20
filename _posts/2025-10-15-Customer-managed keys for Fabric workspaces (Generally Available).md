---
layout: post
title:  "Fabric 작업 영역에서 고객 관리 키 지원 (정식 지원)"
author: jyseong
tag: [ microsoft fabric ]
category: [ Solution ]
image: https://dataplatformblogwebfd-d3h9cbawf0h8ecgf.b01.azurefd.net/wp-content/uploads/2025/10/image-25.png
---

### 작성자 : [Sumiran Tandon](https://blog.fabric.microsoft.com/en-us/blog/author/Sumiran%20Tandon)
### 원본 : [Customer-managed keys for Fabric workspaces (Generally Available)](https://blog.fabric.microsoft.com/en-us/blog/customer-managed-keys-for-fabric-workspaces-generally-available/)

## 소유하고 관리하는 키로 데이터 보호하기

기본적으로 Fabric은 저장된 모든 데이터를 Microsoft 관리 키로 암호화하고, 전송 중인 데이터는 TLS 1.2 이상을 사용해 보호합니다.
[고객 관리 키(CMK)](https://learn.microsoft.com/ko-kr/fabric/security/workspace-customer-managed-keys)는 사용자가 Azure Key Vault(AKV)에서 직접 생성, 소유, 관리하는 키로, 암호화 전략에 대한 더 강력한 제어 옵션을 제공합니다.

CMK를 사용하면 키의 수명 주기, 접근 권한, 사용 방식을 직접 관리할 수 있어 Microsoft 관리 암호화보다 한층 강화된 보안 계층을 제공하게 됩니다.

이 기능은 엄격한 규정 준수, 거버넌스, 고급 보안 요구 사항이 있는 조직에 특히 유용합니다.

또한 키를 필요할 때마다 교체하거나 접근 권한을 해제해 조직의 민감한 정보를 안전하게 보호할 수 있습니다.

## 새로운 기능
[고객 관리 키(CMK)는 미리보기 단계에서 처음 제공](https://blog.fabric.microsoft.com/blog/encrypt-data-at-rest-in-your-fabric-workspaces-using-customer-managed-keys/)되었으며, 이를 통해 작업 영역 관리자는 Azure Key Vault와 Managed HSM에 저장된 키를 사용해 특정 Fabric 항목의 데이터를 보호할 수 있었습니다.
이제 암호화 지원 범위를 더 많은 Fabric 워크로드로 확장할 수 있게 되었습니다.

이제 Fabric Warehouse와 Notebook을 생성하고, 작업 영역에서 SQL Analytics Endpoint를 활용할 수 있습니다. 이 모든 기능은 고객 관리 키를 적용해 암호화가 활성화된 상태에서 제공됩니다.

이 변경 사항은 순차적으로 배포 중이며, 앞으로 며칠 내에 모든 지역에서 사용할 수 있게 될 예정입니다.

<img src='https://dataplatformblogwebfd-d3h9cbawf0h8ecgf.b01.azurefd.net/wp-content/uploads/2025/10/image-25.png'>

추가 기능을 제공하기 위해 현재 개발을 진행 중입니다. 여기에는 API 지원, 방화벽 뒤에 있는 Key Vault 사용 기능, 그리고 더 많은 Fabric 항목에 대한 지원이 포함됩니다.

좀 더 자세한 내용은 [패브릭 작업 영역에 대한 고객 관리형 키](https://learn.microsoft.com/ko-kr/fabric/security/workspace-customer-managed-keys)와 [Warehouse’s CMK launch blog](https://blog.fabric.microsoft.com/ko-KR/blog/bringing-customer-managed-keys-to-fabric-warehouse-and-sql-analytics-endpoint/)를 참고하시기 바랍니다.

## Fabric 작업 영역에서 CMK 시작하기
작업 영역 관리자는 Fabric 포털에서 작업 영역 설정으로 이동해 고객 관리 키(CMK)를 사용한 암호화를 설정할 수 있습니다.
단계별 가이드는 [암호화 문서](https://learn.microsoft.com/fabric/security/workspace-customer-managed-keys)를 참고하시기 바랍니다.

## 여러분의 피드백이 중요합니다!
Fabric을 더 안전하고 유연하게 만들 수 있도록 의견을 공유해주세요.
피드백은 [Fabric Ideas – Microsoft Fabric Community](https://community.fabric.microsoft.com/t5/Fabric-Ideas/idb-p/fbc_ideas/label-name/fabric%20platform%20%7C%20security)에 남길 수 있습니다.

----------

- 2025년 10월 15일 업데이트 됨.
- 2025년 10월 16일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))