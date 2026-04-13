#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def get_mode_config(context):
    """Функция, которая возвращает параметры в зависимости от режима"""
    mode = LaunchConfiguration('mode').perform(context)
    
    if mode == 'fast':
        frequency = 20.0
        threshold = 50
        topic = '/even_numbers_fast'
    else:  # slow по умолчанию
        frequency = 5.0
        threshold = 150
        topic = '/even_numbers_slow'
    
    overflow_topic = LaunchConfiguration('overflow_topic_name').perform(context)
    listener_name = LaunchConfiguration('listener_name').perform(context)
    
    return [
        Node(
            package='frog_pkg',
            executable='even_number_publisher',
            name='even_pub',
            parameters=[
                {'publish_frequency': frequency},
                {'overflow_threshold': threshold},
                {'topic_name': topic},
                {'enable_logging': True},
                {'overflow_topic': overflow_topic},
            ],
            output='screen',
        ),
        Node(
            package='frog_pkg',
            executable='overflow_listener',
            name=listener_name,
            remappings=[
                ('/overflow', overflow_topic),
            ],
            output='screen',
        ),
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'mode',
            default_value='slow',
            description='Режим работы: fast (20 Гц, порог 50) или slow (5 Гц, порог 150)'
        ),
        DeclareLaunchArgument(
            'overflow_topic_name',
            default_value='/overflow',
            description='Имя топика для переполнения'
        ),
        DeclareLaunchArgument(
            'listener_name',
            default_value='overflow_listener',
            description='Имя узла слушателя'
        ),
        OpaqueFunction(function=get_mode_config),
    ])