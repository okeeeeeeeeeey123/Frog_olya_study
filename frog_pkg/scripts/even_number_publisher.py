
#!/usr/bin/env python3
import rclpy                        # это главная библиотека ROS 2 для Python
from rclpy.node import Node         # от неё будем наследоваться
from std_msgs.msg import String     
from std_msgs.msg import Int32      # тип сообщения — Int32

# ────────────────────────────────────────────────
# 1. Создаём класс — это и есть наш узел
# ────────────────────────────────────────────────
class even_number_publisher(Node):

    def __init__(self):
        # Даём узлу имя "even_number_publisher"
        super().__init__('even_number_publisher')

        # Создаём "почтовый ящик" — место, куда будем отправлять сообщения
        # Название топика → 'even_numbers'
        # Тип сообщения → std_msgs/msg/Int32 (или Int64)
        # 10 — размер очереди (сколько сообщений можно временно держать)
        self.publisher_even_numbers = self.create_publisher(Int32, 'even_numbers', 10)
        self.publisher_overflow = self.create_publisher(String, 'overflow', 10)

        # Говорим: "каждую 0.1 секунду вызывай функцию timer_callback"
        timer_period = 0.1          # 1 секунда = 1 Гц
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info("even_number_publisher")

    # ────────────────────────────────────────────────
    # 2. Эта функция не будет вызываться каждую секунду
    # ────────────────────────────────────────────────
    def timer_callback(self):
        #msg = String()                      # создаём пустое сообщение
        msg = Int32()                       # создаём сообщение типа Int32
        #msg.data = f"Привет! Сейчас {self.get_clock().now().to_msg().sec}"  # пишем текст

        # Инициализируем счётчик, если его ещё нет
        if not hasattr(self, 'counter'):
            self.counter = 0
        
        # Записываем текущее чётное число в поле data
        msg.data = self.counter

        # Обновляем счётчик: увеличиваем на 2, но если достигли 100 — сбрасываем на 0
        self.counter += 2
        if self.counter >= 100:
            self.counter = 0
            # СОЗДАЁМ И ОТПРАВЛЯЕМ СПЕЦИАЛЬНОЕ СООБЩЕНИЕ В ТОПИК overflow
            overflow_msg = String()
            overflow_msg.data = "Счётчик обнулился! Начинаем с 0"
            self.publisher_overflow.publish(overflow_msg)
            self.get_logger().info(f"→→→ overflow: {overflow_msg.data}")

        self.publisher_even_numbers.publish(msg)         # отправляем сообщение в топик
        self.get_logger().info(str(msg.data))    # показываем себе в терминале


# ────────────────────────────────────────────────
# 3. Главная функция — точка входа
# ────────────────────────────────────────────────
def main():
    rclpy.init()                    # начинаем работать с ROS 2

    node = even_number_publisher()                 # создаём наш узел

    try:
        rclpy.spin(node)            # "крутимся" и ждём событий (таймеров, сообщений и т.д.)
    except KeyboardInterrupt:
        pass                        # если нажали Ctrl+C — нормально выходим
    finally:
        node.destroy_node()         # убираем узел
        rclpy.shutdown()            # завершаем ROS 2


if __name__ == '__main__':
    main()
