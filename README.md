## Overview

This ROS package is an adaptation of the pure python3 module written by <a href="https://github.com/dalymople">dalymople.</a> 
The package provides a simple a easy way to incorporate UBX modules such as the M8U or F9P in ROS projects. 
The package has no python dependencies thanks to the work by dalymople and only depends on std_mgs and geometry_msgs in ROS.  
The package can be reconfigured to new modules that have different message types.


## Quickstart

Clone the package to your catkin workspace<br>
`git clone https://github.com/unmannedlab/ubxtranslator.git`

Use catkin to build the packages<br>
`catkin build ubxtranslator`

Start the ROS core service<br>
`roscore`

Launch the publisher<br>
`roslaunch ubxtranslator ubx_publisher`