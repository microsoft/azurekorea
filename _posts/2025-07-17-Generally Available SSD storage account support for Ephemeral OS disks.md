---
layout: post
title:  "Generally Available: SSD 저장소 계정의 Ephemeral OS 디스크 지원"
author: jyseong
tag: [ Azure Disk ]
category: [ Solution ]
---

### 작성자 : [viveksingla](https://techcommunity.microsoft.com/users/viveksingla/1991463)
### 원본 : [Generally Available: SSD storage account support for Ephemeral OS disks](https://techcommunity.microsoft.com/blog/azurecompute/generally-available-ssd-storage-account-support-for-ephemeral-os-disks/4429107)


VM 또는 VMSS 생성 시 Ephemeral OS 디스크에 대해 SSD 저장소 계정 지원이 가능하게(General Availability, GA) 되었습니다. 이번 GA는 공개 미리 보기(Public Preview)를 기반으로 하였으며, stateless 워크로드에 대해 향상된 성능과 안정성을 제공합니다. 이 기능은 특히 VM 부팅 시간과 안정성이 중요한 stateless 애플리케이션에 유용합니다. SSD 기반 디스크의 향상된 읽기 성능은 부팅 및 애플리케이션 초기화 시간을 단축시켜 줍니다. 구체적인 활용 사례는 다음과 같습니다:

- **컨테이너 기반 워크로드:** 더 빠른 확장 작업과 높은 VM 안정성 달성
- **VDI(가상 데스크톱 인프라):** 풀 환경에서 사용자에게 신속하게 새로운 데스크톱 배포
- **CI/CD 빌드 에이전트:** 깨끗하고 일관된 환경에서 작업을 더 빠르게 시작


## 새로운 기능
이번 GA 릴리스를 통해 고객은 Ephemeral OS 디스크의 기본 디스크 유형으로 Standard SSD(StandardSSD_LRS) 또는 Premium SSD(Premium_LRS)를 선택할 수 있게 되었습니다. 이전에는 Standard HDD만 지원되었습니다.

이를 통하여 다음과 같은 장점을 얻을 수 있습니다:

1. **더 높은 SLA:** Premium SSD를 사용하는 VM은 99.9%의 SLA를 제공받으며, 이는 Standard HDD의 95%보다 높습니다.

2. **향상된 읽기 성능:** 기본 디스크로 Premium SSD를 선택하면 OS 디스크의 읽기 성능을 향상시킬 수 있습니다. 대부분의 쓰기 작업은 로컬 임시 디스크에서 수행되지만, 일부 읽기 작업은 관리 디스크에서 수행됩니다. Premium SSD 디스크는 Standard HDD보다 8~10배 더 높은 IOPS를 제공합니다.

## 동작 방식
Ephemeral OS 디스크는 두 개의 디스크로 구분됩니다 — 로컬 임시 디스크에 위치한 diff 디스크와 관리 디스크를 사용하는 base 디스크입니다. 기존 파일 및 새 파일에 대한 모든 쓰기 작업은 diff 디스크에서 수행되며, 원본 파일은 base 디스크에서 읽어옵니다. VM이 정상적으로 작동하려면 diff 디스크와 base 디스크 모두가 필요합니다.

**SSD 지원은 Ephemeral OS 디스크에 사용되는 base 디스크의 유형을 고객이 선택할 수 있도록 하는 새로운 옵션**입니다. 이전에는 base 디스크로 Standard HDD만 사용할 수 있었지만, 이제 고객은 다음 세 가지 디스크 유형 중에서 선택할 수 있습니다:

- Standard HDD(Standard_LRS)
- Standard SSD(StandardSSD_LRS)
- Premium SSD(Premium_LRS)

base 디스크로 SSD를 사용하면, 고객은 Standard HDD에 비해 더 높은 SLA와 더 나은 성능을 얻을 수 있습니다.
Standard HDD를 base 디스크로 사용하는 경우에는 Ephemeral OS 디스크와 함께 무료로 사용할 수 있으며, SSD를 base 디스크로 프로비저닝할 경우에는 추가 디스크 비용이 발생합니다.

## 사용 방법
Azure CLI, PowerShell 또는 ARM 템플릿을 사용하여 VM 생성 시 Ephemeral OS 디스크의 기본 디스크 유형(base disk type)을 지정할 수 있습니다.

예를 들어, 다음 명령어를 이용하면, Ephemeral OS 디스크와 Premium SSD를 base 디스크로 사용하는 VM을 생성할 수 있습니다:

### AzCLI
```shell
az vm create --name MyVM --resource-group MyRG --image UbuntuLTS --ephemeral-os-disk true --storage-sku Premium_LRS
```

### PowerShell
```PowerShell
Set-AzVMOSDisk -VM $VirtualMachine -DiffDiskSetting Local -DiffDiskPlacement ResourceDisk -CreateOption FromImage  -Caching ReadOnly -StorageAccountType "Premium_LRS"
```

## 지금 바로 시작하세요
이제 Azure 포털, CLI, PowerShell, ARM 템플릿을 통해 Azure Storage를 사용한 Ephemeral OS 디스크 기반 VM 배포가 가능해졌습니다. 
VM을 생성할 때, Ephemeral OS 디스크 사용 옵션을 선택하고 OS 디스크 유형에서 Premium SSD를 선택하세요.

보다 자세한 정보와 배포 단계는 [Ephemeral OS 디스크](https://learn.microsoft.com/en-us/azure/virtual-machines/ephemeral-os-disks#ssd-storage-account-support-for-ephemeral-os-disks)에 대한 공식 문서를 참고해 주세요.

----------

- 2025년 7월 13일 업데이트 됨.
- 2025년 7월 17일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))