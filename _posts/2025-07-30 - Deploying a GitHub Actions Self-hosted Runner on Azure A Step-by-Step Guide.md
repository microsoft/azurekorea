---
layout: post
title:  "Azure에 GitHub Actions Self-hosted Runner 배포하기: 단계별 가이드"
author: jyseong
tag: [ Azure Virtual Machines , Github ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-30 - Deploying a GitHub Actions Self-hosted Runner on Azure A Step-by-Step Guide/github.jpg
---

### 작성자 : [NamanNihal](https://techcommunity.microsoft.com/users/namannihal/2904895)
### 원본 : [Deploying a GitHub Actions Self-hosted Runner on Azure: A Step-by-Step Guide](https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deploying-a-github-actions-self-hosted-runner-on-azure-a-step-by-step-guide/4413362)

### GitHub-hosted runners는 대부분의 워크플로에 적합하지만, 때로는 더 많은 제어가 필요할 때가 있습니다.  
### 커스텀 종속성, 영구적인 스토리지, 비용 최적화 등의 이유로 Azure에 셀프 호스팅 러너를 배포하는 것은 강력한 대안이 될 수 있습니다.

이 가이드에서는 Azure 가상 머신(VM)에 GitHub Actions Self-hosted runner를 단계별로 배포하는 과정에 대해서 살펴보겠습니다.

## 사전 준비 사항

시작하기 전에 다음 사항을 확인하세요:

- GitHub 저장소 또는 조직  
- Azure 포털 접근 권한  
- SSH 클라이언트 (예: Windows Terminal, macOS Terminal)  
- 기본적인 Linux(Ubuntu) 사용법 숙지


## 1단계: Azure VM 프로비저닝

1. Azure 포털에 접속합니다.  
2. 검색창에 **Virtual Machines**를 입력한 후, **+ Create**를 클릭합니다.  
3. **Basics** 탭에 다음 정보를 입력합니다:  
   - VM 이름: `gh-runner-vm`  
   - 지역(Region): `East US` (또는 원하는 지역)  
   - 이미지(Image): `Ubuntu 22.04 LTS`  
   - 크기(Size): `Standard B1s`  
   - 인증(Authentication): SSH 공개 키(SSH Public Key)  
   - 사용자 이름(Username): `azureuser`  
4. **Networking** 탭에서 SSH(포트 22) 허용 설정을 합니다.  
5. **Review + Create**를 클릭한 후 VM을 배포합니다.

## 2단계: VM에 연결하기

VM 배포가 완료되면:

1. Azure 포털에서 **Virtual Machines**로 이동 후, 생성한 VM을 선택합니다.  
2. 상단의 **Connect → SSH**를 클릭합니다.  
3. 아래의 SSH 명령어를 복사하여 터미널에 붙여넣고 실행하세요:
    ```bash
    ssh -i "/path/to/your/key.pem" admin_name@<YOUR_VM_PUBLIC_IP>
    ```

## 3단계: GitHub Runner 다운로드 및 구성

### 필요한 종속성 설치:
```bash
sudo apt update && sudo apt install -y curl tar jq
```

### GitHub Runner 다운로드:  
1. GitHub 저장소에서 **Settings → Actions → Runners → New self-hosted runner**로 이동합니다.  
2. 다음을 선택하세요:  
   - 운영체제(OS): Linux  
   - 아키텍처(Architecture): x64  
3. 제공되는 명령어를 실행합니다. 예:  
    ```bash
    mkdir actions-runner && cd actions-runner curl -o actions-runner-linux-x64-2.316.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz
    ```

### Runner 구성:
> 💡 **참고:**  
> 아래 명령어의 플레이스홀더(예: `your-repo`, `YOUR_TOKEN`)는 실제 값으로 반드시 교체해야 합니다.
```bash
./config.sh --url https://github.com/<your-username>/<your-repo> --token <generated-token>

Follow the prompts for runner name, work folder, and labels.
```

## 4단계: Runner를 서비스로 설치하고 시작하기
```bash
sudo ./svc.sh install sudo ./svc.sh start sudo ./svc.sh status
```
이렇게 하면 VM이 재부팅될 때 Runner가 자동으로 시작됩니다.

## 5단계: Runner 상태 확인하기
1. GitHub 저장소에서 **Settings → Actions → Runners**로 이동합니다.  
2. 등록한 Runner가 초록색 점과 함께 목록에 표시되는지 확인하세요.

## 6단계: GitHub Actions 워크플로 실행하기

`.github/workflows/test.yml` 워크플로 파일을 생성하세요:

```yml
name: Test Self-Hosted Runner

on: [push]

jobs:
  test:
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Run a script
        run: echo "Hello from GitHub self-hosted runner!"
```
이 파일을 repo에 푸시하면, 워크플로가 Azure VM에서 실행됩니다.

## 보너스: 자동 시작 및 정리

### 자동 시작(Auto-start)는 다음의 명령에 의해서 설정됩니다:
```bash
sudo ./svc.sh install
```

### runner 삭제
```bash
sudo ./svc.sh stop sudo ./svc.sh uninstall ./config.sh remove
```

### Docker 권한 문제 해결(필요한 경우):
```bash
sudo usermod -aG docker azureuser sudo systemctl restart docker
```

### runner 서비스 재시작
```bash
sudo systemctl restart actions.runner.azureuser.actions-runner.service
```

Azure에 self-hosted GitHub Actions runner를 설정하면, CI/CD 워크플로에 대한 더 큰 유연성, 성능, 그리고 제어권을 확보할 수 있습니다.  
자신만의 클라우드 환경에서 안심하고 빌드, 테스트, 배포를 수행할 수 있게 됩니다.

----------

- 2025년 5월 13일 업데이트 됨.
- 2025년 7월 30일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))