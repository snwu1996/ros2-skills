---
name: ros2-add-dep
description: Add a ROS2 dependency to package.xml and the appropriate build file (CMakeLists.txt or setup.py). Usage: /ros2-add-dep <dependency> [package_path]
argument-hint: <dependency> [package_path]
allowed-tools: Read, Edit, Glob, Bash, Grep
---

# Add ROS2 Dependency

Add a dependency to a ROS2 package. Arguments: `$ARGUMENTS`

Parse arguments:
- **dependency**: first argument (e.g., `rclcpp`, `sensor_msgs`, `nav2_msgs`)
- **package_path**: second argument (optional — default to current directory or auto-detect)

## Steps

1. **Locate the package** — if no path given, look for `package.xml` in the current directory or immediate subdirectories.

2. **Read `package.xml`** to determine:
   - Package name
   - Build type: `ament_cmake` or `ament_python`
   - Existing dependencies (check for duplicates before adding)

3. **Classify the dependency** to determine the correct XML tag:

   | Dependency type | XML tag | When to use |
   |---|---|---|
   | Build-time only (headers, codegen) | `<build_depend>` | C++ headers used only at compile time |
   | Runtime only | `<exec_depend>` | Python imports, runtime libs |
   | Both build and runtime | `<depend>` | Most ROS2 msg/srv packages, rclcpp, rclpy |
   | Test only | `<test_depend>` | gtest, pytest, ament_lint |

   For common packages, use these defaults:
   - `rclcpp`, `rclpy`, `std_msgs`, `sensor_msgs`, `geometry_msgs`, `nav_msgs`, `*_msgs`, `*_interfaces` → `<depend>`
   - `ament_lint_auto`, `ament_lint_common`, `ament_cmake_gtest`, `pytest` → `<test_depend>`
   - `rosidl_default_generators` → `<build_depend>` + `<member_of_group>rosidl_interface_packages</member_of_group>`

4. **Add to `package.xml`** — insert the tag in the correct section (after existing `<depend>` tags, before `<test_depend>` tags). Preserve formatting.

5. **Update the build file**:

   **For CMake (`CMakeLists.txt`)**:
   - Add `find_package(<dep> REQUIRED)` after the existing `find_package` block
   - If target exists, add to `ament_target_dependencies(<target> <dep>)`
   - If it's a message/interface package, also ensure `rosidl_get_typesupport_target` or `ament_target_dependencies` pattern is correct

   **For Python (`setup.py`)**:
   - No CMakeLists changes needed for pure Python
   - Remind user that ROS2 Python packages find deps via `package.xml` at runtime

6. **Check if the dependency is installed** — run `ros2 pkg list | grep <dep>` or `dpkg -l | grep <dep>`. If not found, suggest the install command:
   ```bash
   sudo apt install ros-$ROS_DISTRO-<dep-with-dashes>
   # or
   rosdep install --from-paths src --ignore-src -r -y
   ```

7. Print a summary of all changes made.
