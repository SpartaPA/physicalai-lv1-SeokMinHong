#include <iostream>
#include <memory>
#include <vector>

#include "sensor.hpp"

int main(int argc, char** argv) {
    std::cout << "다형성 루프\n";
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<Lidar>("front_lidar"));
    sensors.push_back(std::make_unique<Imu>("body_imu"));

    return 0;
}
