---
name: ros2-gazebo
description: Launch a Gazebo simulation with a world file and optionally spawn a robot from URDF/Xacro. Supports Gazebo Classic (gazebo) and Gazebo Harmonic/Ignition (gz sim). Usage: /ros2-gazebo [world_file] [--urdf robot.urdf] [--spawn-at x y z] [--gz] [--headless]
argument-hint: [world_file] [--urdf file.urdf|file.xacro] [--spawn-at x y z] [--gz] [--headless] [--paused]
allowed-tools: Bash, Read, Write, Glob
---

# ROS2 Gazebo Launcher

Launch a Gazebo simulation and optionally spawn a robot. Arguments: `$ARGUMENTS`

Parse arguments:
- **world_file**: path to `.world` or `.sdf` file (optional — use empty world if not given)
- **--urdf file**: URDF or Xacro file to spawn as the robot model
- **--spawn-at x y z**: spawn position (default: `0 0 0`)
- **--gz**: use modern Gazebo (Harmonic/Ignition, `gz sim`) instead of Gazebo Classic (`gazebo`)
- **--headless**: run without GUI (server only)
- **--paused**: start simulation paused

Current ROS2 environment: !`echo ${ROS_DISTRO:-"(not sourced)"}`

## Steps

1. **Detect which Gazebo is available**:
   ```bash
   which gazebo 2>/dev/null && gazebo --version 2>/dev/null | head -1
   which gz 2>/dev/null && gz sim --version 2>/dev/null | head -1
   ```
   If `--gz` flag given, require `gz`. If neither is found, stop and show install instructions.

   **ROS2 distro → default Gazebo:**
   | ROS2 Distro | Default Gazebo |
   |---|---|
   | Humble | Gazebo Classic 11 |
   | Iron | Gazebo Harmonic (gz sim) |
   | Jazzy | Gazebo Harmonic (gz sim) |

2. **Find the world file** — if given, verify it exists:
   ```bash
   ls <world_file> 2>/dev/null
   ```
   If not found, search for `.world` and `.sdf` files:
   ```bash
   find . -name "*.world" -o -name "*.sdf" | head -10
   ```
   Also check common ROS2 world locations:
   ```bash
   find /opt/ros/$ROS_DISTRO -name "*.world" 2>/dev/null | head -5
   ```
   If no world given, use empty world.

3. **If --urdf given**, process the robot model:
   - If `.xacro`, expand first:
     ```bash
     ros2 run xacro xacro <file.xacro> -o /tmp/robot_spawner.urdf
     ```
   - Verify the URDF is valid:
     ```bash
     check_urdf /tmp/robot_spawner.urdf 2>/dev/null || echo "check_urdf not available"
     ```

4. **Build the launch commands**:

   **Gazebo Classic:**
   ```bash
   # Start Gazebo
   source /opt/ros/$ROS_DISTRO/setup.bash
   ros2 launch gazebo_ros gazebo.launch.py world:=<world_file> [--headless] [--paused]

   # Spawn robot (separate step)
   ros2 run gazebo_ros spawn_entity.py \
     -file /tmp/robot_spawner.urdf \
     -entity robot \
     -x <x> -y <y> -z <z>
   ```

   **Modern Gazebo (gz sim):**
   ```bash
   # Start Gazebo
   gz sim <world_file> [--headless-rendering] [-r]

   # Spawn via ros_gz_sim
   ros2 run ros_gz_sim create \
     -file /tmp/robot_spawner.urdf \
     -name robot \
     -x <x> -y <y> -z <z>
   ```

5. **Launch Gazebo in background**:
   ```bash
   ros2 launch gazebo_ros gazebo.launch.py world:=<world_file> > /tmp/gazebo_output.txt 2>&1 &
   GAZEBO_PID=$!
   echo "Gazebo PID: $GAZEBO_PID"
   ```

6. **Wait for Gazebo to be ready** — poll for the `/gazebo` or `/world` topics:
   ```bash
   for i in $(seq 1 15); do
     ros2 topic list 2>/dev/null | grep -q "gazebo\|world\|clock" && break
     sleep 1
   done
   ```
   If not ready after 15s, check the output log for errors.

7. **Spawn the robot** (if --urdf given):
   ```bash
   ros2 run gazebo_ros spawn_entity.py -file /tmp/robot_spawner.urdf -entity robot -x <x> -y <y> -z <z>
   ```
   Verify spawn succeeded:
   ```bash
   ros2 topic list | grep "robot"
   ```

8. **Check for essential topics** after spawn:
   ```bash
   ros2 topic list
   ```
   Expect to see:
   - `/clock` — simulation time
   - `/joint_states` — if robot has joints
   - `/tf` — if robot_state_publisher is running
   - `/scan` or `/camera/image_raw` — if sensors configured

9. **Report status**:
   ```
   ✅ Gazebo launched successfully

   Simulator: Gazebo Classic 11
   World:     /path/to/world.world
   PID:       12345
   Log:       /tmp/gazebo_output.txt

   Robot spawned: robot  at (0.0, 0.0, 0.0)

   Active topics:
     /clock                         rosgraph_msgs/msg/Clock
     /joint_states                  sensor_msgs/msg/JointState
     /scan                          sensor_msgs/msg/LaserScan
     /tf                            tf2_msgs/msg/TFMessage

   To inspect:  /ros2-node-graph
   To check TF: /ros2-check-tf --tree
   To monitor:  /ros2-sub /scan 5

   To stop Gazebo: kill 12345
   ```

10. **Common issues and fixes**:

    | Error | Fix |
    |---|---|
    | `[Err] No namespace found` | Check robot URDF has valid `<robot name>` |
    | Gazebo opens but robot invisible | Check mesh paths: `/ros2-urdf-check --meshes` |
    | `/tf` empty after spawn | Start `robot_state_publisher` with the URDF |
    | `gzserver: symbol lookup error` | Source ROS2 setup before running: `. /opt/ros/$ROS_DISTRO/setup.bash` |
    | Sim time not propagating | Set `use_sim_time:=true` on nodes: `/ros2-sim-time --enable` |
