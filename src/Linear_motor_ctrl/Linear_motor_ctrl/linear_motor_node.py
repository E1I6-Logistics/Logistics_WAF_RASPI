from gpiozero import Motor
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class LinearMotorNode(Node):
    """L298N linear actuator control node."""

    def __init__(self):
        super().__init__('linear_motor_node')
        # ENA가 5V 상시 연결이므로 pwm=False로 불필요한 소프트웨어 PWM 스레드 방지
        self.motor = Motor(forward=14, backward=15, pwm=False)
        self.actions = {
            'UP': self.motor.forward,
            'DOWN': self.motor.backward,
            'STOP': self.motor.stop,
        }
        self.subscription = self.create_subscription(
            String,
            '/linear_actuator/cmd',
            self.cmd_callback,
            10
        )
        self.get_logger().info('linear_motor_node initialized (IN1=GPIO14, IN2=GPIO15).')

    def cmd_callback(self, msg: String):
        cmd = msg.data.strip().upper()
        action = self.actions.get(cmd)
        if action:
            action()
            self.get_logger().info(f'Command "{cmd}" executed.')
        else:
            self.get_logger().warn(f'Unknown command "{msg.data}": ignored.')

    def destroy_node(self):
        self.motor.stop()
        self.motor.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LinearMotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('KeyboardInterrupt detected: stopping motor.')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
