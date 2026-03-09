---
name: ros2-log
description: View, filter, and search ROS2 node logs. Tail the latest session, filter by severity or node name, and find errors across recent sessions. Usage: /ros2-log [node_name] [--level debug|info|warn|error] [--session N] [--search pattern] [--list]
argument-hint: [node_name] [--level warn|error] [--session N] [--search pattern] [--lines N] [--list]
allowed-tools: Bash, Glob, Read
---

# ROS2 Log Viewer

View and filter ROS2 node logs from `~/.ros/log/`. Arguments: `$ARGUMENTS`

Parse arguments:
- **node_name**: filter to logs from this node only (partial match ok)
- **--level**: minimum severity to show — `debug`, `info`, `warn`, `error`, `fatal` (default: `info`)
- **--session N**: use the Nth most recent session (default: `1` = latest)
- **--search pattern**: grep for a pattern across all log files in the session
- **--lines N**: number of lines to show (default: `50`)
- **--list**: list available log sessions and stop
- **--all-sessions**: search across all recent sessions (not just latest)

## Steps

1. **Find the ROS2 log directory**:
   ```bash
   ls ~/.ros/log/ 2>/dev/null || ls /tmp/ros2_log/ 2>/dev/null
   ```
   Default is `~/.ros/log/`. Show the path used.

2. **If --list**, show available sessions:
   ```bash
   ls -lt ~/.ros/log/ | head -20
   ```
   Display:
   ```
   Available log sessions (newest first):
     1  2026-03-08_14-32-01  (latest)
     2  2026-03-08_11-15-44
     3  2026-03-07_09-02-17
     4  2026-03-06_16-45-00
   ```
   Stop after listing.

3. **Select the session directory**:
   ```bash
   SESSION=$(ls -t ~/.ros/log/ | grep -v latest | sed -n '<N>p')
   SESSION_DIR=~/.ros/log/$SESSION
   ```
   Also check `~/.ros/log/latest` symlink for the most recent.

4. **List log files in the session**:
   ```bash
   ls $SESSION_DIR/
   ```
   Show: `launch.log`, per-node log files (`<node_name>-stdout.log`, `<node_name>-stderr.log`), `rosout.log`.

5. **Collect the right log file(s)**:
   - If **node_name given**: find matching files:
     ```bash
     find $SESSION_DIR -name "*<node_name>*" | head -10
     ```
   - If **no node given**: use `rosout.log` (aggregated):
     ```bash
     cat $SESSION_DIR/rosout.log 2>/dev/null
     ```
     Or combine all node logs:
     ```bash
     cat $SESSION_DIR/*.log
     ```

6. **Filter by severity level**:
   Map levels to ROS2 log prefixes:
   - `debug` → show all (`[DEBUG]`, `[INFO]`, `[WARN]`, `[ERROR]`, `[FATAL]`)
   - `info` → `[INFO]`, `[WARN]`, `[ERROR]`, `[FATAL]`
   - `warn` → `[WARN]`, `[ERROR]`, `[FATAL]`
   - `error` → `[ERROR]`, `[FATAL]`
   - `fatal` → `[FATAL]` only

   ```bash
   grep -E "\[(WARN|ERROR|FATAL)\]" $LOG_FILE | tail -<lines>
   ```

7. **If --search given**, search across all log files in the session:
   ```bash
   grep -rn "<pattern>" $SESSION_DIR/ --include="*.log"
   ```
   Show file:line:match for each result.

8. **Format and display log output** — don't dump raw. Colorize by level:
   ```
   Session: 2026-03-08_14-32-01  (latest)
   Node:     /camera_driver  (camera_driver-1.log)
   Showing:  WARN and above  |  last 50 lines
   ══════════════════════════════════════════════════════

   [14:32:01.123] INFO  /camera_driver: Camera initialized at 30Hz
   [14:32:03.441] WARN  /camera_driver: Exposure auto-adjustment taking >100ms
   [14:32:15.002] ERROR /camera_driver: Frame drop detected (3 consecutive)
   [14:32:15.003] WARN  /camera_driver: Reducing resolution to maintain framerate
   [14:33:02.771] ERROR /camera_driver: USB bandwidth saturation — reducing to 15Hz

   ══════════════════════════════════════════════════════
   5 lines shown  (2 WARN, 2 ERROR, 0 FATAL)
   ```

9. **Highlight common error patterns** and suggest fixes:

   | Pattern | Suggested fix |
   |---|---|
   | `TF_OLD_DATA` / `TF_REPEATED_DATA` | Check TF publisher rate: `/ros2-check-tf` |
   | `QoS` / `incompatible QoS` | `/ros2-qos <topic>` |
   | `parameter` not declared | Add param to node init or load params file |
   | `No module named` | `pip3 install <module>` or `/ros2-rosdep` |
   | `Connection refused` | Check hardware connection / driver process |
   | `extrapolation into the future` | Check `use_sim_time` mismatch: `/ros2-sim-time` |

10. **If --all-sessions**, scan across multiple sessions:
    ```bash
    grep -rn "<pattern>" ~/.ros/log/*/rosout.log 2>/dev/null | tail -50
    ```
    Show session timestamps alongside matches so you can correlate with events.
