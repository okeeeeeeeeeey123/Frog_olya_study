#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Только черепашка и наш TF-бродкастер
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtle1',
            output='screen'
        ),
        Node(
            package='frog_pkg',
            executable='carrot_tf_broadcaster',
            name='carrot_broadcaster',
            output='screen'
        ),
    ])