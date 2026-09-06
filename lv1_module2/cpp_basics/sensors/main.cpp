#include <algorithm>
#include <cmath>
#include <iomanip>
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


void scope_demo() {
    std::cout << "[스코프 진입]\n";
    Imu stack_imu("imu_on_stack");                       // 스택 객체
    auto heap_imu = std::make_unique<Imu>("imu_on_heap");  // 힙 객체 (unique_ptr 가 소유)
    std::cout << "[스코프 끝 직전] — 아래 소멸자 두 개는 여기서 자동 호출된다\n";
}

int main(int argc, char** argv) {
    const bool leak_mode = (argc >= 2 && std::string(argv[1]) == "leak");

    // 1. 다형성 루프 
    std::cout << "=== 1. 다형성 루프 ===\n";
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<Lidar>("front_lidar"));
    sensors.push_back(std::make_unique<Imu>("body_imu"));

    std::cout << std::fixed << std::setprecision(3);
    for (int step = 0; step < 3; ++step) {
        for (auto& s : sensors) {
            // s 는 Sensor* 지만 실제로 불리는 것은 Lidar::read / Imu::read (동적 바인딩)
            std::cout << "  step " << step << "  " << s->name() << " -> " << s->read() << "\n";
        }
    }

    // 2. 스택 vs 힙 소멸 시점 
    std::cout << "\n=== 2. 스택 객체와 힙 객체의 소멸 시점 ===\n";
    scope_demo();
    std::cout << "[스코프 벗어남] — 위 소멸자들이 이미 모두 호출되었다\n";

    // 3. STL 컨테이너와 count_if
    std::cout << "\n=== 3. unordered_map / vector / count_if ===\n";
    std::unordered_map<std::string, double> latest;      // 센서 이름 -> 최근 측정값
    for (auto& s : sensors) {
        latest[s->name()] = s->read();
    }
    for (const auto& [name, value] : latest) {
        std::cout << "  latest[" << name << "] = " << value << "\n";
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

    //  4. 함수 템플릿 ----------
    std::cout << "\n=== 4. 함수 템플릿 clamp_value ===\n";
    const double speed = clamp_value(2.7, 0.0, 1.5);
    const int pixel = clamp_value(300, 0, 255);
    std::cout << "  clamp_value(2.7, 0.0, 1.5) = " << speed << "  (double)\n";
    std::cout << "  clamp_value(300, 0, 255)   = " << pixel << "  (int)\n";

    // 5. 누수 재현과 수정 ----------
    std::cout << "\n=== 5. 메모리 누수 ===\n";
    if (leak_mode) {
        std::cout << "  [leak] new 로 100개 할당하고 delete 하지 않는다\n";
        for (int i = 0; i < 100; ++i) {
            Sensor* raw = new Lidar("leaky_lidar", 16);
            (void)raw->read();
            // delete raw; 일부러 하지 않는다.
        }
    } else {
        std::cout << "  [fixed] make_unique 로 100개 할당 — 스코프를 벗어나며 자동 해제\n";
        for (int i = 0; i < 100; ++i) {
            auto owned = std::make_unique<Lidar>("safe_lidar", 16);
            (void)owned->read();
        }
    }

    std::cout << "\n=== 종료 — sensors 벡터의 소멸자가 이제 호출된다 ===\n";
    return 0;
}
