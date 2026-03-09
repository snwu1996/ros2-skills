---
name: ros2-node-graph
description: Print the ROS2 computation graph as text — nodes, topics, connections, and directions. Detect orphaned nodes, isolated subgraphs, and unexpected connections. Usage: /ros2-node-graph [--node <name>] [--topic <name>] [--orphans] [--compact]
argument-hint: [--node <name>] [--topic <name>] [--orphans] [--compact]
allowed-tools: Bash
---

# ROS2 Node Graph

Render the live ROS2 computation graph as text. Arguments: `$ARGUMENTS`

Parse arguments:
- **--node name**: focus on a single node and its direct connections
- **--topic name**: focus on a single topic and its publishers/subscribers
- **--orphans**: highlight nodes with no publishers or subscribers
- **--compact**: one-line-per-connection format instead of grouped blocks
- If no arguments given, render the full graph

## Steps

1. **Collect all running nodes**:
   ```bash
   ros2 node list
   ```
   If no nodes found, report that no ROS2 nodes are running and stop.

2. **For each node, collect its publishers and subscribers**:
   ```bash
   ros2 node info <node>
   ```
   Parse out: Subscribers, Publishers, Service Servers, Service Clients, Action Servers, Action Clients.
   Skip internal ROS2 topics (`/rosout`, `/parameter_events`, `/_action/`).

3. **Build the connection map** — for each topic:
   - Which nodes publish to it
   - Which nodes subscribe to it

4. **Render the graph** in grouped blocks:

   ```
   ROS2 Computation Graph  (12 nodes, 18 topics)
   ══════════════════════════════════════════════

   TOPICS
   ──────────────────────────────────────────────
   /camera/image_raw          sensor_msgs/Image
     PUB: /camera_driver
     SUB: /image_processor  /rviz2

   /scan                      sensor_msgs/LaserScan
     PUB: /lidar_driver
     SUB: /slam_toolbox  /obstacle_detector

   /cmd_vel                   geometry_msgs/Twist
     PUB: /teleop_keyboard  /move_base
     SUB: /diff_drive_controller

   /odom                      nav_msgs/Odometry
     PUB: /diff_drive_controller
     SUB: /robot_localization  /move_base  /rviz2

   SERVICES
   ──────────────────────────────────────────────
   /set_mode                  std_srvs/SetBool
     SERVER: /mission_manager
     CLIENT: /ui_node

   ACTIONS
   ──────────────────────────────────────────────
   /navigate_to_pose          nav2_msgs/NavigateToPose
     SERVER: /bt_navigator
     CLIENT: /mission_manager
   ```

5. **If --compact flag**, render as connection lines instead:
   ```
   /camera_driver ──/camera/image_raw──▶ /image_processor
   /camera_driver ──/camera/image_raw──▶ /rviz2
   /lidar_driver  ──/scan──────────────▶ /slam_toolbox
   /lidar_driver  ──/scan──────────────▶ /obstacle_detector
   ```

6. **If --node flag**, show only that node's neighbourhood:
   ```
   Focus: /image_processor
   ══════════════════════════════════════════════
   Incoming:
     /camera_driver ──/camera/image_raw──▶ [/image_processor]
   Outgoing:
     [/image_processor] ──/detections──▶ /object_tracker
     [/image_processor] ──/viz_markers──▶ /rviz2 (no other subscribers)
   ```

7. **If --topic flag**, show publisher/subscriber details for that topic:
   ```bash
   ros2 topic info <topic> --verbose
   ```
   Display QoS profiles side by side for each publisher and subscriber.

8. **Detect and flag issues**:

   - **Orphaned publisher** — topic with publishers but 0 subscribers:
     `⚠  /debug_image — published by /camera_driver but no subscribers`

   - **Orphaned subscriber** — topic with subscribers but 0 publishers:
     `❌ /scan — subscribed by /slam_toolbox but no publisher found`

   - **Multiple publishers** on same topic (potential conflict):
     `⚠  /cmd_vel — 2 publishers (/teleop_keyboard, /move_base) — ensure only one publishes at a time`

   - **Isolated node** — node with no connections at all:
     `⚠  /idle_node — no publishers or subscribers`

9. **If --orphans flag**, print only the issues section (skip full graph).

10. **Summary line**:
    ```
    ══════════════════════════════════════════════
    Nodes: 12  Topics: 18  Services: 4  Actions: 2
    Issues: 3 warnings  (run --orphans to filter)
    ```
