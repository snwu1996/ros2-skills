---
name: ros2-run
description: Run a single ROS2 node standalone — by package+executable, or as a direct Python/C++ script. Passes ROS args, remappings, and parameters. Usage: /ros2-run <package> <executable> [--ros-args ...] [--remap from:=to] [--param k:=v] | /ros2-run <script.py> [--ros-args ...]
argument-hint: <package> <executable> [--remap from:=to] [--param k:=v] [--name node_name] [--ns namespace] | <script.py>
allowed-tools: Bash, Glob
---

# ROS2 Node Runner

Run a single ROS2 node standalone. Arguments: `$ARGUMENTS`

Parse arguments:
- **Two-argument form**: `<package> <executable>` — run via installed package (`ros2 run`)
- **One-argument form**: `<script.py>` or `<path>` ending in `.py` — run directly with Python
- **--name name**: override the node name (`__node:=name`)
- **--ns namespace**: set the node namespace (`__ns:=namespace`)
- **--remap from:=to**: add a topic/service remapping (repeatable)
- **--param key:=value**: set a parameter at startup (repeatable)
- **--params-file path**: load parameters from a YAML file
- **--background**: launch in background and return the PID (default: foreground with streamed output)

Current ROS2 environment: !`echo ${ROS_DISTRO:-"(not sourced)"}`

## Steps

1. **Determine run mode** from the first argument:
   - Ends in `.py` or contains `/` with a `.py` extension → **script mode**
   - Otherwise → **package mode**: two arguments required (`<package> <executable>`)

2. **In package mode**, verify the package and executable exist:
   ```bash
   ros2 pkg executables <package>
   ```
   If the package is not found:
   ```bash
   ros2 pkg list | grep -i <partial_name>
   ```
   Show close matches and stop. If the executable is not in the list, show all executables for that package and stop.

3. **In script mode**, verify the file exists:
   ```bash
   ls <script.py>
   ```
   If not found, search nearby:
   ```bash
   find . -name "$(basename <script.py>)" | head -5
   ```

4. **Build the full command**:

   **Package mode:**
   ```bash
   ros2 run <package> <executable> --ros-args \
     [-r __node:=<name>] \
     [-r __ns:=<namespace>] \
     [-r <from>:=<to> ...] \
     [-p <key>:=<value> ...] \
     [--params-file <path>]
   ```

   **Script mode:**
   ```bash
   python3 <script.py> --ros-args \
     [-r __node:=<name>] \
     [-r <from>:=<to> ...]
   ```

5. **Display the command** before running:
   ```
   Running: ros2 run my_pkg my_node --ros-args -r /input:=/robot/input -p speed:=0.5
   ```

6. **If --background**, run in background:
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash
   ros2 run <...> > /tmp/ros2_run_output.txt 2>&1 &
   echo $!
   ```
   Wait 3 seconds, then verify the node came up:
   ```bash
   sleep 3 && ros2 node list
   ```
   Report:
   ```
   ✅ Node started in background
   PID:      12345
   Node:     /my_node
   Log:      /tmp/ros2_run_output.txt

   To stop:    kill 12345
   To inspect: /ros2-debug-node /my_node
   ```

7. **If foreground (default)**, run and stream output:
   ```bash
   source /opt/ros/$ROS_DISTRO/setup.bash && ros2 run <...>
   ```
   Stream stdout/stderr directly. On exit, report the exit code.

8. **Detect and explain common startup errors**:

   | Error | Cause | Fix |
   |---|---|---|
   | `package '<pkg>' not found` | Not built or not sourced | `colcon build --packages-select <pkg>` then re-source |
   | `No executable found` | Wrong executable name | `ros2 pkg executables <pkg>` to list valid names |
   | `ModuleNotFoundError` | Missing Python dep | `pip3 install <module>` or `rosdep install` |
   | `error while loading shared libraries` | Missing C++ dep | `sudo ldconfig` or rebuild |
   | `Failed to find node` after background start | Node crashed immediately | Check `/tmp/ros2_run_output.txt` for traceback |

9. **Examples** — show these as suggestions after the command prints:
   ```bash
   # Run with a remapped topic
   ros2 run my_pkg my_node --ros-args -r /camera/image:=/robot/camera/image

   # Run with parameters
   ros2 run my_pkg my_node --ros-args -p speed:=0.5 -p debug:=true

   # Run from a params file
   ros2 run my_pkg my_node --ros-args --params-file config/my_node.yaml

   # Run a local Python script directly
   python3 demo/counter_node.py

   # Run with a custom node name and namespace
   ros2 run my_pkg my_node --ros-args -r __node:=robot1_node -r __ns:=/robot1
   ```
