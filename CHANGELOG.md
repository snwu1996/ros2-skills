# Changelog

All notable changes to ros2-claude-skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `/ros2-launch` — run a ROS2 launch file by package+name or direct file path; launches in background, waits for nodes to come up, detects startup errors, reports active nodes and topics
- `/ros2-run` — run a single node standalone by package+executable or direct Python script path; supports remappings, parameters, params-file, namespace, background mode, and startup error diagnosis

### Planned
- `/ros2-moveit-setup` — scaffold MoveIt2 configuration for a manipulator
- `/ros2-perf` — profile CPU/memory usage of a running node, identify bottlenecks
- `/ros2-security` — set up SROS2 keys, certificates, and policy files

---

## [1.2.0] - 2026-03-08

### Added

**Diagnostics & Observability (3):**
- `/ros2-node-graph` — render the full ROS2 computation graph as text; detect orphaned nodes, isolated subgraphs, multiple publishers on the same topic
- `/ros2-diag` — subscribe to `/diagnostics`, parse `DiagnosticArray` messages, and display a live OK/WARN/ERROR/STALE health dashboard per hardware component
- `/ros2-qos` — diagnose QoS mismatches between publishers and subscribers; explain incompatibilities in plain English; generate Python and C++ fix code

**Code & Config Generation (4):**
- `/ros2-gen-params` — generate a parameter YAML file from a running node's current values; supports template mode with type annotations and comments
- `/ros2-compose` — register a C++ class as a composable node component; update CMakeLists.txt and generate a component container launch file
- `/ros2-docker` — generate a Dockerfile, entrypoint script, `.dockerignore`, and Docker Compose file; supports multi-stage builds and NVIDIA GPU
- `/ros2-nav2-setup` — scaffold `nav2_params.yaml` with full defaults for differential/omnidirectional/Ackermann robots, plus a bringup launch file

**Robot Model (1):**
- `/ros2-urdf-check` — validate URDF/Xacro files; check joint/link consistency, detect missing meshes, display link tree, flag common errors

**Integration & Deployment (2):**
- `/ros2-rosdep` — run `rosdep install`, fix common failures (missing keys, OS mismatches, permission errors), update the database
- `/ros2-remap` — generate remapping syntax for CLI and launch files; search workspace for all uses of a topic

---

## [1.1.0] - 2026-03-08

### Added

**Debugging & Inspection (3):**
- `/ros2-debug-node` — inspect a running node's publishers, subscribers, services, actions, and parameters; surface QoS mismatches, missing connections, and stale topics
- `/ros2-check-tf` — validate the TF tree, detect broken chains, stale transforms, multiple root frames, and missing standard frames (map, odom, base_link)
- `/ros2-lifecycle` — list lifecycle-managed nodes, get their state, and trigger transitions (configure, activate, deactivate, cleanup, shutdown); supports `--all` to transition every managed node

**Action Monitoring (1):**
- `/ros2-monitor-action` — attach to an already-running action goal and stream its feedback without sending a new goal; supports `--cancel`, `--summary`, and `--timeout`

**Bag Files (1):**
- `/ros2-bag` — record topics to a bag (`record`), play back a bag (`play`), and inspect bag contents (`info`); handles sim-time reminders for playback

---

## [1.0.0] - 2026-03-08

### Added

**Code Generation Skills (5):**
- `/ros2-create-pkg` — scaffold CMake or Python ROS2 packages with correct package.xml, CMakeLists.txt/setup.py, and directory structure
- `/ros2-create-node` — generate Python or C++ ROS2 nodes with configurable publishers, subscribers, services, and actions
- `/ros2-create-interface` — create .msg, .srv, or .action interface files and update CMakeLists.txt
- `/ros2-create-launch` — generate Python launch files with parameters, remappings, and namespace support
- `/ros2-create-test` — generate pytest (Python) or gtest (C++) unit and integration tests

**Build & Dependency Skills (2):**
- `/ros2-build` — build ROS2 workspaces with colcon, detect errors, and suggest targeted fixes
- `/ros2-add-dep` — add dependencies to package.xml and the appropriate build file

**Test Infrastructure (1):**
- `/ros2-launch-test` — generate launch_testing tests for full node bringup validation (topics, services, TF, parameters)

**Runtime Inspection Skills (5):**
- `/ros2-param` — get, set, list, dump, and load ROS2 node parameters
- `/ros2-pub` — publish messages to ROS2 topics with configurable rate and count
- `/ros2-sub` — subscribe to ROS2 topics and summarize received data
- `/ros2-call-service` — send ROS2 service requests and display responses
- `/ros2-send-action` — send ROS2 action goals and monitor feedback and result

---

[Unreleased]: https://github.com/YOUR_USERNAME/ros2-claude-skills/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/YOUR_USERNAME/ros2-claude-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/YOUR_USERNAME/ros2-claude-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/YOUR_USERNAME/ros2-claude-skills/releases/tag/v1.0.0
