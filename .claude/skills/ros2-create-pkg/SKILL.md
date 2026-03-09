---
name: ros2-create-pkg
description: Scaffold a new ROS2 package with proper structure, package.xml, and CMakeLists.txt or setup.py. Usage: /ros2-create-pkg <package_name> [cmake|python] [description]
argument-hint: <package_name> [cmake|python] [description]
allowed-tools: Read, Write, Bash, Glob
---

# ROS2 Package Scaffolding

Scaffold a complete ROS2 package based on the user's arguments: `$ARGUMENTS`

Parse the arguments:
- **Package name**: first argument (required, must be snake_case)
- **Build type**: second argument — `cmake` (default) or `python`
- **Description**: remaining arguments, or a sensible default

## Steps

1. Determine the package name, build type, and description from `$ARGUMENTS`. If no build type is given, default to `cmake`.

2. Validate the package name is valid (lowercase, underscores only, no leading digits).

3. Check if a directory with that name already exists in the current working directory. If so, warn the user and stop.

4. Create the package directory structure:

**For CMake packages:**
```
<pkg>/
├── package.xml
├── CMakeLists.txt
├── include/<pkg>/
├── src/
└── README.md
```

**For Python packages:**
```
<pkg>/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/<pkg>
├── <pkg>/
│   └── __init__.py
└── README.md
```

5. Write each file with correct, idiomatic ROS2 Humble/Iron/Jazzy content:

### package.xml (both types)
- Format 3
- Correct buildtool: `ament_cmake` or `ament_python`
- Include `<test_depend>ament_lint_auto</test_depend>` and `<test_depend>ament_lint_common</test_depend>`

### CMakeLists.txt (cmake only)
- `cmake_minimum_required(VERSION 3.8)`
- `find_package(ament_cmake REQUIRED)`
- Include install and test sections
- Proper `ament_package()` at the end

### setup.py (python only)
- Use `package_name` variable
- Include `entry_points` for console_scripts (with placeholder example)
- Data files for resource marker

### setup.cfg (python only)
```ini
[develop]
script_dir=$base/lib/<pkg>
[install]
install_scripts=$base/lib/<pkg>
```

6. After creating all files, print a summary of what was created and the next steps (e.g., `cd <pkg> && colcon build`).
