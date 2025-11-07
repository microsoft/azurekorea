---
layout: post
title:  "Azure 통합 HSM 도입: 가상 머신을 위한 키 캐시"
author: jyseong
tag: [ HSM, Virtual machine ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-03-Microsoft Azure Introduces Azure Integrated HSM A Key Cache for Virtual Machines/ifthisdoesntwork.png
---

### 작성자 : [simranparkhe](https://techcommunity.microsoft.com/users/simranparkhe/1890043)
### 원본 : [Microsoft Azure Introduces Azure Integrated HSM: A Key Cache for Virtual Machines](https://techcommunity.microsoft.com/blog/azurecompute/microsoft-azure-introduces-azure-integrated-hsm-a-key-cache-for-virtual-machines/4456283)

AMD v7 가상 머신에서 Azure 통합 HSM을 지원하는 미리보기(공개)를 공개합니다.
지난해 Ignite에서 소개했던 [Azure 통합 HSM](https://techcommunity.microsoft.com/blog/AzureInfrastructureBlog/securing-azure-infrastructure-with-silicon-innovation/4293834)은 하드웨어 보안 모듈(HSM) 기반 캐시와 암호화 처리 오프로드 기능을 제공하여, 가상 머신에서 암호화 작업의 보안성과 성능을 높이는 기술입니다.

암호화 기술을 많이 사용하고, 높은 성능을 요구하는 워크로드를 운영하는 고객에게 Azure 통합 HSM은 암호화 키를 안전하게 저장하고 빠르게 활용할 수 있는 하드웨어 기반의 보안 솔루션을 제공합니다.

이 기능은 현재 [AMD D 시리즈와 E 시리즈 v7 미리보기](https://techcommunity.microsoft.com/blog/azurecompute/announcing-preview-of-new-azure-dasv7-easv7-fasv7-series-vms-based-on-amd-epyc%e2%84%a2-/4448360?previewmessage=true)에서 사용할 수 있습니다.

또한 Azure는 [Azure Key Vault Managed HSM](https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/overview)도 제공합니다.
이 서비스는 완전 관리형, 고가용성, 단일 테넌트 클라우드 서비스로, FIPS 140-3 Level 3 인증을 받은 HSM을 사용해 암호화 키를 보호합니다.

이 모델은 강력한 키 보호를 제공하지만, 워크로드가 키를 사용해야 할 때는 다음의 두 가지 방식 중 하나를 선택해야 합니다.

- 네트워크 연결된 HSM 서비스에 호출함으로써 발생되는 네트워크 왕복에 따른 지연(network round-trip latency)을 감수하거나,
- 키 정책이 허용하는 경우 HSM에서 키를 해제하고 로컬 환경으로 가져오기

하지만 키가 HSM에서 해제되어 워크로드 환경으로 가져오면, 제공되는 보안 수준은 FIPS 140-3 Level 3보다 낮아질 수 있습니다. 서버 로컬 Azure 통합 HSM은 이러한 불편한 선택을 없앱니다.
Azure 통합 HSM은 키 작업을 위해 네트워크 왕복을 제거하고, 키를 워크로드 환경으로 해제할 필요가 없습니다.
원격 접근 대신, Azure 통합 HSM은 로컬 워크로드에 안전하게 연결되어 있으며, 승인된 서비스가 로컬 환경에서 오라클 방식으로 키를 사용할 수 있도록 지원합니다.

Azure 통합 HSM은 암호화 모듈에 대한 FIPS 140-3 Level 3 보안 요구사항을 충족하도록 설계되었습니다. Azure 통합 HSM은 키와 보안 자산이 사용 중일 때도 안전하게 보호할 수 있습니다.
또한, Azure 통합 HSM에는 전용 하드웨어 암호화 가속기가 내장되어 있어, 키가 HSM 내부에서 벗어나지 않은 상태로 암호화, 복호화, 서명, 검증 작업을 수행할 수 있습니다.

### 가용성

Azure 통합 HSM은 현재 AMD v7 미리보기 플랫폼에서 사용할 수 있습니다.
지원되는 VM 시리즈는 Dasv7, Dadsv7, Easv7, Eadsv7 시리즈이며, 8 vCore 이상의 가상 머신에서 동작합니다.
이 기능을 사용하려면 Trusted Launch 옵션을 활성화한 상태로 VM을 실행해야 합니다.
현재 미리보기는 Windows만 지원하며, Linux에 대한 지원은 곧 추가될 예정입니다.
이 기능은 추가 비용이 발생되지 않습니다.

[AMD v7 미리보기](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbRyMSy8VejZVEo6yZykiPSHpUQkI0VFlXTVVVUlhDMVg5SkRYSTFPNEJHQi4u&route=shorturl)에 가입해 주시면, 추가 정보를 안내해 드립니다.
또한, 예제와 Azure 통합 HSM 사용 방법에 대해서는 [GitHub 저장소](https://github.com/microsoft/AziHSM-Guest)를 참고하시기 바랍니다.

----------

- 2025년 9월 26일 업데이트 됨.
- 2025년 10월 3일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))