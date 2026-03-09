---
name: ros2-build
description: Build a ROS2 workspace with colcon, detect build errors, and suggest targeted fixes. Usage: /ros2-build [packages] [--symlink-install] [--cmake-args ...]
argument-hint: [package_name ...] [--symlink-install]
allowed-tools: Bash, Read, Glob, Grep
---

# ROS2 Workspace Build

Build the ROS2 workspace and diagnose any errors. Arguments: `$ARGUMENTS`

## Steps

1. **Locate the workspace root** — find the `src/` directory by walking up from the current directory. If not found, tell the user to run this from inside a colcon workspace.

2. **Change to the workspace root** and run:

```bash
colcon build $ARGUMENTS 2>&1
```

If `$ARGUMENTS` is empty, run a plain `colcon build --symlink-install` for faster iterative development.

Include `--event-handlers console_cohesion+` to get clean, readable output.

3. **Parse the build output** to identify:
   - Packages that **failed** (look for `Failed <<< <pkg>` lines)
   - **Error type** — CMake configure error, compile error, linker error, Python import error, missing dependency
   - **Exact error message** and **file:line** if available

4. **For each failed package**, diagnose the root cause:

   | Error pattern | Likely cause | Suggested fix |
   |---|---|---|
   | `Could not find package` | Missing `find_package` or not installed | Add dep to `package.xml` + install with `apt` or `rosdep` |
   | `undefined reference to` | Linker error | Add library to `target_link_libraries` in CMakeLists |
   | `No module named` | Python import missing | Add to `install_requires` in setup.py or install with pip |
   | `ament_target_dependencies` missing | Forgot to declare ament dep | Add `ament_target_dependencies(<target> <dep>)` |
   | `CMake Error at` | CMake logic error | Show the relevant CMakeLists.txt section |
   | Syntax/compile error | Code bug | Show the file and line with context |

5. **For rosdep issues**, suggest running:
   ```bash
   rosdep install --from-paths src --ignore-src -r -y
   ```

6. **If the build succeeds**, report which packages were built, remind the user to source:
   ```bash
   source install/setup.bash
   ```

7. Provide a prioritized, actionable fix list — most impactful issues first.
