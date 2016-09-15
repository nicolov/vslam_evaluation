cmake_minimum_required(VERSION 2.8.3)
project(vslam_evaluation)

find_package(catkin REQUIRED COMPONENTS
  nav_msgs
  rospy
  sensor_msgs
  std_msgs
  trajectory_toolkit
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES vslam_competition
#  CATKIN_DEPENDS nav_msgs rospy sensor_msgs std_msgs trajectory_toolkit
#  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
