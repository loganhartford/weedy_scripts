#!/bin/bash
/home/weedy/weedy_scripts/venv/bin/python3 /home/weedy/weedy_scripts/yellow.py

/usr/bin/docker start rossy7
sleep 5
/usr/bin/docker exec rossy7 bash -c "source /mnt/shared/weedy_ros/install/setup.bash && ros2 launch decisions launch.py"

