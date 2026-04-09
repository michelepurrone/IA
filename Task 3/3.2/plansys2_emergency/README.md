COME ESEGUIRE

terminale 1:
cd plansys2_emergency
colcon build --symlink-install
source install/local_setup.bash
ros2 launch plansys2_emergency plansys2_emergency_launch.py

terminale 2:
cd plansys2_emergency
ros2 run plansys2_terminal plansys2_terminal
source commands.txt 