---
layout: post
title:  "Spark가 OneLake 보안을 지원하는 방법: 행 및 열 수준 정책 적용"
author: jyseong
tag: [ Apache Spark , Data Engineering ]
category: [ Solution ]
---

### 작성자 : [Ted Vilutis](https://blog.fabric.microsoft.com/en-us/blog/author/Ted%20Vilutis)
### 원본 : [How Spark Supports OneLake Security with Row and Column Level Policies](https://blog.fabric.microsoft.com/en-US/blog/how-spark-supports-onelake-security-with-row-and-column-level-security-policies/)

최근 OneLake에서 **행 수준/열 수준 보안(Row/Column Level Security)** 을 공식 지원을 발표하였습니다.
이 범용 보안 프레임워크는 데이터에 접근하는 방식과는 상관없이, 모든 데이터 엔진에 동일하게 적용됩니다. 전통적으로 Spark에서는 정밀한 보안 기능을 제공하지 않으며, 쿼리 실행에 필요한 데이터셋에는 무제한으로 접근이 가능하다고 생각하고 사용해왔습니다.

이 한계를 해결하기 위해, Spark 엔지니어링 팀은 성능 저하 없이 Spark에서 안전한 데이터 접근을 가능하게 하는 맞춤형 솔루션을 개발했습니다. 엔진 레벨에서, 작업이 행/열 수준 보안 정책으로 보호된 테이블을 읽어야 하는 경우, 처리 과정은 서로 격리된 두 환경으로 분리됩니다.

- 하나는 사용자 코드를 실행하는 환경이고,
- 다른 하나는 사용자 코드가 소비할 데이터를 안전하게 접근·준비하는 환경입니다.

데이터 준비 단계에서 행/열 수준 보안 정책이 적용되어, 권한이 부여된 데이터만 사용자 코드에 노출되도록 보장합니다.

<img src='https://dataplatformblogwebfd-d3h9cbawf0h8ecgf.b01.azurefd.net/wp-content/uploads/2025/10/image-33.png'>

이와 같이 두 환경으로 분리하는 과정은 사용자가 추가 설정이나 작업은 필요 없으며, 자동으로 처리됩니다.
Spark 엔진은 작업영역(workspace)에서 실행되는 모든 작업마다 보안 환경을 자동으로 생성하며, 쿼리 부하에 따라 리소스를 동적으로 확장합니다.
쿼리가 실행 중이지 않으면, 성능 최적화와 시작 지연 최소화를 위해 보안 환경은 종료되기 전 최대 5분간 유지됩니다.
사용자는 모니터링 기능에서 보안 환경 작업을 확인할 수 있으며, 해당 작업은 'SparkSecurityControl' 접두사로 표시됩니다.

<img src='https://dataplatformblogwebfd-d3h9cbawf0h8ecgf.b01.azurefd.net/wp-content/uploads/2025/10/image-32.png'>

OneLake는 범용 보안 정책을 엄격하게 적용하여 무단 접근을 완전하게 차단합니다.
행/열 수준 보안(Row/Column Level Security) 정책이 설정된 테이블에 대한 파일 단위 직접 접근은 완전히 금지됩니다.
마찬가지로, Spark 코드가 테이블에 접근할 때 파일 경로를 직접 지정하는 방식은 허용되지 않으며, 반드시 Spark SQL의 네임스페이스 참조(예: lakehouse.schema.table)를 통해 접근해야 합니다.

Spark는 스키마가 활성화된 Lakehouse와 비활성화된 Lakehouse 모두에서 행/열 수준 보안 정책을 지원합니다.
단, Spark가 보안 클러스터를 사용하려면, 쿼리하는 대상 Lakehouse가 스키마를 지원하는지 여부와는 관계없이 **사용자가 기본 Lakehouse로 스키마가 활성화된 Lakehouse를 고정(pinned)** 해야 합니다.

<img src='https://dataplatformblogwebfd-d3h9cbawf0h8ecgf.b01.azurefd.net/wp-content/uploads/2025/10/image-57.png'>

OneLake 보안 기능의 미리보기는 누구나 사용할 수 있게 되었습니다.
지금 바로 작업영역에서 해당 기능을 확인하고, 업데이트된 문서를 검토하거나, [무료 Microsoft Fabric 체험판에 가입](https://app.fabric.microsoft.com/)해 OneLake 보안을 직접 경험해 보시기 바랍니다.

----------

- 2025년 10월 21일 업데이트 됨.
- 2025년 10월 22일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))