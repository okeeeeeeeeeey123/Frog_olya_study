#!/usr/bin/env python3
import rclpy                        # главная библиотека ROS 2
from rclpy.node import Node         # от неё наследуемся
from std_msgs.msg import String     # тип сообщения — строка

class Listener(Node):

    def __init__(self):
        # Даём узлу имя "listener"
        super().__init__('listener')

        # Создаём подписку на топик
        # Название топика     → 'my_chat_topic'
        # Тип сообщения       → String
        # Функция-обработчик  → self.callback
        # 10 — размер очереди
        self.subscription = self.create_subscription(
            String,
            'my_chat_topic',
            self.callback,
            10)

        self.get_logger().info("Узел listener запущен и слушает топик!")

    # Эта функция будет автоматически вызываться каждый раз,
    # когда придёт новое сообщение
    def callback(self, msg):
        # msg — это пришедшее сообщение
        # msg.data — это строка внутри сообщения
        self.get_logger().info(f"Я услышал: {msg.data}")

def main():
    rclpy.init()                    # стартуем ROS 2
    node = Listener()               # создаём наш узел
    try:
        rclpy.spin(node)            # крутимся и ждём сообщений
    except KeyboardInterrupt:
        pass                        # Ctrl+C — нормально выходим
    finally:
        node.destroy_node()         # убираем узел
        rclpy.shutdown()            # завершаем ROS 2

if __name__ == '__main__':
    main()