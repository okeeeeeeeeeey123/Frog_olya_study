import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/olya/ros2_ws/src/frog_pkg/install/frog_pkg'
