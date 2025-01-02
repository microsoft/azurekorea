---
layout: post
title:  "Dev 컨테이너에서 Azurite 실행하기"
author: jyseong
tag: [ Azurite, Dev Container ]
category: [ Solution ]
image: assets/images/jyseong/images/azurite.png
---

### 작성자 : [Pamela_Fox](https://techcommunity.microsoft.com/users/pamela_fox/1604078)
### 원본 : [Running Azurite in a Dev Container:](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/running-azurite-in-a-dev-container/4342188)

## 로컬 Blob 스토리지 에뮬레이터로 환경 구축하기
저는 Python cloud advocacy 팀의 파멜라라고 합니다. 저는 Python 커뮤니티에서 인기있는 오픈-소스 프로젝트(예를 들면, 인기있는 웹 프레임워크인 Flask의 확장)에 기여하는 역할을 담당하고 있습니다. 이번 주에는 Azure Blob Storage SDK를 레거시 버전(v2)에서 최신 버전(v12)으로 [업그레이드](https://github.com/pallets-eco/flask-admin/pull/2573)하기 위한 [Flask-admin 확장 기능](https://github.com/pallets-eco/flask-admin)에 대한 PR 작업을 하였으며, [마이그레이션 가이드](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/migration_guide.md)도 제공됩니다.

운영계의 Blob storage account를 건드리지 않고도 변경 내용에 대한 용이한 테스트를 위해서, 공식 로컬 에뮬레이터인 [Azurite server](https://learn.microsoft.com/azure/storage/common/storage-use-azurite?tabs=docker-hub%2Cblob-storage)를 사용하였습니다. Mac에 에뮬레이터를 설치할 수 있지만, 이미 GitHib Codespace에서 작업을 하고 있기 때문에 Azurite가 개발 환경에 자동으로 설치되도록 하고 싶었습니다. flask-admin 레포지토리에 대한 [dev container 정의](https://containers.dev/)를 생성하고, 이를 이용하여 Azurite를 가져오도록 하였습니다.

Azurite가 포함된 dev container를 모두가 이용할 수 있도록, Azurite 구성 목적의 GitHub 레포지토리를 생성하였습니다.
[https://github.com/pamelafox/azurite-python-playground](https://github.com/pamelafox/azurite-python-playground)
GitHub Codespace나나 VS Code Dev Container에서 바로 사용도 가능하고, 열어서 동작 방식을 알아볼 수도 있습니다.

## devcontainer.json
dev container의 진입점(entry point)는 **.devcontainer/devcontainer.json**로, IDE로 하여금 컨테이너화된 환경 설정 방법을 알려주는 역할을 수행합니다. 
Azurite가 포함된 컨테이너는 **devcontainer.json**로 구현됩니다.

```json
{
  "name": "azurite-python-playground",
  "dockerComposeFile": "docker-compose.yaml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [10000, 10001],
  "portsAttributes": {
    "10000": {"label": "Azurite Blob Storage Emulator", "onAutoForward": "silent"},
    "10001": {"label": "Azurite Blob Storage Emulator HTTPS", "onAutoForward": "silent"}
  },
  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  },
  "remoteUser": "vscode"
}
```

해당 dev container는 IDE로 하여금 **docker-compose.yaml**를 이용하여 컨테이너를 빌드하고, 편집기가 열 수 있는 기본 컨테이너로 "app" 서비스를 사용하도록 지시합니다. 또한, IDE는 Azurite애 의해서 오픈된 두 개의 포트들을 전달(HTTP는 10000, HTTPS는 10001)하고, 이를 "Ports" 탭에 label을 지정합니다. 반드시 필요한 것은 아니지만, 서버가 실행 중임을 확인할 수 있는 좋은 방법이기도 합니다.

## docker-compose.yaml
**docker-compose.yaml** 파일은 먼저 IDE의 편집 환경에 사용될 "app" 컨테이너를 기술한 다음, 로컬 Azurite 서버에 대한 "azurite" 컨테이너를 정의하고 있습니다.

```yaml
version: '3'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    volumes:
      - ..:/workspace:cached

    # Overrides default command so things don't shut down after the process ends.
    command: sleep infinity
    environment:
      AZURE_STORAGE_CONNECTION_STRING: DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;

  azurite:
    container_name: azurite
    image: mcr.microsoft.com/azure-storage/azurite:latest
    restart: unless-stopped
    volumes:
      - azurite-data:/data
    network_mode: service:app

volumes:
  azurite-data:
```

몇 가지 주의할 사항은 다음과 같습니다:

- "app" 서비스는 기본 Python 이미지를 사용하는 로컬 **Dockerfile**에 기반을 두며, **AZURE_STORAGE_CONNECTION_STRING**을 설정하여 로컬 서버에 연결하는데 사용합니다.
- "azurite" 서비스는 **공식 azurite 이미지**를 기반하고 있으며, 데이터 저장을 위해서 볼륨을 사용합니다.
- "azurite" 서비스는 **network_mode: service:app**을 이용하여 "app" 서비스가 동일 네트워크에서 동작하도록 합니다. 이는 앱을 **loclahost** URL로 접근할 수 있음을 의미합니다. 다른 방법으로는 기본값인  **network_mode: bridge**을 이용하여, "http://azurite:10000"와 같이 서비스 이름으로 Azurite 서비스로 접근하도록 할 수 있습니다. 연결 문자열이 제대로 설정되어 있다면, 두 가지 방식 모두 잘 동작합니다.

## Dockerfile
**Dockerfile**에는 코드 편집 환경을 정의합니다. 이 경우, devcontainer 최적화된 Python 이미지를 가져옵니다. Java, .NET, JavaScript, Go 등과 같은 언어별로 조정이 가능합니다.

```
FROM mcr.microsoft.com/devcontainers/python:3.12

pip install -r requirements.txt
```

- 2024년 12월 3일 업데이트 됨.
- 2024년 12월 13일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))