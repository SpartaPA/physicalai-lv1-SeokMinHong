// stop_distance.cpp — 로봇의 제동(정지) 거리 계산
//
// 물리: 바퀴와 바닥 사이 마찰이 유일한 제동력이라고 보면
//   감속도 a = mu * g   (mu: 마찰계수, g: 중력가속도)
//   운동에너지 (1/2)m v^2 이 마찰일 (mu m g d) 로 모두 소모되어 정지하므로
//   d = v^2 / (2 * mu * g)
// ./stop_distance <속도[m/s]> <마찰계수>

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

constexpr double GRAVITY = 9.81;

using std::cout;
using std::endl;

// 인자 문자열 하나를 double로 변환한다.
// 변환 실패 / 범위 초과 / 뒤에 잡문자 / nan·inf 는 모두 runtime_error 로 보고한다.
static double
parse_double(const char* name, const char* arg) {
    std::size_t pos = 0;
    double value = 0.0;

    try {
        value = std::stod(arg, &pos);
    } catch (const std::invalid_argument&) {
        throw std::runtime_error(std::string(name) + ": 숫자로 해석할 수 없습니다 -> \"" + arg + "\"");
    } catch (const std::out_of_range&) {
        throw std::runtime_error(std::string(name) + ": double 표현 범위를 벗어났습니다 -> \"" + arg + "\"");
    }

    if (!std::isfinite(value)) {
        throw std::runtime_error(std::string(name) + ": 유한한 수가 아닙니다 -> \"" + arg + "\"");
    }

    return value;
}

double
stop_distance(double v, double mu) {
    return v * v / (2 * mu * GRAVITY);
}

int
main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <속도[m/s]> <마찰계수>" << endl;
        return 1;
    }

    double mu = 0.0;
    double v = 0.0;

    try {
        v = parse_double("속도(v)", argv[1]);
        mu = parse_double("마찰계수(mu)", argv[2]);

        if (mu <= 0.0) {
            throw std::runtime_error("마찰계수(mu)는 0보다 커야 합니다 -> " + std::to_string(mu));
        }
    } catch (const std::runtime_error& e) {
        std::cerr << "입력 오류: " << e.what() << std::endl;
        std::cerr << "Usage: " << argv[0] << " <속도[m/s]> <마찰계수>" << endl;
        return 1;
    }

    double d = stop_distance(v, mu);
    cout << "정지거리: " << d << " 속도: " << v << " m/s" << " 마찰계수: " << mu << endl;
    return 0;
}
