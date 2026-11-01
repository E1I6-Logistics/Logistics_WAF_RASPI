import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'waffle'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name] if os.path.exists('resource/' + package_name) else []),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='waffle',
    maintainer_email='dl1wjd2@gmail.com',
    description='Bringup and integration launch package for Waffle robot',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
        ],
    },
)
