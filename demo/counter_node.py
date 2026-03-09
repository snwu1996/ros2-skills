#!/usr/bin/env python3
"""Counter node — publishes an incrementing Int32 on /counter at 1 Hz."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class CounterNode(Node):
    def __init__(self):
        super().__init__('counter_node')
        self.publisher_ = self.create_publisher(Int32, '/counter', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info('Counter node started — publishing to /counter at 1 Hz')

    def timer_callback(self):
        msg = Int32()
        msg.data = self.count
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {self.count}')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = CounterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
