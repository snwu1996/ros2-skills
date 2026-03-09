---
name: ros2-sim-time
description: Manage ROS2 simulation time — enable/disable use_sim_time on running nodes, check for clock-source mismatches, and diagnose sim-time-related bugs. Usage: /ros2-sim-time [--enable] [--disable] [--status] [--node node_name]
argument-hint: [--enable] [--disable] [--status] [--node node_name]
allowed-tools: Bash
---

# ROS2 Simulation Time Manager

Inspect and control `use_sim_time` across ROS2 nodes. Arguments: `$ARGUMENTS`

Parse arguments:
- **--enable**: set `use_sim_time=true` on all running nodes (or `--node` scoped)
- **--disable**: set `use_sim_time=false` on all running nodes
- **--status**: show current `use_sim_time` state for all nodes (default if no flag given)
- **--node name**: scope enable/disable to a single node

## Background

`use_sim_time` is one of the most common sources of bugs in ROS2 simulation:
- Nodes using **real time** won't receive messages from bags or Gazebo correctly
- TF lookups fail with "extrapolation into the future" when clocks are mixed
- `ros2 topic hz` shows 0 Hz when sim time is paused

The `/clock` topic must be published (by Gazebo or `ros2 bag play`) before `use_sim_time=true` nodes will advance.

## Steps

1. **Check if /clock is being published**:
   ```bash
   ros2 topic list | grep clock
   ros2 topic info /clock 2>/dev/null
   ```
   Report: publisher count and rate.
   ```bash
   timeout 2 ros2 topic hz /clock 2>/dev/null | tail -3
   ```

2. **Get all running nodes**:
   ```bash
   ros2 node list
   ```

3. **Check `use_sim_time` for each node**:
   ```bash
   for node in $(ros2 node list); do
     val=$(ros2 param get $node use_sim_time 2>/dev/null)
     echo "$node: $val"
   done
   ```

4. **Display status dashboard**:
   ```
   Clock source: /clock  (published by /gazebo at 1000 Hz)

   Node sim-time status:
   ══════════════════════════════════════════════════
   Node                      use_sim_time   Clock OK?
   ══════════════════════════════════════════════════
   /move_base                true           ✅
   /slam_toolbox             true           ✅
   /robot_state_publisher    false          ⚠  MISMATCH
   /camera_driver            false          ⚠  MISMATCH
   /rviz2                    true           ✅
   ══════════════════════════════════════════════════
   Mismatches: 2 nodes using real time while /clock is active
   ```

5. **Flag mismatches** — nodes where `use_sim_time` doesn't match the expected mode:
   - `/clock` is published + node has `use_sim_time=false` → `⚠ MISMATCH — node using real time`
   - `/clock` not published + node has `use_sim_time=true` → `❌ ERROR — node waiting for clock that never comes`

6. **If --enable**, set `use_sim_time=true` on all nodes (or scoped node):
   ```bash
   for node in $(ros2 node list); do
     ros2 param set $node use_sim_time true 2>/dev/null && echo "✅ $node" || echo "⚠  $node (failed — may be read-only)"
   done
   ```
   Warn: this takes effect immediately but is not persistent — nodes will revert on restart unless the parameter is set in a YAML file or launch argument.

7. **If --disable**, set `use_sim_time=false` on all nodes similarly.

8. **If --node given**, scope only to that node:
   ```bash
   ros2 param set <node> use_sim_time <true|false>
   ros2 param get <node> use_sim_time
   ```

9. **Detect common sim-time bugs**:

   **"extrapolation into the future"** in TF:
   - Cause: one node using sim time, TF publisher using real time (or vice versa)
   - Fix: ensure all nodes agree on `use_sim_time`

   **`ros2 topic hz` shows 0 Hz or wrong rate**:
   - Cause: `use_sim_time=true` but `/clock` paused or not published
   - Check: `ros2 topic hz /clock`

   **Bag playback messages not received**:
   - Cause: `ros2 bag play` publishes `/clock` but consuming nodes have `use_sim_time=false`
   - Fix: `/ros2-sim-time --enable` then replay

   **Timestamps in the past on messages**:
   - Cause: sim time running slower than real time
   - Check Gazebo real-time factor: `ros2 topic echo /gazebo/performance_metrics`

10. **How to set permanently** — show the correct patterns:

    **In launch file:**
    ```python
    Node(
        package='my_pkg',
        executable='my_node',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )
    ```

    **In YAML params file:**
    ```yaml
    /my_node:
      ros__parameters:
        use_sim_time: true
    ```

    **At launch:**
    ```bash
    ros2 launch my_pkg bringup.launch.py use_sim_time:=true
    ```
