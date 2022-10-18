# decawave_ros

This is a ROS python package for interfacing with the DecaWave EVB1000 modules. This package includes a python package that can parse the EVB1000 serial messages and a basic script to evaluate the module. Currently, the node only publishes the received distance measurements from the anchors/tags. Future work will include incorportating localization filter nodes.  

## Quickstart

Clone the package to your catkin workspace<br>
`git clone https://github.com/unmannedlab/decawave_ros.git`

Use catkin to build the packages<br>
`catkin build decawave_ros`

Start the ROS core service<br>
`roscore`

Launch the publisher<br>
`roslaunch decawave_ros decawave_publisher.launch`

