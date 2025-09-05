---
layout: post
title:  "Azure에 GitLab Runner 배포하기: 단계별 가이드"
author: jyseong
tag: [ Azure Virtual Machines , Update ]
category: [ Solution ]
image: assets/images/jyseong/images/2025-07-23-Deploying a GitLab Runner on Azure A Step-by-Step Guide/url_upload.jpg
---

### 작성자 : [NamanNihal](https://techcommunity.microsoft.com/users/namannihal/2904895)
### 원본 : [Deploying a GitLab Runner on Azure: A Step-by-Step Guide](https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deploying-a-gitlab-runner-on-azure-a-step-by-step-guide/4413348)

### CI/CD 파이프라인의 성능을 강화하기 위해 강력한 셀프 호스팅 솔루션을 찾고 있다면, Azure 가상 머신(VM)에 GitLab Runner를 배포하는 것이 좋습니다.

이 글에서는 Azure 가상 머신(VM)을 설정하고, GitLab Runner를 배포한 뒤, 첫 작업을 성공적으로 실행하는 단계까지의 전 과정을 차근차근 살펴보게 됩니다.

## 1단계: Azure 가상 머신(VM) 만들기
1. Azure 포털에 로그인합니다.  
2. 다음 설정으로 새 가상 머신(VM)을 생성하세요:
    - **이미지:** Ubuntu 20.04 LTS (권장)  
    - **인증 방식:** SSH 공개 키 (보안을 위해 .pem 파일 생성)
3. VM 생성이 완료되면 **공용 IP 주소**를 기록해 두세요.

###  VM에 연결하기
터미널에서 다음의 명령을 입력합니다.
```bash
ssh -i "/path/to/your/key.pem" admin_name@<YOUR_VM_PUBLIC_IP>
```
> 💡 **참고:**  
> 위 명령어에서 `<생성한_pem_파일>`과 `azureuser`는 VM을 생성할 때 직접 설정한  
> **.pem 파일 경로**와 **관리자 사용자 이름**으로 반드시 바꿔서 입력해야 합니다.


## 2단계: Azure VM에 Docker 설치하기
다음의 명령을 실행하여 Docker를 설치합니다.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker #Enable Docker to start automatically on boot
sudo usermod -aG docker $USER
```
2. Docker 설치가 완료되면 다음 명령어로 정상 작동하는지 테스트합니다.

```bash
docker run hello-world
```

3. 성공 메시지가 나타나야 합니다.
만약 permission denied 오류가 발생하면 아래 명령어를 실행합니다.

```bash
newgrp docker
```
> 💡 **참고:**  
> 그룹 변경 사항을 적용하려면 로그아웃 후 다시 로그인하거나, VM을 재시작해야 합니다.


## 3단계: GitLab Runner 설치

1. GitLab Runner 바이너리 다운로드:
2. 실행 권한 부여:
3. GitLab Runner를 서비스로 설치하고 시작:

```bash
#Step1
sudo chmod +x /usr/local/bin/gitlab-runner

#Step2
sudo curl -L --output /usr/local/bin/gitlab-runner \
https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

#Step3
sudo gitlab-runner install --user=azureuser
sudo gitlab-runner start
sudo systemctl enable gitlab-runner #Enable GitLab Runner to start automatically on boot
```

## 4단계: GitLab Runner 등록

1. GitLab에서 Runner 섹션으로 이동하여 등록 토큰을 생성합니다.  
   (`GitLab → Settings → CI/CD → Runners → New Project Runner`)

2. Azure VM에서 다음 명령어를 실행하세요:
```bash
sudo gitlab-runner register \
--url https://gitlab.com/ \
--registration-token <YOUR_TOKEN> \
--executor docker \
--docker-image Ubuntu:22.04 \
--description "Azure VM Runner" \
--tag-list "gitlab-runner-vm" \
--non-interactive
```
> 💡 **참고:**  
> 등록 시에는 등록 토큰(registration token), 설명(description), 태그 목록(tag-list)을 필요에 맞게 변경해서 입력합니다.

3. 등록이 완료되면, 다음 명령어로 Runner를 재시작합니다: ***sudo gitlab-runner restart***
4. 다음의 명령을 이용하여 Runner 상태를 확인합니다: ***sudo gitlab-runner list***

Runner가 목록에 나타나야 합니다.  
만약 Runner가 보이지 않는다면, 4단계 등록 과정을 다시 한번 정확히 따라 했는지 확인해보시기 바랍니다.

## 5단계: 파이프라인에 Runner 태그 추가하기

### In .gitlab-ci.yml
```yml
default:
tags:
- gitlab-runner-vm
```

## 6단계: 파이프라인 실행 확인하기

간단한 작업(job)을 생성하여, Runner를 테스트합니다:
```yml
test-runner:
tags:
- gitlab-runner-vm
script:
- echo "Runner is working!"
```

## 일반적인 문제 해결
### 권한 거부 오류 (Docker 관련)

**오류 메시지:**  
docker: permission denied while trying to connect to the Docker daemon socket


**해결 방법:**  
1. 먼저 아래 명령어를 실행하세요:  
    ```bash
    newgrp docker
    ```
2. 그래도 문제가 해결되지 않으면 Docker 서비스를 재시작하세요:
    ```bash
    sudo systemctl restart docker
    ```

## 활성화된 Runner 없음 오류

**오류 메시지:**  
This job is stuck because there are no active runners online.


**해결 방법:**  
1. Runner 상태 확인:  
    ```bash
    sudo gitlab-runner status
    ```
2. Runner가 비활성 상태라면 재시작:
    ```bash
    sudo gitlab-runner restart
    ```
3. 파이프라인에서 사용하는 Runner 태그가 프로젝트 등록 시 지정한 태그와 일치하는지 확인하세요.

# 마무리 팁

설정 변경 후에는 항상 Runner를 재시작하세요:  
  ```bash
  sudo gitlab-runner restart
```
주기적으로 Runner 상태를 확인하고, 원활한 동작을 위해 필요한 경우 설정을 업데이트하세요.

새로 구축한 GitLab Runner와 함께 즐거운 코딩 되시길 바랍니다!

----------

- 2025년 5월 13일 업데이트 됨.
- 2025년 7월 23일 번역 함. (by [JYSEONG(MSFT)](https://techcommunity.microsoft.com/users/ji%20yong%20seong/219866) / [GitHub](https://github.com/jiyongseong))