---
name: ros2-lifecycle
description: Manage ROS2 lifecycle nodes. List managed nodes, get their state, and trigger transitions (configure, activate, deactivate, cleanup, shutdown). Usage: /ros2-lifecycle [node] [configure|activate|deactivate|cleanup|shutdown] [--all]
argument-hint: [node_name] [configure|activate|deactivate|cleanup|shutdown] [--all]
allowed-tools: Bash
---

# ROS2 Lifecycle Node Manager

Inspect and control ROS2 lifecycle-managed nodes. Arguments: `$ARGUMENTS`

Parse arguments:
- **node**: lifecycle node name (e.g. `/camera_driver`). Prepend `/` if missing.
- **transition**: one of `configure`, `activate`, `deactivate`, `cleanup`, `shutdown`
- **--all**: apply the transition to ALL managed nodes (use with caution)
- **--status**: just show current state of the node (no transition)
- If only a node name is given (no transition), default to `--status`
- If no arguments given, list all lifecycle nodes and their states

## Lifecycle State Machine Reference

```
          ┌─────────────────────────────────────────────────┐
          │            Lifecycle State Machine               │
          │                                                  │
          │  [unconfigured] ──configure──▶ [inactive]        │
          │  [inactive]     ──activate───▶ [active]          │
          │  [active]       ──deactivate─▶ [inactive]        │
          │  [inactive]     ──cleanup────▶ [unconfigured]    │
          │  [any]          ──shutdown───▶ [finalized]       │
          └─────────────────────────────────────────────────┘
```

## Steps

1. **List all lifecycle-managed nodes** (always run this first):
   ```bash
   ros2 lifecycle nodes
   ```
   If no lifecycle nodes found, inform the user: no nodes implementing the managed lifecycle interface are currently running.

2. **If no arguments or just listing**, display state of all managed nodes:
   ```bash
   ros2 lifecycle nodes
   ```
   For each node, get its current state:
   ```bash
   ros2 lifecycle get <node>
   ```
   Display as a table:
   ```
   Lifecycle Nodes
   ─────────────────────────────────────────────────
   Node                      State         ID
   ─────────────────────────────────────────────────
   /camera_driver            active         3
   /lidar_driver             inactive       2
   /imu_driver               unconfigured   1
   /map_server               active         3
   ─────────────────────────────────────────────────
   ```
   Color-code states: active=✅, inactive=⚠, unconfigured=⬜, finalized=❌

3. **If --status or only a node name given**, get detailed state:
   ```bash
   ros2 lifecycle get <node>
   ```
   Show:
   - Current state name and ID
   - Available transitions from this state
   - How to reach `active` from current state (transition path)

   Example:
   ```
   /camera_driver
     State:    inactive (id: 2)
     Available transitions:
       - activate   → active
       - cleanup    → unconfigured
       - shutdown   → finalized
     To reach active: run /ros2-lifecycle /camera_driver activate
   ```

4. **If a transition is given**, validate it is legal from the current state:
   ```bash
   ros2 lifecycle get <node>
   ```
   If the transition is not valid from the current state, explain why and show the valid path.
   Example: `ERROR: cannot activate /camera_driver from unconfigured — configure first`

5. **Execute the transition**:
   ```bash
   ros2 lifecycle set <node> <transition>
   ```
   Common transitions:
   | Command | Transition | From → To |
   |---|---|---|
   | `configure` | configure | unconfigured → inactive |
   | `activate` | activate | inactive → active |
   | `deactivate` | deactivate | active → inactive |
   | `cleanup` | cleanup | inactive → unconfigured |
   | `shutdown` | shutdown | any → finalized |

6. **Confirm the new state**:
   ```bash
   ros2 lifecycle get <node>
   ```
   Display result: `✅ /camera_driver transitioned to: active`
   If the transition failed, show the error and suggest checking node logs:
   ```bash
   ros2 node info <node>
   ```

7. **If --all flag given**, apply transition to every managed node:
   - First list all nodes and their current states
   - Warn: `About to trigger '<transition>' on ALL managed nodes. Ctrl-C to abort.`
   - Sleep 2 seconds
   - Loop through each node, run the transition, report result
   - Skip nodes where the transition is not valid from their current state (report skipped)

8. **Common workflows** — detect and suggest if the user seems to be doing one:

   **Full startup sequence** (if nodes are all unconfigured):
   ```bash
   ros2 lifecycle set <node> configure
   ros2 lifecycle set <node> activate
   ```
   Suggest: "Run `/ros2-lifecycle <node> configure` then `/ros2-lifecycle <node> activate`"

   **Clean restart** (if node is active and user wants to reset):
   ```bash
   ros2 lifecycle set <node> deactivate
   ros2 lifecycle set <node> cleanup
   ros2 lifecycle set <node> configure
   ros2 lifecycle set <node> activate
   ```

9. **Suggest next steps** after transition:
   - After activate → check topic output: `/ros2-sub <published_topic>`
   - After deactivate → topics will stop publishing
   - After shutdown → node process will exit
