#!/usr/bin/env python3
import select
import sys
import termios
import tty

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

BANNER = """
---------------------------------------------
        Linear Actuator Teleop Controller
---------------------------------------------
  [Control Keys]
    w : UP   (상승)
    x / s : DOWN (하강)
    Space / k : STOP (정지)

  Ctrl + C : 모터 정지 및 프로그램 종료
---------------------------------------------
"""

KEY_BINDINGS = {
    'w': 'UP',
    'x': 'DOWN',
    's': 'DOWN',
    ' ': 'STOP',
    'k': 'STOP',
}


class LinearMotorTeleop(Node):
    """Linear actuator keyboard teleop node."""

    def __init__(self):
        super().__init__('linear_motor_teleop')
        self.publisher_ = self.create_publisher(String, '/linear_actuator/cmd', 10)
        self.msg = String()
        self.get_logger().info('Linear Motor Teleop Node 시작됨')

    def publish_cmd(self, command_str: str):
        self.msg.data = command_str
        self.publisher_.publish(self.msg)
        print(f'\r[명령 전송] -> {command_str:<6}', end='', flush=True)


def get_key(fd, settings):
    """터미널에서 Enter 입력 없이 단일 키 입력을 가져옵니다."""
    tty.setraw(fd)
    try:
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        return sys.stdin.read(1) if rlist else ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, settings)


def main(args=None):
    fd = sys.stdin.fileno()
    settings = termios.tcgetattr(fd)

    rclpy.init(args=args)
    teleop_node = LinearMotorTeleop()
    print(BANNER)

    try:
        while rclpy.ok():
            key = get_key(fd, settings)
            if key == '\x03':  # Ctrl + C
                break
            cmd = KEY_BINDINGS.get(key.lower())
            if cmd:
                teleop_node.publish_cmd(cmd)
    except Exception as e:
        print(f'\n오류 발생: {e}')
    finally:
        teleop_node.publish_cmd('STOP')
        print('\n\n종료 중: STOP 명령 전송 완료 및 터미널 설정 복구')
        termios.tcsetattr(fd, termios.TCSADRAIN, settings)
        teleop_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
