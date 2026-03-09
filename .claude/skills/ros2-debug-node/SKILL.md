---
name: ros2-debug-node
description: Inspect a running ROS2 node's publishers, subscribers, services, actions, and parameters. Surface common issues like missing connections, QoS mismatches, and stale topics. Usage: /ros2-debug-node <node_name> [--params] [--qos] [--graph]
argument-hint: <node_name> [--params] [--qos] [--graph]
allowed-tools: Bash
---

# ROS2 Node Debugger

Inspect a running ROS2 node and surface potential issues. Arguments: `$ARGUMENTS`

Parse arguments:
- **node**: first argument — node name (e.g. `/move_base`, `controller_manager`). Prepend `/` if missing.
- **--params**: also dump all parameter values
- **--qos**: include QoS profile info for all topics (verbose)
- **--graph**: show a text-based connectivity graph for the node

## Steps

1. **List all running nodes** and verify the target exists:
   ```bash
   ros2 node list
   ```
   If the node is not found, show the full node list and fuzzy-match suggestions. Stop.

2. **Get full node info**:
   ```bash
   ros2 node info <node>
   ```
   Parse and display in clearly labeled sections:

   **Subscribers:**
   | Topic | Type |
   |---|---|
   | /topic | msg_type |

   **Publishers:**
   | Topic | Type |
   |---|---|
   | /topic | msg_type |

   **Service Servers:**
   | Service | Type |
   |---|---|

   **Action Servers / Clients:** (extract from services — look for `_action/` prefixes)

3. **Check topic health** — for each subscribed and published topic, verify:
   ```bash
   ros2 topic info <topic>
   ```
   Flag these issues:
   - Subscriber with 0 matching publishers → `WARN: no publisher for <topic>`
   - Publisher with 0 subscribers → `INFO: no subscribers for <topic>` (may be normal)
   - Topic present in node info but absent from `ros2 topic list` → `WARN: ghost topic`

4. **Check topic activity** — for each topic, quickly check message rate:
   ```bash
   timeout 2 ros2 topic hz <topic>
   ```
   Run these in parallel where possible. Flag:
   - Expected-active topics with 0 Hz → `WARN: <topic> — no messages received`
   - Unexpectedly high rate (>500 Hz) → `INFO: <topic> high rate`

5. **If --qos flag**, for each topic show QoS profile:
   ```bash
   ros2 topic info <topic> --verbose
   ```
   Compare publisher and subscriber QoS and flag incompatibilities:
   - Reliability: RELIABLE publisher with BEST_EFFORT subscriber (or vice versa) → `ERROR: QoS mismatch`
   - Durability mismatch → `WARN: durability mismatch`

6. **If --params flag**, dump all parameters:
   ```bash
   ros2 param list <node>
   ros2 param dump <node>
   ```
   Display as a clean YAML block.

7. **If --graph flag**, show connectivity:
   ```bash
   ros2 node info <node>
   ```
   Draw ASCII diagram:
   ```
   [/camera_node] ──/image_raw──▶ [<this_node>]
   [<this_node>] ──/detections──▶ [/display_node]
                ──/stats──▶ (no subscribers)
   ```

8. **Summary report** — always end with:
   ```
   ══════════════════════════════════════════
   Node: /my_node  |  Issues found: 3
   ══════════════════════════════════════════
   ❌ ERROR  /cmd_vel — QoS reliability mismatch with /teleop_node
   ⚠  WARN   /scan — no publisher connected
   ℹ  INFO   /diagnostics — no subscribers (0 consumers)
   ══════════════════════════════════════════
   ```
   If no issues found, print `✅ No issues detected`.

9. **Suggest next steps** based on findings:
   - QoS mismatch → recommend `/ros2-qos` or checking remapping
   - Missing publisher → check if upstream node is running: `ros2 node list | grep <expected_node>`
   - No activity on a topic → check if node is properly initialized: `ros2 param get <node> use_sim_time`
