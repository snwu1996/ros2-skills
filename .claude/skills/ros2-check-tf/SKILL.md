---
name: ros2-check-tf
description: Validate the ROS2 TF tree. Echo transforms between frames, detect missing or broken chains, check latency, and identify stale transforms. Usage: /ros2-check-tf [parent_frame child_frame] [--tree] [--latency] [--all]
argument-hint: [parent_frame child_frame] [--tree] [--latency] [--all]
allowed-tools: Bash
---

# ROS2 TF Tree Checker

Inspect and validate the ROS2 TF transform tree. Arguments: `$ARGUMENTS`

Parse arguments:
- **parent_frame** and **child_frame**: if both given, echo the transform between them
- **--tree**: print the full TF tree structure
- **--latency**: check transform latency for all active frames
- **--all**: run the full diagnostic suite (tree + latency + issue detection)
- If no arguments given, default to `--all`

## Steps

1. **Check that a TF publisher is running**:
   ```bash
   ros2 topic list | grep tf
   ```
   Expect to see `/tf` and/or `/tf_static`. If neither exists, warn: no TF data is being published and stop.

   Also check:
   ```bash
   ros2 topic info /tf
   ros2 topic info /tf_static
   ```
   Show publisher count and rate for each.

2. **If --tree or --all**, print the TF tree using view_frames or tf2_echo:
   ```bash
   ros2 run tf2_tools view_frames
   ```
   If `view_frames` is unavailable, reconstruct the tree manually:
   ```bash
   timeout 3 ros2 topic echo /tf --no-arr
   timeout 3 ros2 topic echo /tf_static --no-arr
   ```
   Parse the frame IDs and parent→child relationships. Display as indented tree:
   ```
   TF Tree:
   map
   └─ odom
      └─ base_footprint
         └─ base_link
            ├─ base_laser_link
            ├─ camera_link
            │  └─ camera_optical_frame
            └─ imu_link
   ```
   Note next to each frame: source (static/dynamic), last update age.

3. **If parent_frame and child_frame given**, echo the transform:
   ```bash
   ros2 run tf2_ros tf2_echo <parent_frame> <child_frame>
   ```
   Run for 3 seconds and display:
   - Translation (x, y, z)
   - Rotation (quaternion and roll/pitch/yaw in degrees)
   - Timestamp and age

   If the transform fails, report the exact error (e.g., `"map" passed to lookupTransform argument target_frame does not exist`).

4. **Detect common TF issues**:

   a. **Broken chain** — a frame appears as a child in some transforms but never as a parent connecting upward to `map` or `odom`:
      - Flag: `WARN: <frame> may be a disconnected island`

   b. **Stale transforms** — a frame's last update is older than 1 second for a dynamic frame:
      ```bash
      timeout 2 ros2 topic hz /tf
      ```
      If rate is 0 or very low, flag: `WARN: /tf publishing at <N> Hz — transforms may be stale`

   c. **Multiple map/world frames** — more than one frame at the root level:
      - Flag: `WARN: multiple root frames detected: [<frame1>, <frame2>]` — this usually causes TF conflicts

   d. **Missing standard frames** — check for absence of expected frames:
      - `odom` → `WARN: no odom frame — odometry may not be publishing`
      - `base_link` → `WARN: no base_link frame — robot model may not be loaded`
      - `map` → `INFO: no map frame — localization may not be running`

5. **If --latency or --all**, measure transform latency:
   ```bash
   timeout 3 ros2 topic echo /tf --no-arr
   ```
   Compare each transform's `header.stamp` to current time. Flag:
   - Age > 0.5s → `WARN: <frame>→<child> transform is <age>s old`
   - Age > 2.0s → `ERROR: <frame>→<child> transform is stale — lookupTransform will fail`

6. **Summary report**:
   ```
   ══════════════════════════════════════════
   TF Status  |  Frames: 12  |  Issues: 2
   ══════════════════════════════════════════
   ❌ ERROR  base_link→camera_link: transform stale (3.2s old)
   ⚠  WARN   Multiple roots: [map, map_2] — possible conflict
   ✅ OK     map→odom→base_link chain complete
   ══════════════════════════════════════════
   ```

7. **Suggest fixes** based on issues found:
   - Stale transform → check the node publishing that frame: `ros2 node list`, `ros2 topic hz /tf`
   - Broken chain → check `robot_state_publisher` is running and URDF is loaded
   - Missing `odom` → check odometry node: `ros2 node list | grep odom`
   - Multiple roots → check for duplicate `map` publishers or namespacing issues
