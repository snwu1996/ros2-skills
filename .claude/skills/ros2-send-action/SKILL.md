---
name: ros2-send-action
description: Send a ROS2 action goal and monitor feedback and result. Usage: /ros2-send-action <action> [action_type] [field:value ...] [--timeout sec] [--cancel-after sec]
argument-hint: <action_name> [action_type_or_auto] [field:value ...] [--timeout sec] [--cancel-after sec]
allowed-tools: Bash
---

# ROS2 Action Goal Sender

Send a goal to a ROS2 action server and monitor feedback until completion. Arguments: `$ARGUMENTS`

Parse arguments:
- **action**: first argument — action name (e.g. `/navigate_to_pose`, `/move_base`). Prepend `/` if missing.
- **action_type**: second argument — full type like `nav2_msgs/action/NavigateToPose`, or `auto` to detect
- **field:value pairs**: goal fields as `field:value` or `{yaml: dict}` syntax
- **--timeout sec**: max time to wait for result (default: `30`)
- **--cancel-after sec**: send a cancel request after this many seconds (useful for testing cancellation)
- **--feedback-only**: print feedback messages only, don't wait for result

## Steps

1. **List available actions** and verify the action exists:
   ```bash
   ros2 action list
   ```
   If not found, show the full action list and close matches. Stop.

2. **Get the action type** if not provided or `auto`:
   ```bash
   ros2 action type <action>
   ```

3. **Show the action interface** (goal/result/feedback):
   ```bash
   ros2 interface show <action_type>
   ```
   Display all three sections clearly labeled so the user knows what to expect.

4. **Check the action server is ready**:
   ```bash
   ros2 action info <action>
   ```
   Show number of action servers. If 0 servers, stop and tell the user no server is running.

5. **Build the goal YAML** from provided field:value pairs:
   - Parse into nested YAML dict matching the goal section of the interface
   - If no fields given, use `{}` for empty goals or show the interface and ask
   - Validate field names; warn on unknown fields

   Common action patterns:
   | Action type | Typical goal fields |
   |---|---|
   | `nav2_msgs/action/NavigateToPose` | `{pose: {header: {frame_id: map}, pose: {position: {x: 1.0, y: 0.0}}}}` |
   | `control_msgs/action/FollowJointTrajectory` | complex trajectory — ask user |
   | `nav2_msgs/action/Spin` | `{target_yaw: 1.57}` |

6. **Display the command** before running:
   ```bash
   ros2 action send_goal <action> <action_type> '<yaml_dict>'
   ```
   With feedback: add `--feedback`

7. **Run the goal** and stream output:
   ```bash
   timeout <timeout> ros2 action send_goal --feedback <action> <action_type> '<yaml_dict>'
   ```

8. **Monitor and format the output** in real time:
   - **Accepted/Rejected**: show goal acceptance status prominently
   - **Feedback**: show each feedback update on one line (summarize, don't dump full YAML for each)
   - **Result**: show final result clearly with success/failure status

   Example formatted output:
   ```
   Goal sent to /navigate_to_pose
   Status: ACCEPTED

   Feedback:
     [0.5s]  distance_remaining: 3.42m
     [1.0s]  distance_remaining: 2.87m
     [2.1s]  distance_remaining: 1.23m
     [3.4s]  distance_remaining: 0.05m

   Result: SUCCESS
     result.error_code: 0
   ```

9. **If --cancel-after is given**, after that delay send a cancel in a second terminal command and report the cancellation result.

10. **On failure or timeout**:
    - Show the last feedback received
    - Show the error code if available
    - Suggest checking node status: `ros2 node info <server_node>`
    - For nav2 actions, suggest checking the behavior tree or costmaps
