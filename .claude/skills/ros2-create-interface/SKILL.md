---
name: ros2-create-interface
description: Create ROS2 .msg, .srv, or .action interface files with correct syntax and update CMakeLists.txt. Usage: /ros2-create-interface <name> [msg|srv|action] [field definitions...]
argument-hint: <InterfaceName> [msg|srv|action] [field:type ...]
allowed-tools: Read, Write, Edit, Glob, Bash
---

# ROS2 Interface Generator

Create a ROS2 message, service, or action interface. Arguments: `$ARGUMENTS`

Parse arguments:
- **name**: first argument — PascalCase interface name (e.g., `RobotStatus`, `MoveToGoal`)
- **type**: `msg`, `srv`, or `action` (default: `msg`)
- **fields**: remaining arguments as `field_name:FieldType` pairs (optional — generate reasonable skeleton if omitted)

## Interface Type Reference

### .msg format
```
# Comment
builtin_type field_name
package/MsgType field_name
builtin_type[] array_field
builtin_type[N] fixed_array_field
builtin_type field_with_default 42
```

### .srv format
```
# Request fields
TypeA field_a
---
# Response fields
TypeB field_b
bool success
string message
```

### .action format
```
# Goal
TypeA goal_field
---
# Result
bool success
string message
---
# Feedback
float32 progress
```

## Built-in types
`bool`, `byte`, `char`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `string`, `wstring`

Common ROS types: `std_msgs/Header`, `geometry_msgs/Pose`, `geometry_msgs/Twist`, `builtin_interfaces/Time`

## Steps

1. **Locate the package** — find `package.xml` in the current or parent directory. The package must use `ament_cmake` (interfaces cannot be pure Python packages).

2. **Create the interface directory** if it doesn't exist: `msg/`, `srv/`, or `action/`

3. **Write the interface file** `<type>/<Name>.<ext>` with:
   - A header comment documenting the interface purpose
   - Fields parsed from arguments, or a sensible skeleton with commented examples if no fields given
   - Proper ROS2 field syntax (snake_case names, PascalCase types)
   - Include `std_msgs/Header header` for messages that need timestamps/frame_id

4. **Update `CMakeLists.txt`** — add or extend the `rosidl_generate_interfaces` call:
   ```cmake
   find_package(rosidl_default_generators REQUIRED)
   find_package(std_msgs REQUIRED)  # add any needed msg deps

   rosidl_generate_interfaces(${PROJECT_NAME}
     "msg/MyMsg.msg"
     "srv/MySrv.srv"     # add the new interface here
     DEPENDENCIES std_msgs
   )
   ```

5. **Update `package.xml`** — ensure these are present:
   ```xml
   <build_depend>rosidl_default_generators</build_depend>
   <exec_depend>rosidl_default_runtime</exec_depend>
   <member_of_group>rosidl_interface_packages</member_of_group>
   ```

6. **Print usage example** showing how to import and use the new interface:

   **Python:**
   ```python
   from <pkg>.msg import <Name>       # for .msg
   from <pkg>.srv import <Name>       # for .srv
   from <pkg>.action import <Name>    # for .action
   ```

   **C++:**
   ```cpp
   #include "<pkg>/msg/<name>.hpp"
   #include "<pkg>/srv/<name>.hpp"
   #include "<pkg>/action/<name>.hpp"
   ```

7. Remind the user to rebuild: `colcon build --packages-select <pkg>`
