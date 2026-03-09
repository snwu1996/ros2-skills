---
name: ros2-qos
description: Diagnose ROS2 QoS mismatches on a topic. Compare publisher and subscriber profiles, explain incompatibilities in plain English, and suggest fixes. Usage: /ros2-qos <topic> [--set publisher|subscriber] [--explain]
argument-hint: <topic> [--set publisher|subscriber] [--explain]
allowed-tools: Bash
---

# ROS2 QoS Diagnostics

Diagnose Quality of Service mismatches on a ROS2 topic. Arguments: `$ARGUMENTS`

Parse arguments:
- **topic**: first argument — topic name. Prepend `/` if missing.
- **--set publisher|subscriber**: show what QoS settings the publisher or subscriber side should use
- **--explain**: print a plain-English explanation of every QoS policy
- If no arguments given, prompt for a topic name

## QoS Policy Reference

| Policy | Values | Compatibility rule |
|---|---|---|
| Reliability | RELIABLE / BEST_EFFORT | Publisher RELIABLE + Subscriber BEST_EFFORT = OK. Reverse = MISMATCH |
| Durability | VOLATILE / TRANSIENT_LOCAL | Publisher TRANSIENT_LOCAL + Subscriber VOLATILE = OK. Reverse = MISMATCH |
| History | KEEP_LAST(N) / KEEP_ALL | Always compatible, affects queue depth only |
| Deadline | duration | Publisher deadline ≤ subscriber deadline = OK |
| Liveliness | AUTOMATIC / MANUAL | Must match |
| Lifespan | duration | Publisher-side only |

## Steps

1. **Verify the topic exists**:
   ```bash
   ros2 topic list
   ```
   If not found, show similar topic names and stop.

2. **Get verbose topic info** (includes QoS profiles):
   ```bash
   ros2 topic info <topic> --verbose
   ```

3. **Parse and display all publisher and subscriber QoS profiles**:

   ```
   Topic: /camera/image_raw  (sensor_msgs/msg/Image)
   ══════════════════════════════════════════════════

   Publishers (1):
   ┌─────────────────────────────────────────┐
   │ Node: /camera_driver                    │
   │ Reliability:  RELIABLE                  │
   │ Durability:   VOLATILE                  │
   │ History:      KEEP_LAST (10)            │
   │ Deadline:     unspecified               │
   │ Liveliness:   AUTOMATIC                 │
   └─────────────────────────────────────────┘

   Subscribers (2):
   ┌─────────────────────────────────────────┐
   │ Node: /image_processor                  │
   │ Reliability:  RELIABLE         ✅       │
   │ Durability:   VOLATILE         ✅       │
   │ History:      KEEP_LAST (5)    ✅       │
   └─────────────────────────────────────────┘
   ┌─────────────────────────────────────────┐
   │ Node: /rviz2                            │
   │ Reliability:  BEST_EFFORT      ✅ OK    │
   │ Durability:   TRANSIENT_LOCAL  ❌ MISMATCH │
   └─────────────────────────────────────────┘
   ```

4. **Detect mismatches** by applying the compatibility rules:

   For each publisher–subscriber pair, check:
   - Reliability: BEST_EFFORT pub + RELIABLE sub → MISMATCH
   - Durability: VOLATILE pub + TRANSIENT_LOCAL sub → MISMATCH
   - Deadline: sub deadline < pub deadline → MISMATCH

5. **Explain each mismatch in plain English**:

   ```
   ❌ MISMATCH: /rviz2 will NOT receive messages from /camera_driver

   Cause: Durability mismatch
     Publisher (/camera_driver): VOLATILE
       → Does not store messages. New subscribers miss anything sent before they connected.
     Subscriber (/rviz2): TRANSIENT_LOCAL
       → Expects to receive messages published before it connected (late-joining behavior).

   Fix options:
     Option A — Change publisher to TRANSIENT_LOCAL (if late-joining support is needed):
       In /camera_driver, set: qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
     Option B — Change subscriber to VOLATILE (simpler, loses late-join):
       In /rviz2, set: qos.durability = QoSDurabilityPolicy.VOLATILE
   ```

6. **Generate fix code snippets** for both Python and C++:

   **Python fix:**
   ```python
   from rclpy.qos import QoSProfile, QoSDurabilityPolicy, ReliabilityPolicy

   qos = QoSProfile(
       depth=10,
       reliability=ReliabilityPolicy.RELIABLE,
       durability=QoSDurabilityPolicy.VOLATILE,
   )
   self.pub = self.create_publisher(Image, '/camera/image_raw', qos)
   ```

   **C++ fix:**
   ```cpp
   auto qos = rclcpp::QoS(rclcpp::KeepLast(10))
       .reliable()
       .durability_volatile();
   pub_ = create_publisher<sensor_msgs::msg::Image>("/camera/image_raw", qos);
   ```

7. **If --explain flag**, print a plain-English explanation of every QoS policy:

   - **Reliability RELIABLE**: every message is guaranteed to be delivered (retransmits on loss). Use for commands, state, critical data.
   - **Reliability BEST_EFFORT**: messages may be dropped. Use for high-rate sensor streams where dropping is acceptable.
   - **Durability TRANSIENT_LOCAL**: publisher stores sent messages; new subscribers receive them immediately on connect.
   - **Durability VOLATILE**: no storage. New subscribers only get messages sent after they connect.
   - **History KEEP_LAST(N)**: queue holds the last N messages. If subscriber is slow, older messages are dropped.
   - **Deadline**: if no message is published within this period, a deadline-missed event fires.

8. **If no mismatches found**:
   ```
   ✅ All publishers and subscribers on <topic> have compatible QoS profiles.
   ```

9. **Common sensor QoS presets** — suggest the right preset for the topic type:
   - Camera/lidar → sensor data preset: BEST_EFFORT, VOLATILE, KEEP_LAST(5)
   - Navigation commands → reliable: RELIABLE, VOLATILE, KEEP_LAST(1)
   - Map/costmap → map preset: RELIABLE, TRANSIENT_LOCAL, KEEP_LAST(1)
   - TF → BEST_EFFORT, VOLATILE, KEEP_LAST(100)
