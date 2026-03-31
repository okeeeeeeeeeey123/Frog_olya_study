
#!/usr/bin/env python3
import rclpy                        # это главная библиотека ROS 2 для Python
from rclpy.node import Node         # от неё будем наследоваться
from std_msgs.msg import String     # тип сообщения — просто строка

# ────────────────────────────────────────────────
# 1. Создаём класс — это и есть наш узел
# ────────────────────────────────────────────────
class Talker(Node):

    def __init__(self):
        # Даём узлу имя "talker"
        super().__init__('talker')

        # Создаём "почтовый ящик" — место, куда будем отправлять сообщения
        # Название топика → 'my_chat_topic'
        # Тип сообщения → строка
        # 10 — размер очереди (сколько сообщений можно временно держать)
        self.publisher = self.create_publisher(String, 'my_chat_topic', 10)

        # Говорим: "каждую 1 секунду вызывай функцию timer_callback"
        timer_period = 1.0          # 1 секунда = 1 Гц
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info("Узел talker запущен!")

    # ────────────────────────────────────────────────
    # 2. Эта функция будет вызываться каждую секунду
    # ────────────────────────────────────────────────
    def timer_callback(self):
        msg = String()                      # создаём пустое сообщение
        msg.data = f"Привет! Сейчас {self.get_clock().now().to_msg().sec}"  # пишем текст

        self.publisher.publish(msg)         # отправляем сообщение в топик
        self.get_logger().info(msg.data)    # показываем себе в терминале


# ────────────────────────────────────────────────
# 3. Главная функция — точка входа
# ────────────────────────────────────────────────
def main():
    rclpy.init()                    # начинаем работать с ROS 2

    node = Talker()                 # создаём наш узел

    try:
        rclpy.spin(node)            # "крутимся" и ждём событий (таймеров, сообщений и т.д.)
    except KeyboardInterrupt:
        pass                        # если нажали Ctrl+C — нормально выходим
    finally:
        node.destroy_node()         # убираем узел
        rclpy.shutdown()            # завершаем ROS 2


if __name__ == '__main__':
    main()
