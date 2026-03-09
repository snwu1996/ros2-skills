---
name: ros2-rosdep
description: Run rosdep to install ROS2 package dependencies, fix common failures, update the database, and explain what each dependency is. Usage: /ros2-rosdep [package_path] [--update] [--fix] [--check-only]
argument-hint: [package_path] [--update] [--fix] [--check-only]
allowed-tools: Bash, Read, Glob
---

# ROS2 rosdep Helper

Install and manage ROS2 package dependencies using rosdep. Arguments: `$ARGUMENTS`

Parse arguments:
- **package_path**: path to workspace or package root (default: current directory)
- **--update**: run `rosdep update` first to refresh the database
- **--fix**: attempt to automatically fix common rosdep failures
- **--check-only**: dry run — show what would be installed without installing

## Steps

1. **Check rosdep is initialized**:
   ```bash
   rosdep db 2>&1 | head -3
   ```
   If not initialized (output contains "rosdep has not been initialized"):
   ```bash
   sudo rosdep init
   rosdep update
   ```
   Report the outcome.

2. **If --update flag**, refresh the rosdep database**:
   ```bash
   rosdep update
   ```
   Show the number of rules updated.

3. **Detect workspace structure** — find `src/` or individual `package.xml`:
   ```bash
   find . -name package.xml -maxdepth 4 | head -30
   ```
   Determine whether this is a workspace (has `src/`) or a single package.

4. **Run rosdep check** (dry run to find missing deps):
   ```bash
   rosdep check --from-paths src --ignore-src -r
   ```
   For a single package:
   ```bash
   rosdep check --from-paths . --ignore-src
   ```

5. **If --check-only**, display what would be installed and stop:
   ```
   Dependencies to install:
     python3-transforms3d     (apt)
     libopencv-dev            (apt)
     ros-humble-nav2-msgs     (apt)

   To install: /ros2-rosdep (without --check-only)
   ```

6. **Install dependencies**:
   ```bash
   rosdep install --from-paths src --ignore-src -r -y
   ```
   Or for a single package:
   ```bash
   rosdep install --from-paths . --ignore-src -y
   ```

7. **Parse rosdep output** — detect and categorize failures:

   Common failures and fixes:

   **a) Key not found:**
   ```
   ERROR: the following packages/stacks could not have their rosdep keys resolved
   to system dependencies: my_package: [python3-mylib]
   ```
   Fix: Check if the key exists in rosdep database:
   ```bash
   rosdep resolve python3-mylib
   ```
   If not found, suggest adding it to `rosdep/sources.list.d/` or installing manually.

   **b) OS version mismatch:**
   ```
   ERROR: cannot find a source for 'ros-humble-some-pkg' on ubuntu jammy
   ```
   Fix: verify the correct distro/OS:
   ```bash
   lsb_release -a
   echo $ROS_DISTRO
   ```
   Suggest: use the correct ROS2 repo for this Ubuntu version.

   **c) Permission error:**
   ```
   ERROR: could not install dependency: permission denied
   ```
   Fix suggestion: run with `sudo` or check `~/.ros/rosdep/` permissions.

   **d) Network error:**
   Fix: `rosdep update` to refresh, check internet connectivity.

8. **If --fix flag**, attempt automated fixes for detected issues**:
   - Missing rosdep key that maps to an apt package → try `sudo apt-get install -y <package>`
   - Stale database → run `rosdep update`
   - Unresolvable key that is a Python package → try `pip3 install <package>`

9. **List what was installed** — parse `apt-get install` output to show a clean list:
   ```
   ✅ Installed 7 dependencies:
     python3-transforms3d
     libopencv-dev
     ros-humble-nav2-msgs
     ros-humble-nav2-costmap-2d
     ros-humble-behaviortree-cpp-v3
     python3-numpy
     libeigen3-dev
   ```

10. **If already up to date**:
    ```
    ✅ All dependencies already satisfied — nothing to install.
    ```

11. **Summary and next steps**:
    ```
    rosdep complete for: src/ (5 packages)
    Installed: 7 new dependencies
    Skipped:   2 already installed

    Next steps:
      colcon build --symlink-install
      # or: /ros2-build
    ```
