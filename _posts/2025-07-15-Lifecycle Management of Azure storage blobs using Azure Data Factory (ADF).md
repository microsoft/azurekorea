---
layout: post
title:  "Azure Data Factory(ADF)를 활용한 Azure 저장소 Blob의 수명 주기 관리"
author: jyseong
tag: [ Azure Data Factory, Azure storage blobs, Lifecycle Management ]
category: [ Solution ]
---

### 작성자 : [Deeksha_S_A](https://techcommunity.microsoft.com/users/deeksha_s_a/986540)
### 원본 : [Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)](https://techcommunity.microsoft.com/blog/azurepaasblog/lifecycle-management-of-azure-storage-blobs-using-azure-data-factory-adf/4397808)


**배경:**
저장소 계정에서 일정 기간이 지난 후 page Blob을 자동으로 삭제해야 하는 요청이 많이 발생되곤 합니다. 현재 수명 주기 관리 기능은 page Blob 삭제를 지원하지 않습니다.

참고: ADF를 사용하면 모든 Blob(Page/Block/Append Blob)을 삭제할 수 있습니다.

저장소 계정에서 page Blob(또는 다른 Blob 유형)을 삭제하는 작업은 다음과 같은 도구를 통해 수행할 수 있습니다:

- Azure Storage Explorer
- REST API
- SDK
- PowerShell
- Azure Data Factory
- Azure Logic App
- Azure Function App
- Azure Storage Actions(미리 보기)

이번 블로그에서는 ADF를 사용하여 Blob을 삭제하는 방법에 대해서 살펴봅니다.

**단계 1:**
Azure 포털에서 Azure Data Factory 리소스를 생성합니다. ADF가 처음이라면, 다음 링크를 참고하여 생성 방법을 확인하세요:
https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal

**단계 2:**
개요 블레이드에서 'Azure Data Factory Studio 열기'를 선택합니다.

![Open Azure Data Factory Studio](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-1-1742278382168.png)

**단계 3:**
Data Factory 포털에서 펜 아이콘을 클릭한 후 → + → 파이프라인 생성(Create pipeline)을 선택합니다.

![Create pipeline](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-2-1742278417160.png)

**단계 4**:
생성된 파이프라인을 클릭한 후 → 활동(Activities) 아래에서 → 일반(General) → 'Delete'를 선택하고 파이프라인 영역으로 드래그합니다.

![Create Activities](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-3-1742278434910.png)

**단계 5:**
소스(Source) 아래에서 새로 만들기(New)를 선택하고, 데이터 소스(Datasource)로 Azure Blob Storage를 선택합니다.

![Create Linked Service](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-4-1742278434913.png)

**단계 6:**
새 연결 서비스(New linked service)에서는 기본으로 제공되는 이름을 사용하거나 필요에 따라 사용자 지정할 수 있습니다.
계정 선택 방법이 Azure 구독인 경우 저장소 계정을 선택할 수 있으며, 그렇지 않은 경우 수동으로 입력할 수도 있습니다.
그런 다음 '생성(Create)'을 클릭합니다.

![Create Linked Service](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-5-1742278434913.png)

**단계 7:**
파일 경로(File path)에 컨테이너 이름과 폴더/디렉터리 이름을 입력합니다 (필요에 따라 입력).

![Create Linked Service](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-6-1742278434913.png)

**단계 8:**
파이프라인으로 돌아와서, 이미지에 표시된 대로 다음 속성들을 구성합니다.

![pipeline configurations](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-7-1742278434914.png)

**참고: 마지막 수정일 기준으로 Blob만 삭제하고 싶다면 "마지막 수정일로 필터링(Filter by last Modified)" 옵션을 사용할 수 있습니다.**

**단계 9:**
디버그(Debug)를 클릭하여 파이프라인을 실행합니다.

![pipeline configurations](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-8-1742278434914.png)

파이프라인 동작은 출력 탭(Output tab)에서 확인할 수 있습니다.

![pipeline configurations](../assets/images/jyseong/images/2025-07-15 - Lifecycle Management of Azure storage blobs using Azure Data Factory (ADF)/clipboard_image-9-1742278434914.png)



**참고:** 

[Use Add Trigger to manually start the pipeline. ](https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal#trigger-the-pipeline-manually)

[Use Add Trigger to schedule the pipeline. ](https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal#trigger-the-pipeline-on-a-schedule)


**참고 문서** 

https://techcommunity.microsoft.com/blog/azurepaasblog/efficient-management-of-append-and-page-blobs-using-azure-storage-actions/4281019 

https://techcommunity.microsoft.com/blog/azurepaasblog/lifecycle-management-for-page-blob-and-block-blob-using-function-app-/2801787 

https://techcommunity.microsoft.com/blog/azurepaasblog/delete-all-the-azure-storage-blob-content-before-n-days-using-logic-app/838870 


----------

- 2025년 3월 27일 업데이트 됨.
- 2025년 7월 4일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))