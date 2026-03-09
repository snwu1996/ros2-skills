---
name: ros2-compose
description: Create a ROS2 composable node component — add RCLCPP_COMPONENTS_REGISTER_NODE, update CMakeLists.txt, and generate a component container launch file. Usage: /ros2-compose <node_class> [package_path] [--container-name name]
argument-hint: <ClassName> [package_path] [--container-name name]
allowed-tools: Read, Edit, Write, Glob, Bash
---

# ROS2 Composable Node Setup

Register a C++ node class as a composable ROS2 component and generate the container launch file. Arguments: `$ARGUMENTS`

Parse arguments:
- **node_class**: first argument — fully qualified class name (e.g. `my_pkg::ImageProcessor` or just `ImageProcessor`)
- **package_path**: second argument — path to the package root (default: current directory)
- **--container-name name**: name for the component container (default: `<snake_case_class>_container`)

## What composable nodes are

Composable nodes (components) run inside a shared process (`ComponentManager` container) and communicate via intra-process communication — zero-copy for large messages like images and pointclouds. This avoids the overhead of separate processes and DDS serialization.

## Steps

1. **Detect the package** — find `package.xml` and `CMakeLists.txt`:
   ```bash
   find . -name package.xml -maxdepth 3
   ```
   Extract the package name from `package.xml`.

2. **Find the node's source file** — search for the class definition:
   ```bash
   grep -r "class <ClassName>" src/ include/
   ```
   Identify the `.cpp` file that implements the class.

3. **Read the CMakeLists.txt** and identify the existing library or executable target for this node.

4. **Check if already a component** — look for `RCLCPP_COMPONENTS_REGISTER_NODE`:
   ```bash
   grep -r "RCLCPP_COMPONENTS_REGISTER_NODE" src/
   ```
   If already registered, report it and stop.

5. **Add the registration macro** to the node's `.cpp` file at the bottom:
   ```cpp
   #include "rclcpp_components/register_node_macro.hpp"
   RCLCPP_COMPONENTS_REGISTER_NODE(<FullyQualifiedClassName>)
   ```
   Ensure the constructor accepts `const rclcpp::NodeOptions &` — check and warn if it doesn't.

6. **Update CMakeLists.txt** — change from `add_executable` to `add_library` (SHARED) and add component registration:

   **Before:**
   ```cmake
   add_executable(image_processor src/image_processor.cpp)
   ament_target_dependencies(image_processor rclcpp sensor_msgs)
   install(TARGETS image_processor DESTINATION lib/${PROJECT_NAME})
   ```

   **After:**
   ```cmake
   # Component library
   add_library(image_processor_component SHARED src/image_processor.cpp)
   ament_target_dependencies(image_processor_component rclcpp sensor_msgs)
   rclcpp_components_register_node(
     image_processor_component
     PLUGIN "<package>::<ClassName>"
     EXECUTABLE image_processor
   )
   install(TARGETS image_processor_component
     ARCHIVE DESTINATION lib
     LIBRARY DESTINATION lib
     RUNTIME DESTINATION bin
   )
   ```

7. **Add `rclcpp_components` dependency** to CMakeLists.txt:
   ```cmake
   find_package(rclcpp_components REQUIRED)
   ```
   And to `package.xml`:
   ```xml
   <depend>rclcpp_components</depend>
   ```

8. **Generate the component container launch file**:

   File: `launch/<container_name>.launch.py`
   ```python
   from launch import LaunchDescription
   from launch_ros.actions import ComposableNodeContainer
   from launch_ros.descriptions import ComposableNode


   def generate_launch_description():
       container = ComposableNodeContainer(
           name='<container_name>',
           namespace='',
           package='rclcpp_components',
           executable='component_container',
           composable_node_descriptions=[
               ComposableNode(
                   package='<package_name>',
                   plugin='<package>::<ClassName>',
                   name='<snake_case_node_name>',
                   parameters=[{
                       # Add parameters here
                   }],
                   remappings=[
                       # ('/input_topic', '/actual_topic'),
                   ],
               ),
           ],
           output='screen',
       )
       return LaunchDescription([container])
   ```

9. **Show summary**:
   ```
   ✅ Composable node setup complete

   Changes made:
     src/image_processor.cpp  — added RCLCPP_COMPONENTS_REGISTER_NODE
     CMakeLists.txt           — converted to shared library + registered component
     package.xml              — added rclcpp_components dependency
     launch/image_processor_container.launch.py  — new container launch file

   Build and run:
     colcon build --packages-select <package>
     ros2 launch <package> image_processor_container.launch.py

   Add more components at runtime:
     ros2 component load /image_processor_container <package> <package>::<ClassName>

   List loaded components:
     ros2 component list
   ```
