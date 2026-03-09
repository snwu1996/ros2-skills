---
name: ros2-sub
description: Subscribe to a ROS2 topic for a given duration and summarize the received data. Usage: /ros2-sub <topic> [duration_sec] [--count N] [--raw]
argument-hint: <topic> [duration_sec] [--count N] [--raw]
allowed-tools: Bash
---

# ROS2 Topic Subscriber

Subscribe to a ROS2 topic and capture messages. Arguments: `$ARGUMENTS`

Parse arguments:
- **topic**: first argument — topic name (e.g. `/cmd_vel`, `scan`). Prepend `/` if missing.
- **duration**: second argument in seconds (default: `5`)
- **--count N**: stop after N messages instead of using a duration
- **--raw**: print full raw message fields (default: summarize)
- **--hz**: just report message frequency, don't print messages (like `ros2 topic hz`)

## Steps

1. **Verify the topic exists** — run:
   ```bash
   ros2 topic list
   ```
   If the topic is not in the list, show the full topic list and stop. If similar topics exist, suggest them.

2. **Get the topic type**:
   ```bash
   ros2 topic info <topic>
   ```
   Extract the message type (e.g. `geometry_msgs/msg/Twist`).

3. **If --hz flag**: run and report results:
   ```bash
   timeout <duration> ros2 topic hz <topic>
   ```

4. **Otherwise, collect messages** using timeout:
   ```bash
   timeout <duration> ros2 topic echo --no-arr <topic>
   ```
   Use `--no-arr` by default to keep output readable (skip large arrays like pointclouds). If `--raw` is given, omit `--no-arr`.

   If `--count N` is given, use:
   ```bash
   ros2 topic echo --once <topic>   # for count=1
   # or pipe through head for N messages
   ```

5. **Summarize the captured data** — do NOT just dump all output. Instead:
   - Report: message type, number of messages received, duration, approximate rate
   - For numeric fields (float/int): show min, max, mean across received messages
   - For string fields: show unique values seen
   - For header fields: show timestamp range
   - For array fields: show length stats
   - Show one representative full message at the end

   Example summary format:
   ```
   Topic:    /cmd_vel  (geometry_msgs/msg/Twist)
   Duration: 5.0s  |  Messages: 12  |  Rate: ~2.4 Hz

   linear.x:   min=-0.5  max=0.5  mean=0.12
   linear.y:   always 0.0
   angular.z:  min=-1.0  max=1.0  mean=-0.03

   Last message:
     linear:  x=0.2, y=0.0, z=0.0
     angular: x=0.0, y=0.0, z=-0.5
   ```

6. If **no messages** were received in the duration, report that and suggest:
   - Check if publishers exist: `ros2 topic info <topic>`
   - Check QoS compatibility: `ros2 topic info <topic> --verbose`
