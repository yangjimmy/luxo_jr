from setuptools import find_packages, setup
import os

package_name = 'detection'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jimmy',
    maintainer_email='jimmyyang@ucla.edu',
    description='Hand detection module using YOLO',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'predict_node = detection.nodes.predict_node:main',
            'listen_node = detection.nodes.listen_node:main',
        ],
    },
)
