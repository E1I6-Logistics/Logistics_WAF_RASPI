import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # 1. turtlebot3_bringup 패키지의 robot.launch.py 경로 취득
    tb3_bringup_dir = get_package_share_directory('turtlebot3_bringup')
    tb3_robot_launch = os.path.join(tb3_bringup_dir, 'launch', 'robot.launch.py')

    # 2. 터틀봇3 하드웨어(OpenCR + 라이다 + 로봇 상태 퍼블리셔) 브링업 포함
    tb3_bringup_action = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(tb3_robot_launch)
    )

    # 3. 리니어 모터 제어 노드 정의
    linear_motor_node = Node(
        package='Linear_motor_ctrl',
        executable='linear_motor_node',
        name='linear_motor_node',
        output='screen',
        emulate_tty=True
    )

    return LaunchDescription([
        tb3_bringup_action,
        linear_motor_node,
    ])
