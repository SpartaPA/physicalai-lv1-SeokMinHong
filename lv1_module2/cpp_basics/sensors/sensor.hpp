#ifndef SENSOR_HPP_
#define SENSOR_HPP_

#include <iostream>
#include <string>
#include <utility>
#include <vector>

class Sensor {
 public:
    explicit Sensor(std::string name) : name_(std::move(name)) {
        std::cout << "[생성] Sensor (" << name_ << ")\n";
    }

    virtual double read() = 0;

    virtual ~Sensor() {
        std::cout << "[소멸] ~Sensor (" << name_ << ")\n";
    }

    const std::string& name() const { return name_; }

 private:
    std::string name_;
};


class Lidar : public Sensor {
 public:
    explicit Lidar(std::string name, int n_beams = 1080)
        : Sensor(std::move(name)), beams_(n_beams, 0.0) {
        std::cout << "[생성] Lidar\n";
    }

    double read() override {
        tick_ += 1;
        return 2.0 + 0.5 * ((tick_ % 7) - 3);
    }

    ~Lidar() {
        std::cout << "[소멸] ~Lidar\n";
    }

 private:
    std::vector<double> beams_;
    int tick_ = 0;
};

class Imu : public Sensor {
 public:
    explicit Imu(std::string name) : Sensor(std::move(name)) {
        std::cout << "[생성] Imu\n";
    }

    double read() override {
        tick_ += 1;
        return 0.01 * ((tick_ % 5) - 2);
    }

    ~Imu() { std::cout << "[소멸] ~Imu\n"; }

 private:
    int tick_ = 0;
};

#endif
