---
name: ros2-clean
description: Clean ROS2 workspace build artifacts — selectively wipe build/, install/, log/ per package or entirely. Usage: /ros2-clean [packages...] [--build] [--install] [--log] [--all] [--dry-run]
argument-hint: [package_name ...] [--build] [--install] [--log] [--all] [--dry-run]
allowed-tools: Bash, Glob
---

# ROS2 Workspace Cleaner

Remove colcon build artifacts from a ROS2 workspace. Arguments: `$ARGUMENTS`

Parse arguments:
- **packages**: optional list of package names — clean only those packages
- **--build**: clean only `build/` directory (or per-package subdirs)
- **--install**: clean only `install/` directory
- **--log**: clean only `log/` directory
- **--all**: clean build/, install/, and log/ entirely (default if no flag given)
- **--dry-run**: show what would be deleted without deleting anything

## Steps

1. **Detect workspace root** — look for `build/`, `install/`, `src/` in current or parent directories:
   ```bash
   ls build/ install/ src/ 2>/dev/null
   ```
   If not in a workspace, stop and warn. Show the current directory and suggest `cd` to the workspace root.

2. **Determine what to clean**:
   - If no `--build/--install/--log` flags → default to `--all`
   - If packages given → scope to those package subdirectories only

3. **Show disk usage before cleaning**:
   ```bash
   du -sh build/ install/ log/ 2>/dev/null
   ```
   Display:
   ```
   Current artifact sizes:
     build/    1.2 GB
     install/  340 MB
     log/       45 MB
   ```

4. **For full clean (`--all`, no packages specified)**:

   Try `colcon clean` first if available:
   ```bash
   colcon clean workspace --yes 2>/dev/null
   ```
   If not available, fall back to:
   ```bash
   rm -rf build/ install/ log/
   ```

5. **For per-package clean**, remove only the package subdirectories:
   ```bash
   # For each <package>:
   rm -rf build/<package>
   rm -rf install/<package>
   ```
   Log entries are not easily scoped — skip log or offer to clean all log.

6. **For selective directory clean** (`--build` only, etc.):
   ```bash
   rm -rf build/    # if --build
   rm -rf install/  # if --install
   rm -rf log/      # if --log
   ```

7. **If --dry-run**, print what would be removed:
   ```
   DRY RUN — nothing will be deleted

   Would remove:
     build/my_package/     (234 MB)
     install/my_package/   (89 MB)

   Re-run without --dry-run to proceed.
   ```

8. **After cleaning**, show freed space:
   ```bash
   du -sh build/ install/ log/ 2>/dev/null || echo "(directories removed)"
   ```

9. **Report and suggest next steps**:
   ```
   ✅ Clean complete

   Removed:
     build/     1.2 GB freed
     install/   340 MB freed
     log/        45 MB freed
   Total freed: ~1.6 GB

   Next steps:
     source /opt/ros/$ROS_DISTRO/setup.bash
     colcon build --symlink-install
     # or: /ros2-build
   ```

   If only specific packages were cleaned:
   ```
   ✅ Cleaned: my_package, my_interfaces

   Next:
     /ros2-build my_package my_interfaces
   ```

10. **Warn** if `install/setup.bash` is currently sourced in the shell — cleaning install/ will break the current session:
    ```
    ⚠  WARNING: You may have install/setup.bash sourced in your current shell.
    After cleaning, re-source:
      source /opt/ros/$ROS_DISTRO/setup.bash
      source install/setup.bash  (after rebuild)
    ```
