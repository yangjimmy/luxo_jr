from setuptools import find_packages
from setuptools import setup

setup(
    name='realsense2_camera',
    version='4.56.4',
    packages=find_packages(
        include=('realsense2_camera', 'realsense2_camera.*')),
)
