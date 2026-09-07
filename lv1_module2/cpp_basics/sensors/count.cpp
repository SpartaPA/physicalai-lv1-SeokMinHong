#include <algorithm>
#include <cmath>
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "sensor.hpp"

// 함수 템플릿
// 값을 [lo, hi] 안으로 자른다. double 속도와 int 픽셀값에 같은 코드로 쓴다.
template <typename T>
T clamp_value(T v, T lo, T hi) {
    return (v < lo) ? lo : (hi < v) ? hi : v;
}

// 측정 로그 한 줄
struct Measurement {
    std::string sensor;
    double x;
    double y;
};

// 목표점까지의 거리
double distance_to(const Measurement& m, double gx, double gy) {
    return std::hypot(m.x - gx, m.y - gy);
}

int main(int argc, char** argv) {
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<Lidar>("front_lidar"));
    sensors.push_back(std::make_unique<Imu>("body_imu"));

    std::cout << "unordered_map / vector / count_if\n";
    std::unordered_map<std::string, double> latest;
    for (auto& s : sensors) {
        latest[s->name()] = s->read();
    }
    for (const auto& entry : latest) {
        std::cout << "  latest[" << entry.first << "] = " << entry.second << "\n";
    }

    const std::vector<Measurement> log = {
        {"front_lidar", 2.00, 3.00}, {"front_lidar", 2.20, 3.10},
        {"front_lidar", 2.60, 3.40}, {"body_imu", 2.05, 2.95},
        {"body_imu", 3.00, 3.90},    {"front_lidar", 1.90, 2.80},
        {"body_imu", 2.30, 3.05},
    };
    const double gx = 2.1, gy = 3.0;
    const auto near_count = std::count_if(
        log.begin(), log.end(),
        [&](const Measurement& m) { return distance_to(m, gx, gy) <= 0.35; });
        std::cout << "  목표 (" << gx << ", " << gy << ") 에서 0.35 m 이내 기록: "
                  << near_count << " / " << log.size() << " 개\n";

    return 0;
}
