#!/usr/bin/env python3
"""Первый узел ROS 2 — Hello World"""

import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args)                   # инициализация ROS 2
    node = Node('hello_node')               # создаём узел с именем hello_node
    node.get_logger().info("Hello ROS 2 World! 🚀")
    rclpy.spin(node)                        # запускаем цикл обработки
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
