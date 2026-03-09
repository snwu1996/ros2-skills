---
name: ros2-launch
description: Run a ROS2 launch file from a package or a direct file path. Streams output, detects startup errors, and reports which nodes came up. Usage: /ros2-launch <package> <launch_file> [arg:=value ...] | /ros2-launch <path/to/file.launch.py> [arg:=value ...]
argument-hint: <package> <launch_file.launch.py> [arg:=value ...] | <path/to/file.launch.py> [arg:=value ...]
allowed-tools: Bash, Glob
---

# ROS2 Launch

Run a ROS2 launch file. Arguments: `$ARGUMENTS`

Parse arguments:
- **Two-argument form**: `<package> <launch_file>` — launch via installed package
- **One-argument form**: `<path>` — launch a file directly by path (must end in `.launch.py`, `.launch.xml`, or `.launch`)
- **arg:=value pairs**: any remaining `key:=value` tokens are passed as launch arguments
- **--timeout sec**: wait this many seconds for nodes to come up before reporting (default: `5`)
- **--dry-run**: print the command that would be run without executing it

Current ROS2 environment: !`echo ${ROS_DISTRO:-"(not sourced)"}`

## Steps

1. **Determine launch mode** from the first argument(s):

   - If first argument contains `/` or ends in `.launch.py` / `.launch.xml` → **file mode**
   - If two non-flag arguments are given → **package mode**: `ros2 launch <pkg> <file>`
   - If only one argument with no `/` → try package mode with just that argument (may be a package with a default launch file)

2. **In file mode**, verify the file exists:
   ```bash
   ls <path>
   ```
   If not found, search the current directory:
   ```bash
   find . -name "*.launch.py" -o -name "*.launch.xml" | head -10
   ```
   Show matches and stop if ambiguous.

3. **In package mode**, verify the package and launch file exist:
   ```bash
   ros2 pkg list | grep <package>
   ros2 launch <package> --show-args 2>/dev/null || true
   ```
   If the package is not found, show similar package names:
   ```bash
   ros2 pkg list | grep -i <partial_name>
   ```

4. **Show the full command** that will be run:
   ```
   Running: ros2 launch <package> <launch_file> [args...]
   ```

5. **If --dry-run**, print the command and stop.

6. **Launch and stream output**:

   **File mode:**
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash && python3 <path>
   ```
   Wait — for `.launch.py` files run directly this won't work. Use:
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash && ros2 launch <path> [arg:=value ...]
   ```

   **Package mode:**
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash && ros2 launch <package> <launch_file> [arg:=value ...]
   ```

   Run in the **background** so Claude can continue:
   ```bash
   ros2 launch ... > /tmp/ros2_launch_output.txt 2>&1 &
   LAUNCH_PID=$!
   echo "Launch PID: $LAUNCH_PID"
   ```

7. **Wait for nodes to come up** — poll for `--timeout` seconds:
   ```bash
   sleep <timeout>
   ros2 node list
   ```

8. **Check for startup errors** in the launch output:
   ```bash
   grep -i "error\|exception\|failed\|traceback" /tmp/ros2_launch_output.txt | head -20
   ```

9. **Report the result**:

   **Success:**
   ```
   ✅ Launch successful

   Command: ros2 launch my_pkg bringup.launch.py use_sim_time:=false
   PID:     12345

   Nodes up (after 5s):
     /camera_driver
     /lidar_driver
     /robot_state_publisher

   Topics active:
     /camera/image_raw   (sensor_msgs/msg/Image)
     /scan               (sensor_msgs/msg/LaserScan)

   Logs: /tmp/ros2_launch_output.txt

   To stop:   kill 12345
   To inspect: /ros2-debug-node <node_name>
   To monitor: /ros2-node-graph
   ```

   **Startup errors detected:**
   ```
   ⚠  Launch started but errors detected:

   [camera_driver]: ModuleNotFoundError: No module named 'cv2'
   [lidar_driver]:  [ERROR] Failed to open /dev/ttyUSB0: Permission denied

   Nodes that came up:
     /robot_state_publisher  ✅

   Nodes that did NOT appear:
     /camera_driver  ❌
     /lidar_driver   ❌

   Suggested fixes:
     - cv2 missing: pip3 install opencv-python
     - Permission denied: sudo chmod a+rw /dev/ttyUSB0
                          or: sudo usermod -aG dialout $USER
   ```

10. **Common launch argument examples**:
    ```bash
    # Simulation time
    ros2 launch my_pkg bringup.launch.py use_sim_time:=true

    # Custom parameter file
    ros2 launch my_pkg bringup.launch.py params_file:=/path/to/params.yaml

    # Namespace
    ros2 launch my_pkg bringup.launch.py namespace:=/robot1

    # Direct file path
    ros2 launch /home/user/ros2_ws/src/my_pkg/launch/bringup.launch.py
    ```
