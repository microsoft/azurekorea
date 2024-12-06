---
layout: post
title:  "Azure Load Testing: 곧 출시될 기능 미리 엿보기"
author: jyseong
tag: [Azure Network, Azure Load Testing]
category: [ Update ]
image: assets/images/thumnails/jyseong-lbtesting.png

---
### 원본 : [Azure Load Testing: A sneak peek into what’s coming soon](https://techcommunity.microsoft.com/blog/appsonazureblog/azure-load-testing-a-sneak-peek-into-what%E2%80%99s-coming-soon/4304743)
작성자 : Nikita_Nallamothu

성능 테스트를 한 단계 높이고자 하십니까? 완전히 관리되는 서비스인 [Azure Load Testing](https://aka.ms/malt)을 이용하면, 별다른 노력 없이도 대규모 부하를 만들어서 성능 병목 현상을 찾아낼 수 있도록 해줍니다. 지난 몇 달에 걸쳐서, 고객의 피드백을 경청하고 서비스를 지속적으로 개선해 왔습니다. 지리적으로 여러 위치에 걸쳐서 부하를 분산시키는 것부터 디버깅 개선, 로깅 향상에 이르기까지, 최신 업데이트는 테스트 작업을 보다 원활하고 효율적으로 만들도록 설계하였습니다.

이 뿐만 아니라, 다음과 같은 흥미로운 기능들이 새롭게 출시될 예정입니다. 곧 출시될 기능들과 개선 사항들이 성능 테스트의 요구 사항을 충족하는데 어떻게 도움을 줄 수 있는지 상세하게 살펴보도록 하겠습니다.

### 여러 개의 JMeter 파일 지원

이 기능은 여러 개의 JMeter 파일을 업로드할 수 있도록 하여, **JMeter 스크립트를 모듈화**할 수 있습니다. 이러한 모듈식 접근 방법은 아래와 같이 여러 가지 측면에서 도움이 됩니다.

- **관리의 용이성**: 테스트 계획을 더 작고 관리하기 쉬운 구성 요소로 쪼개면, 복잡한 테스트 시나리오를 좀 더 효율적으로 관리할 수 있습니다.
- **재사용성**: 서로 다른 테스트 계획에 걸쳐서 테스트 구성요소를 재사용할 수 있게 됩니다. 이를 통해서 테스트 생성 및 관리에 필요한 시간과 노력을 절약할 수 있습니다.
- **유연성**: 모듈화를 통해서 전체 스크립트에 영향을 주지 않고 테스트 계획의 일부를 업데이트하거나 수정할 수 있습니다. 이를 통해서 변경 적용이 쉬워집니다.

### 일정 및 알림

해당 기능을 이용하면, 다음과 같은 장점을 누릴 수 있습니다,

- **부하 테스트 예약**: 부하 테스트를 나중에 실행하거나 반복되는 간격으로 실행하도록 예약이 가능합니다. 특히 정기적인 성능 확인이나 회귀 테스트에 유용하게 사용할 수 있습니다.
- **알림**: 테스트 완료와 실패와 같이, 부하 테스트와 관련된 중요한 이벤트에 대한 알림을 받을 수 있습니다. 이를 통하여, 테스트 상태와 결과에 대한 정보 받기가 가능합니다.

![img](../assets/images/jyseong/lb-test1.png)
### 결론

앞선 기능들은 여러 분의 시간과 노력을 절약할 수 있도록 설계되었습니다. 이를 통하여, 여러 분에게 가장 중요한 가치인 ‘고품질의 어플리케이션 생산’에 집중할 수 있습니다. 새로운 업데이트들을 기대해주시고, Azure Load Testing으로 여러 분의 성능 테스트를 한 단계 높일 수 있기 바랍니다. 자세한 내용은 [여기](https://aka.ms/malt-docs)를 참고하시기 바랍니다. 여러 분의 피드백도 기다리겠습니다. 피드백은 [여기](https://aka.ms/malt-feedback)에 공유 해주세요.

즐거운 부하 테스트가 되길 바랍니다!

- 2024년 11월 22일 업데이트 됨.
- 2024년 11월 27일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))