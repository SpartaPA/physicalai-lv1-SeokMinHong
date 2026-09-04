#ifndef MOTOR_HPP
#define MOTOR_HPP

class Motor {
    private:
        double current_speed_ = 0.0;

    public:
        void setSpeed(double mps);
};

#endif
