---
name: ros2-bag
description: Record, play back, and inspect ROS2 bag files. Usage: /ros2-bag record [topics...] [--duration sec] [--output name] | play <bag_path> [--rate N] [--topics ...] | info <bag_path>
argument-hint: <record|play|info> [topics|bag_path] [--duration sec] [--rate N] [--output name]
allowed-tools: Bash
---

# ROS2 Bag Tool

Record, play back, and inspect ROS2 bag files. Arguments: `$ARGUMENTS`

Parse arguments:
- **subcommand**: first argument — `record`, `play`, or `info` (required)
- For `record`:
  - **topics**: list of topic names to record (or `-a` for all)
  - **--duration sec**: stop recording after N seconds
  - **--output name**: bag directory name (default: timestamped `rosbag2_YYYY_MM_DD-HH_MM_SS`)
  - **--split-size MB**: split bag into files of this size
- For `play`:
  - **bag_path**: path to the bag directory or `.db3` file
  - **--rate N**: playback rate multiplier (default: `1.0`)
  - **--topics**: only publish these topics during playback
  - **--start-offset sec**: skip this many seconds at the start
  - **--loop**: loop playback continuously
- For `info`:
  - **bag_path**: path to the bag directory or `.db3` file

## Steps

---

### Subcommand: `record`

1. **List available topics** so the user can choose:
   ```bash
   ros2 topic list
   ```
   If no topics given in arguments, show the list and ask which to record. Suggest `-a` for all topics.

2. **Check available disk space**:
   ```bash
   df -h .
   ```
   Warn if less than 1 GB available.

3. **Show the record command** before running:
   ```bash
   ros2 bag record -o <output_name> <topics>
   # With duration:
   timeout <duration> ros2 bag record -o <output_name> <topics>
   # All topics:
   ros2 bag record -a -o <output_name>
   ```

4. **Run recording** and show live status:
   - Display topics being recorded
   - Show message count and bag size periodically
   - Stop after duration if given, or wait for Ctrl-C

5. **On completion**, run `info` automatically on the recorded bag:
   ```bash
   ros2 bag info <output_name>
   ```
   Show: topics recorded, message counts, total duration, file size.

---

### Subcommand: `info`

1. **Verify bag path exists**:
   ```bash
   ls <bag_path>
   ```
   If not found, check current directory for any `rosbag2_*` directories and suggest them.

2. **Show bag info**:
   ```bash
   ros2 bag info <bag_path>
   ```

3. **Format and display clearly**:
   ```
   Bag: /path/to/rosbag2_2024_01_15-10_30_00
   ─────────────────────────────────────────────────────────
   Duration:  45.3 s
   Start:     Jan 15 2024 10:30:00.123
   End:       Jan 15 2024 10:30:45.421
   Size:      234 MB
   Storage:   sqlite3
   ─────────────────────────────────────────────────────────
   Topics (8):
     /camera/image_raw          sensor_msgs/msg/Image       450 msgs  (~9.9 Hz)
     /scan                      sensor_msgs/msg/LaserScan   453 msgs  (~10.0 Hz)
     /odom                      nav_msgs/msg/Odometry       904 msgs  (~19.9 Hz)
     /cmd_vel                   geometry_msgs/msg/Twist     186 msgs  (~4.1 Hz)
     /tf                        tf2_msgs/msg/TFMessage     4521 msgs  (~99.8 Hz)
     /tf_static                 tf2_msgs/msg/TFMessage        3 msgs
     /diagnostics               diagnostic_msgs/msg/DiagnosticArray  45 msgs  (~1.0 Hz)
     /rosout                    rcl_interfaces/msg/Log      312 msgs
   ─────────────────────────────────────────────────────────
   ```

4. **Suggest next steps**:
   - To play: `/ros2-bag play <bag_path>`
   - To play specific topics: `/ros2-bag play <bag_path> --topics /scan /odom`

---

### Subcommand: `play`

1. **Verify bag path exists** and show bag info summary:
   ```bash
   ros2 bag info <bag_path>
   ```

2. **If --topics given**, verify all requested topics exist in the bag. Warn on any not found.

3. **Show the play command** before running:
   ```bash
   ros2 bag play <bag_path>
   # With rate:
   ros2 bag play <bag_path> --rate <rate>
   # Specific topics only:
   ros2 bag play <bag_path> --topics <topic1> <topic2>
   # With start offset:
   ros2 bag play <bag_path> --start-offset <sec>
   # Looping:
   ros2 bag play --loop <bag_path>
   ```

4. **Remind the user** of important playback notes:
   - `/use_sim_time` should be `true` on nodes consuming the bag data
   - Set clock: `ros2 param set /<node> use_sim_time true`
   - The bag publishes `/clock` — consumers must be sim-time-aware
   - To set all nodes: consider launching with `use_sim_time:=true`

5. **Run playback**:
   ```bash
   ros2 bag play <bag_path> [options]
   ```
   Report when playback starts and ends.

6. **On completion**, report:
   - Total messages published
   - Topics published
   - Any topics that were skipped (type mismatch, not found)
