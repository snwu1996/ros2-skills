---
name: ros2-remap
description: Generate ROS2 topic/service remapping syntax for CLI and launch files. Find all uses of a topic across nodes and launch files, and produce correct remapping arguments. Usage: /ros2-remap <from_topic> <to_topic> [node] [--launch file] [--find]
argument-hint: <from_topic> <to_topic> [node_name] [--launch file.launch.py] [--find]
allowed-tools: Bash, Read, Grep, Glob
---

# ROS2 Topic Remapper

Generate remapping syntax and find all uses of a topic across your workspace. Arguments: `$ARGUMENTS`

Parse arguments:
- **from_topic**: source topic name (e.g. `/camera/image_raw`)
- **to_topic**: target topic name (e.g. `/robot/camera/image`)
- **node**: optional — node name to scope the remap to (e.g. `/image_processor`)
- **--launch file**: generate the remap inside this specific launch file
- **--find**: search the workspace for all uses of `from_topic` in source and launch files
- If only one topic given, default to `--find` mode

## Steps

1. **Normalize topic names** — ensure both have leading `/`.

2. **If --find mode**, search the workspace for uses of the topic:

   In Python and C++ source files:
   ```bash
   grep -r "from_topic\|<from_topic_stripped>" src/ --include="*.py" --include="*.cpp" --include="*.hpp" -l
   ```
   For each match file, show the line and context.

   In launch files:
   ```bash
   grep -r "from_topic" . --include="*.launch.py" --include="*.launch.xml" --include="*.launch" -n
   ```

   In parameter YAML files:
   ```bash
   grep -r "from_topic" . --include="*.yaml" --include="*.yml" -n
   ```

   Display all findings:
   ```
   Uses of '/camera/image_raw' found in:
   ──────────────────────────────────────────────────────
   src/image_processor/src/processor.cpp:42
     this->create_subscription<Image>("/camera/image_raw", ...)

   src/display/src/viewer.cpp:18
     this->create_subscription<Image>("/camera/image_raw", ...)

   launch/bringup.launch.py:34
     remappings=[('/camera/image_raw', '/robot/camera')]

   config/processor_params.yaml
     (no direct reference found)
   ──────────────────────────────────────────────────────
   3 files reference this topic
   ```

3. **Generate remapping syntax** in all formats:

   **CLI / ros2 run:**
   ```bash
   ros2 run <pkg> <exe> --ros-args -r /camera/image_raw:=/robot/camera/image
   ```
   Node-scoped:
   ```bash
   ros2 run <pkg> <exe> --ros-args -r /image_processor:/camera/image_raw:=/robot/camera/image
   ```

   **Python launch file:**
   ```python
   from launch_ros.actions import Node

   Node(
       package='my_pkg',
       executable='image_processor',
       remappings=[
           ('/camera/image_raw', '/robot/camera/image'),
       ],
   )
   ```

   **XML launch file:**
   ```xml
   <node pkg="my_pkg" exec="image_processor">
     <remap from="/camera/image_raw" to="/robot/camera/image"/>
   </node>
   ```

   **YAML parameter file** (for composable nodes):
   ```yaml
   /image_processor:
     ros__parameters:
       {}  # params here
     remappings:
       /camera/image_raw: /robot/camera/image
   ```

4. **If --launch flag given**, open that launch file and insert the remapping**:

   Read the file, find the relevant `Node(...)` block for the given node name, and add the remapping to the `remappings=[...]` list. If no `remappings` key exists, add it. Write the updated file.

   Report the change:
   ```
   ✅ Updated launch/bringup.launch.py
      Added remap to Node(executable='image_processor'):
        ('/camera/image_raw', '/robot/camera/image')
   ```

5. **Warn about common remapping pitfalls**:
   - Remaps use exact string matching — partial topic names don't work
   - Relative vs absolute: `/camera/image_raw` (absolute) vs `image_raw` (relative to node namespace)
   - Node namespace interacts with remapping: if node has namespace `/robot`, then `image_raw` resolves to `/robot/image_raw`
   - Remap takes effect at node startup — runtime remapping is not supported in ROS2

6. **If a running node is specified**, check the live remap:
   ```bash
   ros2 node info <node>
   ```
   Show currently active remappings for that node.

7. **Summary**:
   ```
   Remap:  /camera/image_raw  →  /robot/camera/image

   Syntax generated for:
     ✅ ros2 run (CLI)
     ✅ Python launch file
     ✅ XML launch file

   Found 3 existing uses of /camera/image_raw in workspace.
   Remember to update or remap all consumers if changing the topic name.
   ```
