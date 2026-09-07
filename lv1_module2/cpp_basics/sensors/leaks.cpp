#include <iostream>
#include <memory>
#include <string>


#include "sensor.hpp"

void make_leaks() {
    std::cout << "[leak] new 로 100개 할당하고 delete 하지 않는다\n";
    for (int i = 0; i < 100; ++i) {
        Sensor* raw = new Lidar("leaky_lidar", 16);
        (void)raw->read();
        // delete raw;  // 주석 처리하여 메모리 누수 발생
    }
}

void make_safe() {
    std::cout << "[safe] make_unique 로 100개 할당 — 스코프를 벗어나며 자동 해제\n";
    for (int i = 0; i < 100; ++i) {
        auto owned = std::make_unique<Lidar>("safe_lidar", 16);
        (void)owned->read();
    }
}

int main(void) {

    std::cout << "메모리 누수\n";
    make_leaks();

    return 0;
}
