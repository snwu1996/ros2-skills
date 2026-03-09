---
name: ros2-pub
description: Publish messages to a ROS2 topic for a given duration or count. Usage: /ros2-pub <topic> <msg_type> [values] [--rate hz] [--duration sec] [--count N] [--once]
argument-hint: <topic> <msg_type_or_auto> [field:value ...] [--rate hz] [--duration sec] [--once]
allowed-tools: Bash
---

# ROS2 Topic Publisher

Publish messages to a ROS2 topic. Arguments: `$ARGUMENTS`

Parse arguments:
- **topic**: first argument (e.g. `/cmd_vel`). Prepend `/` if missing.
- **msg_type**: second argument — full type like `geometry_msgs/msg/Twist`, or `auto` to detect from existing subscribers
- **field:value pairs**: remaining key=value or field:value pairs for message data
- **--rate hz**: publish rate in Hz (default: `1.0`)
- **--duration sec**: how long to publish (default: `5`)
- **--count N**: publish exactly N messages then stop
- **--once**: publish a single message (equivalent to --count 1)
- **--zero**: publish a zeroed/default message (useful for stopping a robot)

## Steps

1. **If msg_type is `auto` or not given** — detect from existing subscribers:
   ```bash
   ros2 topic info <topic>
   ```
   Extract the type. If no subscribers exist but the topic is in the list, use the publisher type. If the topic doesn't exist at all, tell the user the type is required.

2. **Determine message content**:

   - If field:value pairs are given, build the YAML message dict from them.
   - If `--zero` is given, use `{}` (default/zero values).
   - If no values are given for a known type, provide a **safe default**:

   | Type | Safe default |
   |---|---|
   | `geometry_msgs/msg/Twist` | `{linear: {x: 0.0}, angular: {z: 0.0}}` |
   | `std_msgs/msg/Bool` | `{data: false}` |
   | `std_msgs/msg/Float64` | `{data: 0.0}` |
   | `std_msgs/msg/String` | `{data: 'hello'}` |
   | `std_msgs/msg/Int32` | `{data: 0}` |
   | Other | `{}` |

   **Safety check**: if the topic is `/cmd_vel`, `/cmd_vel_unstamped`, or similar velocity command topics, warn the user before publishing non-zero velocities and ask to confirm if the values are large (|linear| > 0.5 m/s or |angular| > 1.0 rad/s).

3. **Build and display the command** that will be run (show the user before executing):

   For duration-based publishing:
   ```bash
   timeout <duration> ros2 topic pub --rate <hz> <topic> <msg_type> '<yaml_dict>'
   ```

   For once/count:
   ```bash
   ros2 topic pub --once <topic> <msg_type> '<yaml_dict>'
   ros2 topic pub --times <N> <topic> <msg_type> '<yaml_dict>'
   ```

4. **Run the command** and monitor output:
   - Report when publishing starts
   - Count messages published
   - On completion, report total messages sent and duration

5. **After publishing**, optionally check that the topic received the messages:
   ```bash
   ros2 topic echo --once <topic>
   ```

6. **On error** (bad YAML, unknown type, etc.) — parse the error and suggest a fix:
   - Invalid field name → show the correct message structure with `ros2 interface show <msg_type>`
   - Type not found → suggest `ros2 interface list | grep <keyword>`
