#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String     
from std_msgs.msg import Int32

class even_number_publisher(Node):

    def __init__(self):
        super().__init__('even_number_publisher')
        
        # Объявляем параметры которые можно будет менять извне с значениями по умолчанию
        self.declare_parameter('publish_frequency', 10.0)#Гц
        self.declare_parameter('overflow_threshold', 100)#порог сброса
        self.declare_parameter('topic_name', '/even_numbers')#имя топика куда публиковать четные числа
        self.declare_parameter('enable_logging', True)#включать/выключать логи
        self.declare_parameter('overflow_topic', '/overflow')#имя топика куда публиковать счетчик

        # Читаем параметры
        self.freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        self.topic = self.get_parameter('topic_name').value
        self.enable_logging = self.get_parameter('enable_logging').value
        self.overflow_topic = self.get_parameter('overflow_topic').value

        # Создаём издатели
        self.publisher_even_numbers = self.create_publisher(Int32, self.topic, 10)
        #self.publisher_overflow = self.create_publisher(String, 'overflow', 10)
        self.publisher_overflow = self.create_publisher(String, self.overflow_topic, 10)

        # Таймер с частотой из параметра
        self.timer = self.create_timer(1.0 / self.freq, self.timer_callback)

        # Счётчик
        self.counter = 0
        
        #Выводит информационное сообщение, чтобы мы видели, с какими настройками запустился узел.
        self.get_logger().info(f"even_number_publisher started: freq={self.freq}Hz, threshold={self.threshold}, topic={self.topic}")

    def timer_callback(self):
        msg = Int32() #Создаётся сообщение типа Int32
        msg.data = self.counter #в его поле data кладётся текущее значение счётчика
        
        # Отправляем чётное число
        self.publisher_even_numbers.publish(msg)#Публикуем сообщение с чётным числом.
        if self.enable_logging:#Если параметр enable_logging установлен в True, то выводим это число в лог
            self.get_logger().info(str(msg.data))
        
        # Обновляем счётчик
        self.counter += 2
        
        # Если счётчик достиг или превысил порог self.threshold, то сбрасываем его в 0.
        if self.counter >= self.threshold: 
            self.counter = 0
            
            # Создаётся и отправляется сообщение-предупреждение в топик overflow.
            overflow_msg = String()
            overflow_msg.data = f"Счётчик обнулился! Достигнут порог {self.threshold}"
            self.publisher_overflow.publish(overflow_msg)
            self.get_logger().info(f" to topic{self.overflow_topic}: {overflow_msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = even_number_publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()