from setuptools import find_packages
from setuptools import setup

setup(
    name='play_motion2_msgs',
    version='1.3.0',
    packages=find_packages(
        include=('play_motion2_msgs', 'play_motion2_msgs.*')),
)
