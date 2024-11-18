from setuptools import find_packages
from setuptools import setup

setup(
    name='tiago_gazebo',
    version='4.2.0',
    packages=find_packages(
        include=('tiago_gazebo', 'tiago_gazebo.*')),
)
