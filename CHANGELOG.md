# Changelog

All notable changes to ros2-skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- `/ros2-moveit-setup` — scaffold MoveIt2 configuration for a manipulator
- `/ros2-security` — set up SROS2 keys, certificates, and policy files

---

## [1.3.0] - 2026-03-08

### Added

**Workspace Management (2):**
- `/ros2-workspace` — scaffold a new ROS2 workspace with `src/`, `.colcon/defaults.yaml` (symlink-install), `colcon.meta` (RelWithDebInfo), `.gitignore`, README, and git init
- `/ros2-clean` — clean `build/`, `install/`, `log/` directories per-package or entirely; shows disk usage before/after; warns when install/ is sourced

**Testing (1):**
- `/ros2-test` — run `colcon test` for one or more packages; parse pytest XML and gtest XML; display per-failure details with file:line; `--rerun-failed` flag

**Debugging & Inspection (3):**
- `/ros2-log` — view and filter ROS2 logs from `~/.ros/log/`; filter by severity, node name, or pattern; `--list` sessions; `--search` across sessions; highlights common error patterns with fix suggestions
- `/ros2-pkg-info` — inspect any installed ROS2 package: share directory, executables, launch files with listed arguments, config files, interfaces, and mesh assets
- `/ros2-perf` — profile a running node's CPU% and RSS/VSZ memory over time; detect memory growth; measure topic rates and header-stamp latency; `--cpu`, `--mem`, `--latency`

**Runtime & Execution (2):**
- `/ros2-launch` — run a ROS2 launch file by package+name or direct file path; stream output, detect startup errors, verify nodes came up
- `/ros2-run` — run a single node standalone by package+executable or direct Python script path; supports remappings, parameters, background mode, startup error diagnosis

**Simulation & Infrastructure (3):**
- `/ros2-gazebo` — launch Gazebo Classic (Humble) or Gazebo Harmonic (Iron/Jazzy); spawn a robot from URDF/Xacro; `--headless`, `--paused`; verify essential topics after spawn
- `/ros2-sim-time` — inspect `use_sim_time` on all running nodes; detect clock mismatches; `--enable`/`--disable` sets the parameter live; explains extrapolation bugs
- `/ros2-domain` — show `ROS_DOMAIN_ID` status; `--scan` domains 0–50 for active nodes; `--set` with session and permanent instructions; `--isolate` generates multi-robot env files and `domain_bridge` config

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

[Unreleased]: https://github.com/snwu1996/ros2-skills/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/snwu1996/ros2-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/snwu1996/ros2-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/snwu1996/ros2-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/snwu1996/ros2-skills/releases/tag/v1.0.0
