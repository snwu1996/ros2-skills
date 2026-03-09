---
name: ros2-pkg-info
description: Inspect an installed ROS2 package — find its share directory, list executables, launch files, config files, and interfaces. Usage: /ros2-pkg-info <package_name> [--executables] [--launches] [--interfaces] [--path]
argument-hint: <package_name> [--executables] [--launches] [--interfaces] [--path]
allowed-tools: Bash, Glob
---

# ROS2 Package Inspector

Inspect an installed ROS2 package — find its files, executables, launch files, and interfaces. Arguments: `$ARGUMENTS`

Parse arguments:
- **package_name**: first argument — the package to inspect
- **--executables**: list all executable nodes in the package
- **--launches**: list all launch files
- **--interfaces**: list all msg/srv/action interfaces defined by this package
- **--path**: just print the share directory path
- If no flags given, show everything

## Steps

1. **Verify the package is installed**:
   ```bash
   ros2 pkg list | grep "^<package_name>$"
   ```
   If not found, show fuzzy matches:
   ```bash
   ros2 pkg list | grep -i <partial_name>
   ```
   Stop if not found.

2. **Get the package share directory**:
   ```bash
   ros2 pkg prefix <package_name>
   ros2 pkg prefix --share <package_name>
   ```
   Display the prefix and share paths clearly.

3. **If --path**, print the share dir and stop.

4. **List executables**:
   ```bash
   ros2 pkg executables <package_name>
   ```
   Display as a clean list with descriptions if available.

5. **List launch files**:
   ```bash
   SHARE=$(ros2 pkg prefix --share <package_name>)
   find $SHARE/launch -name "*.launch.py" -o -name "*.launch.xml" -o -name "*.launch" 2>/dev/null
   ```
   For each launch file, show its name and any `DeclareLaunchArgument` entries (grep for them):
   ```bash
   grep -h "DeclareLaunchArgument" $SHARE/launch/*.launch.py 2>/dev/null
   ```

6. **List config/parameter files**:
   ```bash
   find $SHARE/config -name "*.yaml" -o -name "*.yml" 2>/dev/null
   find $SHARE/params -name "*.yaml" 2>/dev/null
   ```

7. **List interfaces** (msg/srv/action):
   ```bash
   ros2 interface list | grep "^<package_name>/"
   ```
   Group by type:
   ```
   Messages (3):
     <package_name>/msg/Status
     <package_name>/msg/Command
     <package_name>/msg/Feedback

   Services (1):
     <package_name>/srv/SetMode

   Actions (1):
     <package_name>/action/Navigate
   ```
   For each interface, show its fields:
   ```bash
   ros2 interface show <package_name>/msg/Status
   ```

8. **List URDF/mesh assets**:
   ```bash
   find $SHARE/urdf -name "*.urdf" -o -name "*.xacro" 2>/dev/null
   find $SHARE/meshes -name "*.stl" -o -name "*.dae" -o -name "*.obj" 2>/dev/null | head -10
   ```

9. **Show ament index entries** for this package:
   ```bash
   ls $(ros2 pkg prefix <package_name>)/share/ament_index/resource_index/packages/ 2>/dev/null
   ```

10. **Full summary output**:
    ```
    Package: nav2_bringup
    ══════════════════════════════════════════════════════
    Prefix:  /opt/ros/jazzy
    Share:   /opt/ros/jazzy/share/nav2_bringup

    Executables (0):
      (none — this is a launch-only package)

    Launch files (6):
      bringup_launch.py        args: map, use_sim_time, params_file, ...
      navigation_launch.py     args: use_sim_time, params_file, ...
      localization_launch.py   args: map, use_sim_time, params_file, ...
      slam_launch.py           args: use_sim_time, slam_params_file, ...
      tb3_simulation_launch.py args: world, ...
      rviz_launch.py           args: rviz_config, ...

    Config files (3):
      nav2_params.yaml
      nav2_multirobot_params_1.yaml
      nav2_multirobot_params_2.yaml

    Interfaces:
      (defined in nav2_msgs — not this package)

    Usage:
      ros2 launch nav2_bringup bringup_launch.py map:=/path/to/map.yaml
    ```
