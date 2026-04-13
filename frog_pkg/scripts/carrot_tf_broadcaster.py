#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster# Класс для публикации динамических трансформаций в TF2
from geometry_msgs.msg import TransformStamped# TF2 ожидает сообщения именно этого типа
import math
from turtlesim.msg import Pose  # подпишемся на положение черепашки

class CarrotTFBroadcaster(Node):
    def __init__(self):
        super().__init__('carrot_tf_broadcaster')
        
        # Создаёт объект для публикации трансформаций, Внутри создаёт издатель в топик /tf
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Подписка на положение черепашки (топик /turtle1/pose)
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        # Параметры вращения морковки
        self.radius = 1.5          # радиус вращения (метры)
        self.angular_speed = 0.8   # скорость вращения (радиан/секунда)
        
        self.current_angle = 0.0   # текущий угол морковки
        self.last_time = self.get_clock().now()# Нужно для вычисления dt (разницы во времени между кадрами)
        
        self.get_logger().info("Carrot TF Broadcaster запущен")

    def pose_callback(self, pose_msg):
        # Получаем текущее время
        now = self.get_clock().now()
        
        # Вычисляем время с прошлого кадра
        dt = (now - self.last_time).nanoseconds / # 1e9Делит на 1 миллиард, чтобы получить секунды 
        if dt > 0.1:  # ограничиваем максимальный шаг
            dt = 0.1
            
        # Обновляем угол морковки
        self.current_angle += self.angular_speed * dt
        if self.current_angle > 2 * math.pi:
            self.current_angle -= 2 * math.pi
            
        # Вычисляем координаты морковки относительно черепашки
        carrot_x = self.radius * math.cos(self.current_angle)
        carrot_y = self.radius * math.sin(self.current_angle)
        
        # Создаём сообщение трансформации
        t = TransformStamped() # Создаёт пустое сообщение типа TransformStamped
        t.header.stamp = now.to_msg() # Время, когда была измерена трансформация Преобразует ROS 2 Time в формат сообщения
        t.header.frame_id = 'turtle1'        # От какой системы координат мы считаем положение
        t.child_frame_id = 'carrot_frame'    # Какая система координат является "дочерней"
        
        # Смещение морковки
        t.transform.translation.x = carrot_x
        t.transform.translation.y = carrot_y
        t.transform.translation.z = 0.0
        
        # Без поворота (кватернион для единичного поворота)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        # Публикуем трансформацию
        self.tf_broadcaster.sendTransform(t) # Отправляет сообщение в топик /tf
        
        # Сохраняем время для следующего шага
        self.last_time = now #Чтобы в следующий раз правильно вычислить dt

def main(args=None):
    rclpy.init(args=args)
    node = CarrotTFBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()