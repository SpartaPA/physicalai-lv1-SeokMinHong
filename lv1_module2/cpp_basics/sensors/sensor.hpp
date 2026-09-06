// sensors/sensor.hpp — 센서 계층 (문제 2: 상속·가상함수·RAII)
#ifndef SENSOR_HPP_
#define SENSOR_HPP_

#include <iostream>
#include <string>
#include <utility>
#include <vector>

// ---------------------------------------------------------------- 추상 기반
class Sensor {
 public:
    explicit Sensor(std::string name) : name_(std::move(name)) {
        std::cout << "  [ctor] Sensor(" << name_ << ")\n";
    }

    // 순수 가상 함수 — 파생 클래스가 반드시 구현해야 한다.
    virtual double read() = 0;

    // [핵심] 가상 소멸자.
    // 기반 클래스 포인터로 delete 할 때 파생 클래스의 소멸자까지 불리게 하려면 필요하다.
    // 이 virtual 을 빼면 ~Lidar() / ~Imu() 가 호출되지 않아 파생 클래스가 잡은 자원이 샌다
    // (표준상 undefined behavior). VIRTUAL_DTOR 매크로로 그 차이를 실험할 수 있다.
#ifdef NO_VIRTUAL_DTOR
#define DTOR_OVERRIDE                 /* 기반이 virtual 이 아니면 override 를 못 쓴다 */
    ~Sensor() {                       // 일부러 virtual 을 뺀 버전
#else
#define DTOR_OVERRIDE override
    virtual ~Sensor() {
#endif
        std::cout << "  [dtor] ~Sensor(" << name_ << ")\n";
    }

    const std::string& name() const { return name_; }

 private:
    std::string name_;
};

// ---------------------------------------------------------------- 파생 1
class Lidar : public Sensor {
 public:
    explicit Lidar(std::string name, int n_beams = 1080)
        : Sensor(std::move(name)), beams_(n_beams, 0.0) {
        std::cout << "  [ctor] Lidar (빔 " << beams_.size() << "개 버퍼 확보)\n";
    }

    // override 를 붙이면 시그니처가 어긋났을 때 컴파일 단계에서 잡힌다.
    double read() override {
        tick_ += 1;
        return 2.0 + 0.5 * ((tick_ % 7) - 3);   // 재현 가능한 가짜 거리 [m]
    }

    ~Lidar() DTOR_OVERRIDE {
        std::cout << "  [dtor] ~Lidar (빔 버퍼 " << beams_.size() << "개 해제)\n";
    }

 private:
    std::vector<double> beams_;
    int tick_ = 0;
};

// ---------------------------------------------------------------- 파생 2
class Imu : public Sensor {
 public:
    explicit Imu(std::string name) : Sensor(std::move(name)) {
        std::cout << "  [ctor] Imu\n";
    }

    double read() override {
        tick_ += 1;
        return 0.01 * ((tick_ % 5) - 2);        // 가짜 각속도 [rad/s]
    }

    ~Imu() DTOR_OVERRIDE { std::cout << "  [dtor] ~Imu\n"; }

 private:
    int tick_ = 0;
};

#endif  // CPP_BASICS_SENSORS_SENSOR_HPP_
