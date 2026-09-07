import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


class TurtleTF2Broadcaster(Node):
    def __init__(self):
        super().__init__("turtlesim_tf2_broadcaster")

        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.on_msg, 10)
        self.tf2_bd = TransformBroadcaster(self)

    def on_msg(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"
        t.child_frame_id = "turtle1"
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y

        t.transform.rotation.z = math.sin(msg.theta / 2.0)  # 회전은 쿼터니언으로(20강)
        t.transform.rotation.w = math.cos(msg.theta / 2.0)

        self.tf2_bd.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTF2Broadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
