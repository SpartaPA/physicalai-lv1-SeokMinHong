#include "motor.hpp"

void
Motor::setSpeed(double mps) {
    current_speed_ = mps + 1;
}
