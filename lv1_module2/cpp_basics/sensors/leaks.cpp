#include <iostream>
#include <memory>
#include <string>


#include "sensor.hpp"

int main(int argc, char** argv) {
    auto leak_mode = (argc >= 2 && std::string(argv[1]) == "leak");

    std::cout << "메모리 누수\n";
    if (leak_mode) {
        std::cout << "[leak] new 로 100개 할당하고 delete 하지 않는다\n";
        for (int i = 0; i < 100; ++i) {
            Sensor* raw = new Lidar("leaky_lidar", 16);
            (void)raw->read();
            // delete raw; 일부러 하지 않는다.
        }
    } else {
        std::cout << "make_unique 로 100개 할당 — 스코프를 벗어나며 자동 해제\n";
        for (int i = 0; i < 100; ++i) {
            auto owned = std::make_unique<Lidar>("safe_lidar", 16);
            (void)owned->read();
        }
    }
    return 0;
}
