#!/bin/bash

./setup.bash
roscore &
rosrun rosbag_to_csv rosbag_to_csv.py --all -d /home/greg/Lab/MURI/UML-BYU-2023-Data/bags
killall -9 roscore
killall -9 rosmaster
python clean_topic_names.py /home/greg/Lab/MURI/UML-BYU-2023-Data/bags