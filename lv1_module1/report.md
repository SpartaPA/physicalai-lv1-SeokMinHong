# 모듈 ① 과제 — 배달 로봇 온보딩

## 1. 배달 로봇의 연산 분담과 실시간성 설계

| 장치 | 갱신 주기 | 1회 데이터 | 데이터율 |
| --- | --- | --- | --- |
| 2D 라이다 | 15Hz(66.67ms) | 360 점 × (거리 4 B + 세기 4 B) = 2880 B |  |
| RGB 카메라 | 60fps (16.67ms) | 1280 x 720 x3 B =  |  | 
| IMU | 400Hz (2.5ms) | 가속도 3축 + 각속도 3축 × 4 B + 타임스탬프 8 B = 32 B |  |
| 바퀴 엔코더 | 2kHz (0.5ms) | 2륜 × 4 B = 8 B |  |
| LTE | - | - | 업링크 95Mbps , 다운로드 100Mbps |

### 1-1. 연산 분담 배치표
모터 속도 제어, 장애물 감지, 보행자 인식, 지도 기반 경로 계획, 배달 완료 사진 업로드, 운행 로그 집계

임베디드 / Edge AI / 클라우드

| 작업 | 위치 | 지연 예산 | 데이터량 | 근거 |
| --- | --- | --- | --- | --- |
| 모터 속도 제어 | 임베디드 | <= 0.5ms | 엔코더 8 KB/s + 명령 수 B/ms | 
| 장애물 감지 | Edge AI | <= 66.67ms | 
| 보행자 인식 | Edge AI | <= 66.67ms |
| 지도 기반 경로 계획 | 클라우드 |
| 배달 완료 사진 업로드 | 클라우드 |
| 운행 로그 집계 | 클라우드 |

### 1-2. 카메라 원시 영상 전송량

```
720p RGB 한 장 = 1280 x 720 x 3 B = 2,764,800 B ≈ 2.64 MB
60fps 이므로 2,764,800 B x 60 = 165,888,000 B/s ≈ 165.9 MB/s ≈ 158.2 MiB/s ≈ 1.327 Gbps
```
LTE 대비 LTE 업링크 95Mbps, 다운로드 100Mbps로는 원시 영상 전송이 불가능하다. 또한 지하나 터널 등 LTE 신호가 약한 환경에서는 연결이 끊길 수 있다.

### 1-3. 인지·판단·제어 계층 매핑과 주기표

|  | 


```
  엔코더 2 kHz ─┐
  IMU 400 Hz ───┼─▶ [인지] 오도메트리 400 Hz ─┐
  라이다 15 Hz ─┴─▶ [인지] 장애물 15 Hz ──────┼─▶ [판단] 지역 계획 10~20 Hz ─┐
  카메라 60 fps ──▶ [인지] 보행자 5~10 Hz ────┘        ▲                      │
                                                      │ 전역 경로 0.2~1 Hz    ▼
                                            (클라우드 지도)          [제어] PID 2 kHz ─▶ 모터
```

### 1-4. Hard / Firm / Soft 분류표

| 작업 | 등급 |
| --- | --- |
| 모터 속도 제어 | Hard |
| 장애물 감지 | Hard |
| 보행자 인식 | Firm |
| 지도 기반 경로 계획 | Soft |
| 배달 완료 사진 업로드 | Soft |
| 운행 로그 집계 | Soft |

**Hard 항목의 마감 초과 결과**

- 모터 속도 제어: 마감을 놓치면 의도한 속도를 넘어 가속하거나 진동이 발산한다.
- 장애물 감지: 마감을 놓치면 정지 거리가 늘어나며 충돌 위험이 증가한다.

### 1-5. 주기·지연·지터

- 주기:
- 지연:
- 지터:

## 2. 원격 접속(SSH)과 센서 장치 경로 고정

### 2-1. 고른 접속 대상: `서브 노트북`

![ssh_conection](./images/02_ssh_login.png)

### 2-2. 개인키·공개키 중 서버에 등록하는 것

공개키를 서버에 등록합니다. 개인키로만 서명 생성하기 때문입니다. 공개키는 개인키로 서명된 메시지를 검증하는 데 사용되기 때문에 서버에 등록합니다.

### 2-3. 원격 단일 명령 실행과 `scp` 전송 출력

```bash
ssh pa17@pa17 'uname -a'

scp hello pa17@pa17:~
```

![ssh_scp](./images/03_ssh_scp.png)

### 2-4. 두 장치를 구분한 속성

| 장치 | 구분 속성 | 값 |
|---|---|---|
| 라이다 | `ATTR{loop/backing_file}` | `*/lidar.img` |
| IMU | `ATTR{loop/backing_file}` | `*/imu.img` |

### 2-5. 작성한 udev 규칙 2개 + 규칙 키 설명표

```
SUBSYSTEM=="block", KERNEL=="loop*", ATTR{loop/backing_file}=="*/lidar.img", SYMLINK+="robot_lidar", MODE="0660", GROUP="dialout"
SUBSYSTEM=="block", KERNEL=="loop*", ATTR{loop/backing_file}=="*/imu.img", SYMLINK+="robot_imu", MODE="0660", GROUP="dialout"
```

규칙 키 설명
| 키 | 설명 |
| --- | --- |
| `SUBSYSTEM` | 서브시스템. loop 장치는 블록 장치이므로 `block`이다. |
| `KERNEL` | 커널에 붙인 장치 이름이다. |
| `ATTR{loop/backing_file}` | 장치 속성. loop 장치의 실제 파일 경로이다. |
| `SYMLINK+=` | 추가 이름(심볼릭 링크)을 만든다. 원래 이름은 그대로 남는다. |
| `MODE` | 장치 노드의 권환 소유자 및 그룹 권한 설정한다. |
| `GROUP` | 장치 노드의 그룹 소유자 설정한다. |

`==`와 `=`와 `+=`의 차이
| 연산자 | 역할 |
|---|---|---|
| `==` | 비교. 이 규칙을 적용할지 말지 고르는 매칭. 하나라도 안 맞으면 그 줄 전체가 건너뛰어진다. |
| `=` | 대입. 값을 통째로 설정한다(앞의 값을 덮어쓴다). |
| `+=` | 추가. 리스트형 키에 값을 덧붙인다. 심볼릭 링크는 여러 개일 수 있으므로 `+=` 를 쓴다. |

한줄을 읽을 때 `==` 조건이 전부 맞으면 `=`/`+=` 동작을 수행하라로 읽는다.

### 2-6. 순서를 바꿔 재연결한 뒤 `ls -l /dev/robot_*` 출력

```
sudo losetup -f --show lidar.img
sudo losetup -f --show imu.img

ls -l /dev/robot_* // 출력

// 순서를 바꿔 재연결
sudo losetup -f --show imu.img
sudo losetup -f --show lidar.img

ls -l /dev/robot_* // 출력
```

![udev_rules](./images/04_udev.png)

### 2-7. 실제 USB 센서용 규칙 초안과 구분 근거

```
SUBSYSTEM=="tty", ATTR{idVendor}=="10c4", ATTR{idVendor}=="ea60", SYMLINK+="robot_lidar", MODE="0660", GROUP="dialout"
SUBSYSTEM=="tty", ATTR{idVendor}=="10c4", ATTR{idVendor}=="ea70", SYMLINK+="robot_imu", MODE="0660", GROUP="dialout"
```

**`idVendor` 값이 같고 `idProduct` 값이 다른 경우**
idProduct으로 구분을 한다. 제조사가 같아도 제품 ID가 달라 서로 다른 장치로 인식한다.

## 3. 팀 저장소 협업 - 브랜치·충돌 해결·PR 리뷰

### 3-1. 저장소 URL / PR URL

### 3-2. PR리뷰 코멘트와 반영 커밋

### 3-3. 충돌이 난 파일과 줄

### 3-4. merge 방식 이력 그래프 / rebase 방식 이력 그래프

### 3-5. 언제 merge를, 언제 rebase를 쓸지
