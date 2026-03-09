---
name: ros2-workspace
description: Scaffold a new ROS2 workspace — create the directory structure, git init, .colcon/defaults.yaml, and optional colcon.meta. Usage: /ros2-workspace <workspace_name> [--path dir] [--no-git] [--vcs-file repos.yaml]
argument-hint: <workspace_name> [--path dir] [--no-git] [--vcs-file repos.yaml]
allowed-tools: Bash, Write, Glob
---

# ROS2 Workspace Scaffolder

Create a new ROS2 workspace with correct structure and configuration. Arguments: `$ARGUMENTS`

Parse arguments:
- **workspace_name**: first argument — directory name (e.g. `my_robot_ws`)
- **--path dir**: parent directory to create the workspace in (default: current directory)
- **--no-git**: skip `git init`
- **--vcs-file repos.yaml**: also generate a `repos.yaml` for `vcs import`

Current ROS2 environment: !`echo ${ROS_DISTRO:-"(not sourced)"}`

## Steps

1. **Validate the workspace name** — must be a valid directory name, conventionally ends in `_ws`.
   If name doesn't end in `_ws`, warn but continue: `NOTE: ROS2 workspaces are conventionally named <name>_ws`

2. **Check the target path doesn't already exist**:
   ```bash
   ls <path>/<workspace_name> 2>/dev/null
   ```
   If it exists, stop and warn.

3. **Create the directory structure**:
   ```bash
   mkdir -p <workspace_name>/src
   mkdir -p <workspace_name>/.colcon
   ```

4. **Write `.colcon/defaults.yaml`** — sensible colcon defaults:
   ```yaml
   # colcon defaults for <workspace_name>
   # Applies to all colcon commands run from this workspace root
   build:
     symlink-install: true       # faster iteration — no need to rebuild for Python changes
     event-handlers:
       - console_cohesion+        # group output per package
   test:
     event-handlers:
       - console_cohesion+
   ```

5. **Write `colcon.meta`** at the workspace root:
   ```json
   {
     "names": {
       "<workspace_name>": {
         "cmake-args": [
           "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
           "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
         ]
       }
     }
   }
   ```

6. **Write `.gitignore`** at the workspace root:
   ```
   # ROS2 colcon build artifacts
   build/
   install/
   log/

   # Python
   __pycache__/
   *.pyc
   *.egg-info/

   # IDE
   .vscode/
   .idea/
   *.swp

   # OS
   .DS_Store
   ```

7. **Write `README.md`** with basic workspace instructions:
   ```markdown
   # <workspace_name>

   ROS2 workspace for <workspace_name>.
   Distro: <ROS_DISTRO>

   ## Setup

   ```bash
   # Install dependencies
   rosdep install --from-paths src --ignore-src -r -y

   # Build
   colcon build --symlink-install

   # Source
   source install/setup.bash
   ```

   ## Adding packages

   ```bash
   cd src/
   ros2 pkg create my_package --build-type ament_cmake
   ```
   ```

8. **If --vcs-file given**, write `<vcs-file>`:
   ```yaml
   repositories:
     # Add your repositories here
     # Example:
     # my_package:
     #   type: git
     #   url: https://github.com/my_org/my_package.git
     #   version: main
   ```
   And show the import command:
   ```bash
   vcs import src < repos.yaml
   ```

9. **If not --no-git**, initialize git:
   ```bash
   cd <workspace_name> && git init && git add . && git commit -m "Initial workspace scaffold"
   ```

10. **Print summary and next steps**:
    ```
    ✅ Workspace created: <workspace_name>/

    Structure:
      <workspace_name>/
      ├── src/              ← put your packages here
      ├── .colcon/
      │   └── defaults.yaml ← symlink-install enabled by default
      ├── colcon.meta       ← RelWithDebInfo + compile_commands.json
      ├── .gitignore
      └── README.md

    Next steps:
      cd <workspace_name>
      source /opt/ros/<distro>/setup.bash

      # Create a package
      /ros2-create-pkg my_package cmake

      # Or clone existing packages into src/
      git clone <url> src/<package>

      # Install dependencies
      /ros2-rosdep

      # Build
      /ros2-build
    ```
