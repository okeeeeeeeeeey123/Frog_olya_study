
#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='frog_pkg',           # ← замени на своё имя пакета
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': 8.0},           # float
                {'overflow_threshold': 80},           # int
                {'topic_name': '/even_numbers_fast'}, # string
                {'enable_logging': True},             # bool
            
        ),
        Node(
            package='frog_pkg',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
        ),
    ])