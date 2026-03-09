---
name: ros2-create-launch
description: Generate a Python launch file for one or more ROS2 nodes with parameters, remappings, and namespaces. Usage: /ros2-create-launch <launch_name> [node:pkg ...] [--param key:value] [--ns namespace]
argument-hint: <launch_name> [node_name:package ...] [--param key:value] [--ns namespace] [--yaml config.yaml]
allowed-tools: Read, Write, Edit, Glob, Bash
---

# ROS2 Launch File Generator

Generate a Python launch file. Arguments: `$ARGUMENTS`

Parse arguments:
- **launch_name**: first argument (snake_case, without `.launch.py` suffix)
- **node:pkg pairs**: `node_name:package_name` entries — can repeat
- **--param key:value**: launch argument with default value
- **--ns namespace**: wrap all nodes in a namespace
- **--yaml path**: load parameters from a YAML file
- **--remap from:to**: add a topic remapping

If no nodes are given, generate a skeleton with comments showing how to add nodes.

## Steps

1. **Locate the package** — find `package.xml` in current directory or parent. If not found, create launch file in current directory.

2. **Create `launch/` directory** if it doesn't exist.

3. **Generate `launch/<launch_name>.launch.py`** following this idiomatic structure:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare
# add other imports as needed

def generate_launch_description():
    # --- Launch Arguments ---
    # (one DeclareLaunchArgument per --param)

    # --- Nodes ---
    # (one Node() per node:pkg pair)

    return LaunchDescription([
        # arguments first, then nodes
    ])
```

4. **For each node:pkg pair**, generate a `Node()` action:
```python
Node(
    package='<pkg>',
    executable='<node>',
    name='<node>',          # explicit name
    namespace=LaunchConfiguration('namespace') if --ns given,
    output='screen',
    parameters=[{
        # inline params or yaml file
    }],
    remappings=[
        ('/from', '/to'),   # per --remap
    ],
)
```

5. **For YAML parameter files**, use:
```python
params_file = PathJoinSubstitution([
    FindPackageShare('<pkg>'), 'config', '<launch_name>.yaml'
])
# then pass params_file to parameters=[params_file]
```
Also create a skeleton `config/<launch_name>.yaml` if it doesn't exist.

6. **For namespaces**, use `GroupAction` with `PushRosNamespace`:
```python
GroupAction([
    PushRosNamespace(LaunchConfiguration('namespace')),
    node1,
    node2,
])
```

7. **Update `CMakeLists.txt` or `setup.py`** to install the launch directory:

   **CMake:**
   ```cmake
   install(DIRECTORY launch config
     DESTINATION share/${PROJECT_NAME}
   )
   ```
   **Python (setup.py):**
   ```python
   data_files=[
       ...
       ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
       ('share/' + package_name + '/config', glob('config/*.yaml')),
   ],
   ```

8. Print usage:
   ```bash
   ros2 launch <pkg> <launch_name>.launch.py
   ros2 launch <pkg> <launch_name>.launch.py param_name:=value
   ```
