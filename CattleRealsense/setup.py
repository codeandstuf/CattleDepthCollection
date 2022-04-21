from setuptools import find_packages, setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='CattleRealsense',
    packages=find_packages(include=['CattleRealsense']),
    version='0.1.7',
    description='Takes depth video or pictures from birds eye view. Intended for use with cattle',
    author='Robert Kadlec',
    install_requires=[],
    setup_requires=['pytest-runner', 'datetime',
                 'opencv-python', 'numpy', 'imutils', 'pynput', 'tk', 'keyboard', 'pyrealsense2'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)


