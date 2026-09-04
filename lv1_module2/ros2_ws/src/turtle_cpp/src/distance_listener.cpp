#include <chrono>
#include <functional>
#include <memory>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"

using namespace std::chrono_literals;

class DistanceListener: public rclcpp::Node {
    public:
        DistanceListener() : Node("turtle_distance_listener") {
            distance_sub_ = this->create_subscription<std_msgs::msg::Float32>(
                "/turtle_distance", 10,
                [this](std_msgs::msg::Float32::ConstSharedPtr msg) {
                    RCLCPP_INFO(this->get_logger(), "거리 %.3f m", msg->data);
                }
            );
            RCLCPP_INFO(this->get_logger(), "구독 시작 (C++) — /turtle_distance");
        }

    private:
        rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr distance_sub_;
};

int
main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DistanceListener>());
    rclcpp::shutdown();
    return 0;

}
