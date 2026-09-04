#include <chrono>
#include <memory>
#include <optional>

#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "std_msgs/msg/float32.hpp"

using namespace std::chrono_literals;

class DistancePublisher : public rclcpp::Node {
    public:
        DistancePublisher() : Node("turtle_distance") {
            pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
                "turtle1/pose", 10,
                [this](turtlesim::msg::Pose::ConstSharedPtr msg) {
                    latest_pose_ = *msg;
                }
            );
            distance_pub_ = this->create_publisher<std_msgs::msg::Float32>(
                "/turtle_distance",
                10
            );
            timer_ = this->create_wall_timer(
                100ms,
                [this]() { this->publish_distance(); }
            );
        }

    private:
        rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr distance_pub_;
        rclcpp::TimerBase::SharedPtr timer_;
        std::optional<turtlesim::msg::Pose> latest_pose_;

        void publish_distance() {
            if (!latest_pose_.has_value()) {
                RCLCPP_WARN_THROTTLE(this->get_logger(), *this->get_clock(), 5000,
                                     "아직 /turtle1/pose 를 받지 못했습니다.");
                return;
            }
            std_msgs::msg::Float32 msg;
            msg.data = static_cast<float>(std::hypot(latest_pose_->x, latest_pose_->y));
            distance_pub_->publish(msg);
        }
};

int
main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DistancePublisher>());
    rclcpp::shutdown();
    return 0;

}
