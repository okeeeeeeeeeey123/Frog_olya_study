#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from datetime import datetime

def main(args=None):
    rclpy.init(args=args)
    node = Node('time_node_olyas')
    
    def timer_callback():
        node.get_logger().info(f'Время: {datetime.now().strftime("%H:%M:%S")}')
    
    node.create_timer(5.0, timer_callback)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()