---
name: ros2-domain
description: Manage ROS2 domain IDs — check the current domain, list nodes across domains, detect conflicts, and configure multi-robot domain isolation. Usage: /ros2-domain [--status] [--scan] [--set ID] [--list] [--isolate robot1:ID1 robot2:ID2]
argument-hint: [--status] [--scan 0-232] [--set <ID>] [--list] [--isolate robot:ID ...]
allowed-tools: Bash, Write
---

# ROS2 Domain Manager

Manage ROS2 `ROS_DOMAIN_ID` for network isolation and multi-robot setups. Arguments: `$ARGUMENTS`

Parse arguments:
- **--status**: show current domain ID and active nodes (default if no flags given)
- **--scan**: scan domain IDs 0–232 for active ROS2 nodes (slow — use carefully on shared networks)
- **--set ID**: set `ROS_DOMAIN_ID` for the current session (prints export command)
- **--list**: list nodes visible on the current domain
- **--isolate robot:ID ...**: generate launch/env setup for multi-robot domain isolation

Current domain: !`echo "ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0 (default)}"`

## Background

`ROS_DOMAIN_ID` (0–232) controls which DDS domain ROS2 nodes communicate on. Nodes on different domains **cannot see each other** — this is the primary mechanism for:
- Isolating multiple robots on the same network
- Preventing interference between developers on the same LAN
- Separating simulation from real-robot traffic

Default domain is `0`. On shared networks, collisions are common.

## Steps

1. **If --status or no args**, show current state:
   ```bash
   echo "Current ROS_DOMAIN_ID: ${ROS_DOMAIN_ID:-0}"
   hostname
   ros2 node list 2>/dev/null
   ros2 topic list 2>/dev/null | wc -l
   ```
   Display:
   ```
   Current Domain: 0 (default)
   Host: my-robot-pc
   Nodes visible: 8
   Topics visible: 24

   ⚠  Domain 0 is the default — anyone on your network with ROS2 running
      will see your nodes. Consider setting a unique domain ID.
   ```

2. **If --list**, show all nodes and topics on the current domain with more detail:
   ```bash
   ros2 node list
   ros2 topic list
   ```
   Group by apparent namespace to reveal robot structure.

3. **If --set ID**, validate the ID is in range (0–232):
   Domain IDs 215–232 are reserved — warn if user picks one.
   Print the commands to set it:
   ```
   To set domain ID for this session:
     export ROS_DOMAIN_ID=42

   To set permanently (bash):
     echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
     source ~/.bashrc

   To set permanently (zsh):
     echo "export ROS_DOMAIN_ID=42" >> ~/.zshrc
     source ~/.zshrc

   ⚠  All nodes in this terminal will now use domain 42.
      Other terminals need the same export to communicate.
   ```

4. **If --scan**, scan for active domains:
   ```bash
   for id in $(seq 0 50); do
     ROS_DOMAIN_ID=$id ros2 node list 2>/dev/null | grep -q "." && echo "Domain $id: ACTIVE"
   done
   ```
   This is slow (~1s per domain). Warn the user and scan 0-50 by default (most common range).
   Display:
   ```
   Scanning domains 0-50...
   Domain  0: ACTIVE  (8 nodes found)
   Domain 12: ACTIVE  (3 nodes found — likely another developer)
   Domain 42: ACTIVE  (1 node — likely yours from another terminal)
   Domain 0-50: 3 active domains found

   Recommendation: use domain 25 (no activity detected)
   ```

5. **If --isolate**, generate multi-robot isolation configuration:

   For `--isolate robot1:10 robot2:20`:

   **Shell setup files:**
   ```bash
   # robot1_env.sh
   export ROS_DOMAIN_ID=10
   export ROS_NAMESPACE=/robot1
   echo "Robot1 environment set (domain 10)"

   # robot2_env.sh
   export ROS_DOMAIN_ID=20
   export ROS_NAMESPACE=/robot2
   echo "Robot2 environment set (domain 20)"
   ```

   **Launch file argument pattern:**
   ```python
   # In bringup.launch.py
   DeclareLaunchArgument('domain_id', default_value='10'),
   SetEnvironmentVariable('ROS_DOMAIN_ID', LaunchConfiguration('domain_id')),
   ```

   **Cross-domain bridge** (if robots need to communicate):
   ```bash
   # Using domain_bridge package
   ros2 run domain_bridge domain_bridge --config bridge_config.yaml
   ```
   Generate `bridge_config.yaml`:
   ```yaml
   # Bridge topics between robot1 (domain 10) and robot2 (domain 20)
   topics:
     - topic: /robot1/odom
       type: nav_msgs/msg/Odometry
       from_domain: 10
       to_domain: 20
   ```

6. **Common domain ID recommendations**:

   | Use case | Suggested domain |
   |---|---|
   | Single developer, isolated | 1-9 (pick anything non-zero) |
   | Team lab (multiple devs) | Assign unique IDs per person: 10, 20, 30... |
   | Robot 1 in fleet | 10 |
   | Robot 2 in fleet | 20 |
   | Simulation | 0 (keep isolated from real robots) |
   | CI/CD pipeline | 100+ (unlikely to conflict) |

7. **Detect domain conflicts**:
   ```bash
   ros2 node list
   ```
   If unexpected nodes appear (nodes you didn't launch):
   ```
   ⚠  Unexpected nodes visible on domain 0:
     /other_developers_node
     /lab_robot_arm

   These are from other ROS2 instances on your network.
   Set a unique domain ID to isolate: /ros2-domain --set <ID>
   ```
