#include <iostream>
#include <string>

#include "sensor.hpp"


void control_loop() {
    std::cout << "[스코프 진입]\n";
    Imu stack_imu("imu_on_stack");


    std::cout << "[스코프 끝 직전]\n";
}

int main(int argc, char** argv) {
    std::cout << "스택 vs 힙 — 생성/소멸 시점 관찰\n\n";
    Imu* p = new Imu("imu_on_heap");
    control_loop();

    delete p;


    return 0;
}
