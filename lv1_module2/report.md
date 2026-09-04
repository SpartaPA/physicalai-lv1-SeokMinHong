# 모듈 ② 과제 — turtlesim 기반 C++·Python ROS2 패키지 개발

## 1. C++ 빌드 체계 세우기 - g++ 다중 파일 빌드와 CMake 전환

### 1-1. **수동 2단계 빌드 명령** (터미널 입력)
```bash
g++ -Wall -std=c++17 -c main.cpp motor.cpp

g++ -Wall -std=c++17 main.o motor.o -o main
```

### 1-2. **`undefined reference` 에러 메시지** (출력) - 컴파일 에러와의 차이 설명

![undefined_reference](./images/01_undefined_reference.png)

### 1-3. **CMake빌드 출력** (터미널 출력)

![cmake_build](./images/02_cmake_build.png)

### 1-4. 증분 빌드 시 재컴파일된 파일

`motor.cpp` 파일만 재컴파일 됩니다. 그렇게 판단한 이유는 `main.cpp` 파일은 수정되지 않았기 때문에, 이전에 컴파일된 `main.o` 파일을 재사용하고, 변경된 `motor.cpp` 파일만 새로 컴파일하여 `motor.o` 파일을 생성합니다. 따라서 증분 빌드 시에는 변경된 소스 파일만 재컴파일되어 빌드 시간을 단축시킬 수 있습니다.

## 2. 현대 C++로 센서 계층 구현 - RAII·다형성·STL
### 2-1. 다형성 루프 출력
### 2-2. 스택 객체와 힙 객체의 소멸 시점 - 관찰 로그와 설명
### 2-3. 가상 소멸자를 뺐을 때의 차이
### 2-4. `count_if` 결과
### 2-5. 누수 검출 결과 -> 수정 후 결과


## 3. rclpy 노드 작성 - 거북이 상태 발행자와 구독자

### 3-1. `/turtle1/pose` 필드 구성

```
❯ ros2 topic echo /turtle1/pose
x: 5.544444561004639
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
---
```

```
❯ ros2 interface show /turtlesim/msg/Pose
float32 x
float32 y
float32 theta

float32 linear_velocity
float32 angular_velocity
```

![]

### 3-2. `ros2 topic hz /turtle_distance`

출력이 대략 9.998 (10hz 근접) 한다.

```
ros2 topic hz /turtle_distance
```

![turtle_distance_hz](./images/03_turtle_distance_hz.png)


### 3-3. 구독자 경고 로그 (터미널 출력)

![turtle_distance_warning](./images/04_turtle_warning.png)

### 3-4. 구독자 2개 동시 수신 확인 (양쪽 로그)



### 3-5. 주행 캡쳐 (turtlesim 화면)

![turtlesim_capture](./images/04_turtlesim_draw.png)

### 3-6. Ctrl+C 정상 종료 화면 (출력)
