from setuptools import find_packages, setup

package_name = 'Linear_motor_ctrl'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='waffle',
    maintainer_email='dl1wjd2@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'linear_motor_node = Linear_motor_ctrl.linear_motor_node:main',
            'linear_motor_teleop = Linear_motor_ctrl.linear_motor_teleop:main',
        ],
    },
)
