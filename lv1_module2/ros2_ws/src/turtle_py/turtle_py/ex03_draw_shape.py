import sys
import time

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rcl_interfaces.msg import ParameterDescriptor, SetParametersResult
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class TurtleDrawShape(Node):

    def __init__(self):
        super().__init__("turtle_draw")

        self.declare_parameter(
            "sides", 3,
            ParameterDescriptor(description="도형의 변 개수 3, 5, 6만 가능")
        )
        self.sides = self.get_parameter("sides").value

        self._draw_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.x = 0
        self.y = 0
        self.get_logger().info("도형 그리기 노드 실행")

    def _on_set_parameters(self, params):
        for param in params:
            if param.name != "sides":
                continue
            if param.type != param.Type.INTEGER:
                return SetParametersResult(successful=False, reason="sides 는 정수여야 합니다")
            elif param.value not in [3, 5, 8]:
                return SetParametersResult(successful=False, reason="sides 는 3, 5, 8만 가능합니다")
            self.get_logger().info(f"sides 변경 → {param.value}")
        return SetParametersResult(successful=True)

    def move(self):
        self.get_logger().info("도형 그리기 이동 시작")

        move_msg, angle_msg = Twist(), Twist()
        move_msg.linear.x = 2.0
        angle_msg.angular.z = np.deg2rad(180 - (180 * (self.sides - 2)) / self.sides)

        move_time = 2. / 2
        angle_time = np.pi / 2
        for _ in range(self.sides):
            self._draw_pub.publish(move_msg)
            time.sleep(move_time)
            self._draw_pub.publish(angle_msg)
            time.sleep(angle_time)
        self.get_logger().info("도형 그리기 이동 완료")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleDrawShape()
    try:
        node.move()
    except (KeyboardInterrupt, ExternalShutdownException):
        node.get_logger().info('Ctrl+C - 정상 종료합니다')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
