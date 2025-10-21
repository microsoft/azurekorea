---
layout: post
title:  "Azure VM 맞춤 설정 미리보기 공개: 멀티스레딩 끄기 & 코어 개수 제한 기능 제공"
author: jyseong
tag: [ virtual machine ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-18-Announcing Public Preview of VM Customization in Azure Disable Multithreading & Constrained Cores/header.jpg
---

### 작성자 : [eehindero](https://techcommunity.microsoft.com/users/eehindero/3018825)
### 원본 : [Announcing Public Preview of VM Customization in Azure: Disable Multithreading & Constrained Cores](https://techcommunity.microsoft.com/blog/azurecompute/announcing-public-preview-of-vm-customization-in-azure-disable-multithreading--c/4462417)

Azure의 VM 맞춤 설정 기능에 대한 미리보기가 발표되었습니다.
이번 미리보기에서는 다음의 두 가지 강력한 기능이 포함되었습니다:

- **동시 멀티스레딩(SMT/HT) 비활성화**
- **코어 개수 제한(Constrained Cores)**

이 기능을 통해 고객은 가상 CPU 구성을 원하는 대로 조정할 수 있어, 성능 최적화는 물론 다양한 워크로드에서 소프트웨어 라이선스 비용 절감까지 가능합니다.

VM 맞춤 설정은 컴퓨팅 리소스 할당 방식에서 유연성을 요구하는 고객의 변화하는 요구를 충족하도록 설계되었습니다.
비용, 성능, 규정 준수 중 어떤 것을 최적화하든, 이 기능을 사용하면 메모리, 스토리지, I/O는 그대로 유지하면서 라이선스 용량, 워크로드 특성, 인프라 전략에 맞게 VM 구성을 조정할 수 있습니다.
Azure는 이번 발표로 맞춤형 인프라 전략을 더욱 강화했습니다.

VM 크기에서 코어 수를 분리함으로써, 고객은 메모리나 네트워크 대역폭이 큰 VM을 더 적은 코어로 실행할 수 있어, 소프트웨어 라이선스 비용을 줄이고 효율성을 높일 수 있습니다.
또한, 지연 시간에 민감한 워크로드에서 하이퍼스레딩을 비활성화할 수 있어, 데이터베이스 최적화, HPC(고성능 컴퓨팅), 분석 등 새로운 시나리오를 지원합니다.

## 새로운 기능
VM 맞춤 설정을 통해 고객은 이제 다음과 같은 기능을 사용할 수 있습니다:

- **동시 멀티스레딩 비활성화 (SMT/HT Off):**

    지원되는 VM을 코어당 하나의 스레드로 실행하도록 설정할 수 있습니다.
이를 통해 워크로드는 물리적 코어를 독점적으로 사용하여 성능을 향상시키고 지연 시간을 안정적으로 유지할 수 있습니다.

- **사용자 지정 vCPU 개수 선택:**

    VM 크기에 맞는 유효한 vCPU 개수 목록에서 선택하여 라이선스 요구사항이나 워크로드에서 필요한 기준에 맞출 수 있습니다.
    이 과정에서 메모리, 스토리지, I/O 기능은 변경되지 않습니다.

## 중요한 점

VM 맞춤 설정은 가상 머신을 구성하는 방식에서 좀 더 큰 유연성을 제공하여 고객이 겪는 지속적인 문제를 해결하도록 설계되었습니다.
고성능 컴퓨팅(HPC)이나 금융 모델링처럼 성능에 민감한 워크로드의 경우, 하이퍼스레딩을 비활성화하면 코어를 완전히 분리할 수 있어 성능을 크게 향상시킬 수 있습니다.

SQL Server, Oracle, SAP 같은 데이터베이스 워크로드에서는, VM 맞춤 설정을 통해 고객이 필요한 코어 수만 선택하면서도 대형 VM의 메모리와 대역폭 혜택을 그대로 누릴 수 있습니다.
이러한 방식은 소프트웨어 라이선스 비용을 크게 줄이는 효과를 가져올 수 있습니다.

또한, VM 맞춤 설정은 규정 준수와 비용 최적화를 단순화합니다. 특히 BYOL(Bring Your Own License) 모델이나 코어 단위 소프트웨어 계약을 사용하는 조직에 유용합니다.
VM 리소스를 정확한 요구사항에 맞게 조정함으로써, 고객은 기술적 요구와 비즈니스 요구를 모두 충족하는 인프라를 더 잘 구축할 수 있습니다.

## 미리보기 참여
VM 맞춤 설정은 이제 미리보기(공개) 형식으로 미국 중서부, 북유럽, 동아시아, 영국 남부등의 지역에서 제공됩니다.

VM 맞춤 설정은 Azure 포털, ARM 템플릿, Azure CLI, PowerShell을 통해 사용할 수 있습니다.

1st party OS 이미지만 지원되며, 3rd party 라이선스가 포함된 Marketplace 이미지는 지원되지 않습니다.

미리보기를 사용하려면 [여기](https://forms.office.com/r/JjMivfn8bS)의 설문 양식을 작성해 주세요.
여러분의 의견을 기다리고 있겠습니다.

----------

- 2025년 10월 18일 업데이트 됨.
- 2025년 10월 18일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))