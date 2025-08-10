---
layout: post
title:  "프라이빗 링크를 활용한 Databricks와 Storage Account 간의 크로스 테넌트 연결"
author: jyseong
tag: [ Azure Networking , Azure Private Link ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-02-Network Redundancy from On-Premises to Azure VMware and VNETs/image.png
---

### 작성자 : [umairakhtar19](https://techcommunity.microsoft.com/users/umairakhtar19/2807670)
### 원본 : [Cross-Tenant Connectivity between Databricks and Storage account using Private Link](https://techcommunity.microsoft.com/blog/azurenetworkingblog/cross-tenant-connectivity-between-databricks-and-storage-account-using-private-l/4406700)

### Azure Private Link는 프라이빗 엔드포인트를 활용하여 서로 다른 테넌트 간에도 Azure PaaS 서비스에 대한 사적이고 안전한 연결을 제공합니다. 이 아키텍처는 모든 트래픽이 Microsoft 백본 네트워크를 통해 전달되도록 하여 공용 인터넷을 완전히 우회합니다.  
## 이 블로그에서는 Azure Private Link를 사용하여 Azure Databricks와 Azure Storage 계정 간의 크로스 테넌트 연결을 설정하는 과정을 안내합니다.


## High Level Architecture
![High level architecture](../assets/images/jyseong/images/2025-07-02 - Network Redundancy from On-Premises to Azure VMware and VNETs/image.png)

## 크로스 테넌트 아키텍처 개요

- 이 구성은 두 개의 별도 Azure 테넌트를 포함합니다:
  - **테넌트 A:** Storage Account를 호스팅
  - **테넌트 B:** Azure Databricks를 호스팅

- 테넌트 B의 Databricks가 Private Endpoint를 사용하여 테넌트 A의 Hierarchical Namespace (HNS)가 활성화된 Storage Account에 접근합니다.
- 테넌트 A의 Storage Account는 HNS가 활성화되어 있으며 (즉, Azure Data Lake Storage Gen2에 적합함).
- 스토리지 계정을 위해 생성된 Private Endpoint의 NIC를 해석할 수 있도록 Private DNS Zone을 구성해야 합니다.
- 다중 테넌트 서비스 주체(Service Principal, SPN)가 필요합니다:
  - 테넌트 B의 Databricks가 테넌트 A의 Storage Account에 안전하고 관리되는 방식으로 접근할 수 있도록 허용
  - Storage Account에 대한 역할 기반 액세스 제어(RBAC) 권한 부여


# 크로스 테넌트 Private Endpoint 구성 단계

1. **테넌트 A에서 HNS가 활성화된 Storage Account 생성**
    - **리소스 ID와 하위 리소스 이름(blob)을 기록**
2. **테넌트 B에서 Private Endpoint 생성**
   - 테넌트 A의 Storage Account에서 기록한 리소스 ID와 하위 리소스 이름(blob)을 사용
3. **Private Endpoint 생성 후:**
   - 테넌트 A로 승인 요청이 전송됨
   - 승인은 다음 경로에서 확인 가능:
     - `Storage Account > Networking > Private endpoint connections`
4. **테넌트 A에서 Private Endpoint 요청 승인**
   - 최소 필요한 역할:
     - Private Link Service Owner
     - 또는 Network Contributor
5. **DNS 구성 업데이트**
   - Private DNS Zone이 Private Endpoint의 NIC를 정확히 해석할 수 있도록 설정하여, 테넌트 B에서 Storage Account의 이름 해석이 정상적으로 이루어지도록 함

## 다중 테넌트 SPN 구성 및 액세스

1. **테넌트 B에서 다중 테넌트 앱 등록(SPN) 생성**
2. **테넌트 A에서 관리자 동의(admin consent) 부여**
   - 다음 URL을 사용:
     - `https://login.microsoftonline.com/{organization}/adminconsent?client_id={client-id}`
   - 대체할 값:
     - `{organization}` = 테넌트 A의 디렉터리 (Tenant) ID
     - `{client-id}` = SPN의 애플리케이션 (Client) ID
3. **관리자 동의 승인을 위한 최소 Entra ID 역할:**
   - Application Administrator
4. **동의가 부여된 후, 테넌트 A에서 SPN에 RBAC 할당**
   - 역할: Storage Blob Data Contributor
   - 범위: 대상 Storage Account

## Azure 문서 참고 자료

- **다중 테넌트 SPN:** [How to convert an app to be multi-tenant](https://learn.microsoft.com/en-us/entra/identity-platform/howto-convert-app-to-be-multi-tenant)

- **테넌트 전체 관리자 동의:** 
  [Grant tenant-wide admin consent to an application - Microsoft Entra ID | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/howto-admin-consent)


----------

- 2025년 5월 19일 업데이트 됨.
- 2025년 7월 2일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))