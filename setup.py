# WARNING: SETUP.PY MODIFIED FOR USE WITH CATKIN BUILD
# DO NOT RUN PYTHON SETUP.PY INSTALL ON THIS FILE

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

def readme():
    with open('README.md') as f:
        return f.read()

setup_args = generate_distutils_setup(
    name='decawave_ros',
    version='0.1.0',
    description='A ROS package for interfacing with the Decawave TREK1000 UWB modules',
    long_description=readme(),
    url='https://github.com/unmannedlab/decawave_ros.git',
    author='Jacob Hartzer',
    author_email='JacobHartzer@gmail.com',
    license='MIT',
    packages='decawave_ros',
    package_dir={'' : 'src'},
    )

setup(**setup_args)