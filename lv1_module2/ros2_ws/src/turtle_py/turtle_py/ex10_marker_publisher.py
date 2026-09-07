#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import Point
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from turtle_interfaces.msg import WaypointList
from visualization_msgs.msg import Marker, MarkerArray


class WaypointMarkerPublisher(Node):

    def __init__(self):
        super().__init__('waypoint_marker_publisher')

        qos = QoSProfile(history=HistoryPolicy.KEEP_LAST, depth=1,
                         reliability=ReliabilityPolicy.RELIABLE,
                         durability=DurabilityPolicy.TRANSIENT_LOCAL)

        self._pub = self.create_publisher(MarkerArray, 'waypoint_markers', qos)
        self._sub = self.create_subscription(WaypointList, 'waypoints', self._on_waypoints, qos)
        self.get_logger().info('/waypoints -> /waypoint_markers 변환 시작 (Fixed Frame: world)')

    def _on_waypoints(self, msg: WaypointList) -> None:
        if not msg.waypoints:
            self.get_logger().warn('경유점이 비어 있어 마커를 만들지 않습니다.')
            return

        now = self.get_clock().now().to_msg()
        points = Marker()
        points.header.frame_id = 'world'
        points.header.stamp = now
        points.ns = 'waypoints'
        points.id = 0
        points.type = Marker.SPHERE_LIST
        points.action = Marker.ADD
        points.scale.x = points.scale.y = points.scale.z = 0.4
        points.color.r, points.color.g, points.color.b, points.color.a = 1.0, 0.55, 0.0, 1.0
        points.pose.orientation.w = 1.0

        line = Marker()
        line.header = points.header
        line.ns = 'waypoint_path'
        line.id = 1
        line.type = Marker.LINE_STRIP
        line.action = Marker.ADD
        line.scale.x = 0.08
        line.color.r, line.color.g, line.color.b, line.color.a = 0.1, 0.6, 1.0, 0.9
        line.pose.orientation.w = 1.0

        for wp in msg.waypoints:
            p = Point(x=float(wp.x), y=float(wp.y), z=0.0)
            points.points.append(p)
            line.points.append(p)

        self._pub.publish(MarkerArray(markers=[points, line]))
        self.get_logger().info(f'마커 발행 — 경유점 {len(msg.waypoints)} 개')


def main(args=None):
    rclpy.init(args=args)
    node = WaypointMarkerPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        node.get_logger().info('종료 요청을 받았습니다 (Ctrl+C).')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
