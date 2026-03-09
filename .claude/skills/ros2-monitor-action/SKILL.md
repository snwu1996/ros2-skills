---
name: ros2-monitor-action
description: Monitor feedback from an already-running ROS2 action goal without sending a new one. Stream feedback, check status, and optionally cancel. Usage: /ros2-monitor-action <action> [--cancel] [--timeout sec] [--summary]
argument-hint: <action_name> [--cancel] [--timeout sec] [--summary]
allowed-tools: Bash
---

# ROS2 Action Monitor

Attach to an in-progress ROS2 action and monitor its feedback stream. Does NOT send a new goal — use `/ros2-send-action` for that. Arguments: `$ARGUMENTS`

Parse arguments:
- **action**: first argument — action name (e.g. `/navigate_to_pose`). Prepend `/` if missing.
- **--cancel**: send a cancel request to the active goal after connecting
- **--timeout sec**: stop monitoring after this many seconds (default: `60`)
- **--summary**: instead of streaming, collect for 5s then print a summary of feedback fields

## Steps

1. **Verify the action exists and has an active server**:
   ```bash
   ros2 action list
   ros2 action info <action>
   ```
   Show: number of action servers, number of action clients, goal count.
   If no servers found, stop — nothing to monitor.

2. **Get the action type**:
   ```bash
   ros2 action type <action>
   ```

3. **Show the feedback message schema** so the user knows what fields to expect:
   ```bash
   ros2 interface show <action_type>
   ```
   Extract and display only the `feedback:` section, clearly labeled.

4. **Check for active goals** using action info verbose output:
   ```bash
   ros2 action info <action> --verbose
   ```
   Show goal IDs if visible. Inform the user how many goals are currently active.

5. **If --cancel flag given**, display a warning and ask for confirmation before proceeding:
   ```
   WARNING: This will cancel all active goals on <action>.
   Proceeding in 3 seconds... (Ctrl-C to abort)
   ```
   Then run:
   ```bash
   sleep 3
   ros2 action cancel <action>
   ```
   Report the cancellation response and stop.

6. **Otherwise, stream feedback** by echoing the feedback topic:
   The feedback topic for action `<action>` is `<action>/_action/feedback`.
   ```bash
   timeout <timeout> ros2 topic echo --no-arr <action>/_action/feedback
   ```

7. **Format the streaming output** — do NOT dump raw YAML for every message. Instead:
   - Print a header line: `Monitoring <action> feedback (<action_type>)`
   - For each feedback message, extract the `feedback` sub-field and print it on one line with a timestamp prefix
   - Highlight any field named `status`, `state`, `progress`, `distance_remaining`, `error_code`, `current_waypoint` etc.

   Example formatted output:
   ```
   Monitoring /navigate_to_pose feedback (nav2_msgs/action/NavigateToPose)
   ──────────────────────────────────────────────────────────────────
   [00:01]  distance_remaining: 4.23m  |  speed: 0.25 m/s
   [00:02]  distance_remaining: 3.97m  |  speed: 0.25 m/s
   [00:05]  distance_remaining: 2.11m  |  speed: 0.25 m/s
   [00:08]  distance_remaining: 0.42m  |  speed: 0.10 m/s
   [00:09]  Goal completed (no more feedback)
   ```

8. **If --summary flag given**, collect feedback for 5 seconds, then print:
   - Total feedback messages received
   - Rate (Hz)
   - For numeric fields: min, max, last value
   - For string/enum fields: all unique values seen

9. **If no feedback arrives within 5 seconds**, check whether the action completed already:
   ```bash
   ros2 action info <action>
   ```
   Report if the goal count dropped to 0 (likely completed before we connected).
   Suggest using `/ros2-send-action` to send and monitor a new goal from the start.

10. **On timeout**, report:
    - Total messages received
    - Last feedback values
    - Whether the action server is still running
