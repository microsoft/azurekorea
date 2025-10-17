---
layout: post
title:  "Azure Migrate에서 B-시리즈와 Cobalt 100 VM 지원으로 마이그레이션 비용 절감하기"
author: jyseong
tag: [ Azure Migrate, Azure Virtual Machine ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-10-10-Cut migration costs with B-Series and Cobalt 100 VM support in Azure Migrate/AZUREBLOG_MAR27_Azure-3D-Illustration-2-OffWhite_240327_V1.webp
---

### 작성자 : [ankitsurkar](https://techcommunity.microsoft.com/users/ankitsurkar/1930507)
### 원본 : [Cut migration costs with B-Series and Cobalt 100 VM support in Azure Migrate](https://techcommunity.microsoft.com/blog/azuremigrationblog/cut-migration-costs-with-b-series-and-cobalt-100-vm-support-in-azure-migrate/4460285)

# Azure Migrate에서 B-시리즈와 Cobalt 100 VM 지원으로 마이그레이션 비용 절감하기

## 스마트한 사이징으로 시작하는 스마트 마이그레이션 – Azure Migrate에서 B-시리즈와 Cobalt 100 VM 지원으로 비용 절감, 효율성 향상, 원활한 마이그레이션 실행

## 개요
클라우드로 마이그레이션한다고 해서 과도한 비용이 드는 것은 아닙니다. 많은 워크로드(예: 개발/테스트 환경, 소규모 데이터베이스, 트래픽이 적은 앱)가 지속적인 CPU 파워를 필요하지 않습니다. 그렇다면 거의 사용하지 않는 성능에 비용을 지불할 필요가 있을까요?

Azure Migrate는 B-시리즈와 Cobalt 100 VM에 대한 마이그레이션을 지원합니다. 이를 통해 더 스마트한 마이그레이션 계획을 세우고, 비용을 최적화하며, 각 워크로드에 꼭 맞는 성능을 확보할 수 있습니다.

## B-시리즈 VM: 버스트 가능한 성능, 더 낮은 비용
B-시리즈 VM은 CPU 사용량이 가변적인 워크로드를 위해 설계되어, 유연성을 유지하면서도 비용 효율성을 제공합니다.

**주요 장점:**

- **기본 성능:** 낮고 안정적인 CPU 기본 성능에 대해서만 비용을 지불합니다.
- **버스트 기능:** 유휴 시간 동안 적립된 크레딧을 사용해 일시적으로 성능을 확장(scale-up) 할 수 있습니다.
- **비용 효율성:** 대부분의 시간은 유휴 상태지만 가끔 높은 CPU가 필요한 워크로드(예: 개발/테스트 환경, 소규모 웹 서버, 배치 작업)에 이상적입니다.

**왜 중요한가?**

- CPU 사용량이 변동하는 워크로드에 적합합니다.
- 사용한 만큼만 비용을 지불해 큰 비용 절감을 가져올 수 있습니다.
- Azure Migrate 평가(assessment)에서 지원되어 정확한 비용 계획이 가능합니다.

일반용 D-시리즈 VM과 B-시리즈 VM을 비교하면 다음과 같습니다 (다른 조건은 동일)


| **VM 유형 / SKU**              | **vCPU / RAM**     | **시간당 요금 (USD)** | **월 예상 비용**\*                   | **비고**               |
| ---------------------------- | ------------------ | ---------------- | ------------------------------- | -------------------- |
| **Standard\_B8s v2** (B-시리즈) | 8 vCPU, 32 GiB RAM | —                | **약 $270.10** (Windows 라이선스 포함) | 버스트 가능한 VM, 낮은 기본 비용 |
| **D8s v4** (D-시리즈, 최신)       | 8 vCPU, 32 GiB RAM | **약 $0.384/시간**  | **약 $548.96** (Windows 라이선스 포함) | 범용 D 시리즈             |

> ✅ **참고:** 워크로드에서 성능 요구가 가끔씩 급증하는 경우, 최대 **50%까지 비용을 절감**할 수 있습니다.


## Cobalt 100 VM: ARM64 워크로드를 위한 네이티브 성능
Cobalt 100 VM은 에너지 효율적인 워크로드에 최적화된 최신의 ARM 네이티브 가상 머신입니다. ARM64 기반 서버를 온프레미스에서 클라우드로 이전할 때 가장 이상적입니다.

**주요 장점:**

- **아키텍처 호환성:** ARM64 워크로드를 재설계 없이 원활하게 마이그레이션.
- **성능 향상:** ARM 네이티브 최적화를 통해 더 높은 효율성 제공.
- **비용 절감:** ARM64 효율성과 Azure의 유연한 가격 정책을 결합해 코어당 더 높은 가치를 실현.


**중요한 이유:**

- ARM64 기반 서버와 애플리케이션에 이상적.
- 전력 대비 성능 효율을 극대화.
- Azure Migrate에서 ARM64 지원 평가를 통해 계획을 간소화.

## 시작할 준비가 되셨나요?
높은 비용 때문에 마이그레이션을 주저하지 마세요.
지금 바로 Azure Migrate에서 B-시리즈와 Cobalt 100 VM 지원을 활용해 보시기 바랍니다.

👉 자세히 알아보고 시작하기: [Assessment Properties – Azure Migrate | Microsoft Learn](https://learn.microsoft.com/en-us/azure/migrate/vm-assessment-properties?view=migrate)

----------

- 2025년 10월 9일 업데이트 됨.
- 2025년 10월 10일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))