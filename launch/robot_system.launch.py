#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # Аргументы для even_number_publisher
    freq_arg = DeclareLaunchArgument(
        'publish_frequency',
        default_value='8.0',
        description='Частота публикации чётных чисел (Гц)'
    )

    threshold_arg = DeclareLaunchArgument(
        'overflow_threshold',
        default_value='80',
        description='Порог, после которого происходит переполнение'
    )

    topic_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='/even_numbers_fast',
        description='Имя топика для чётных чисел'
    )

    logging_arg = DeclareLaunchArgument(
        'enable_logging',
        default_value='true',
        description='Включить логирование'
    )

    # Аргументы для overflow_listener
    listener_name_arg = DeclareLaunchArgument(
        'listener_name',
        default_value='overflow_listener',
        description='Имя узла слушателя'
    )

    # Получаем значения аргументов
    frequency = LaunchConfiguration('publish_frequency')
    threshold = LaunchConfiguration('overflow_threshold')
    topic_name = LaunchConfiguration('topic_name')
    enable_logging = LaunchConfiguration('enable_logging')
    listener_name = LaunchConfiguration('listener_name')

    return LaunchDescription([
        freq_arg,
        threshold_arg,
        topic_arg,
        logging_arg,
        listener_name_arg,

        Node(
            package='frog_pkg',
            executable='even_number_publisher',
            name='even_pub',
            parameters=[
                {'publish_frequency': frequency},
                {'overflow_threshold': threshold},
                {'topic_name': topic_name},
                {'enable_logging': enable_logging},
            ],
            output='screen',
        ),

        Node(
            package='frog_pkg',
            executable='overflow_listener',
            name=listener_name,
            output='screen',
        ),
    ])