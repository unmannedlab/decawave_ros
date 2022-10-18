# WARNING: SETUP.PY MODIFIED FOR USE WITH CATKIN BUILD
# DO NOT RUN PYTHON SETUP.PY INSTALL ON THIS FILE

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

def readme():
    with open('README.md') as f:
        return f.read()

setup_args = generate_distutils_setup(
    packages=['decawave_ros'],
    package_dir={'' : 'src'},
    )

setup(**setup_args)