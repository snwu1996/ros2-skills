# ros2-claude-skills

**28 production-ready Claude Code skills for ROS2 development** — covering the full robot software lifecycle from package scaffolding and node generation to runtime debugging, TF inspection, QoS diagnostics, Nav2 setup, bag recording, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-28-brightgreen.svg)](#skills)
[![ROS2](https://img.shields.io/badge/ROS2-Humble%20%7C%20Iron%20%7C%20Jazzy-blue.svg)](https://docs.ros.org)

---

## Quick Install

### Project-level (recommended — skills only active in your ROS2 workspace)

```bash
cd ~/ros2_ws
git clone https://github.com/YOUR_USERNAME/ros2-claude-skills.git .ros2-skills
mkdir -p .claude/skills
cp -r .ros2-skills/.claude/skills/* .claude/skills/
```

### User-level (skills available in all Claude Code sessions)

```bash
git clone https://github.com/YOUR_USERNAME/ros2-claude-skills.git ~/ros2-claude-skills
mkdir -p ~/.claude/skills
cp -r ~/ros2-claude-skills/.claude/skills/* ~/.claude/skills/
```

See [INSTALLATION.md](INSTALLATION.md) for symlink install, per-skill install, and troubleshooting.

---

## Skills

### Code Generation

| Skill | Usage | Description |
|---|---|---|
| `/ros2-create-pkg` | `/ros2-create-pkg <name> [cmake\|python] [desc]` | Scaffold a package with package.xml, CMakeLists.txt or setup.py |
| `/ros2-create-node` | `/ros2-create-node <name> [python\|cpp] [--pub topic:type] [--sub topic:type] [--srv name:type] [--action name:type]` | Generate a Python or C++ node with pub/sub/srv/action |
| `/ros2-create-interface` | `/ros2-create-interface <Name> [msg\|srv\|action] [field type ...]` | Create .msg, .srv, or .action files and update CMakeLists.txt |
| `/ros2-create-launch` | `/ros2-create-launch <name> [node:pkg ...] [--param k:v] [--ns ns]` | Generate a Python launch file with parameters and remappings |
| `/ros2-launch` | `/ros2-launch <pkg> <file.launch.py> [arg:=value ...]` or `/ros2-launch <path/to/file.launch.py>` | Run a launch file, stream output, detect startup errors, report which nodes came up |
| `/ros2-run` | `/ros2-run <pkg> <executable> [--remap from:=to] [--param k:=v]` or `/ros2-run <script.py>` | Run a single node standalone by package or direct script path |
| `/ros2-compose` | `/ros2-compose <ClassName> [package_path] [--container-name name]` | Register a C++ node as a composable component and generate container launch |

### Build & Dependencies

| Skill | Usage | Description |
|---|---|---|
| `/ros2-build` | `/ros2-build [packages] [--symlink-install] [--cmake-args ...]` | Build with colcon, detect errors, and suggest fixes |
| `/ros2-add-dep` | `/ros2-add-dep <dependency> [package_path]` | Add a dependency to package.xml and CMakeLists.txt or setup.py |
| `/ros2-rosdep` | `/ros2-rosdep [path] [--update] [--fix] [--check-only]` | Install ROS2 dependencies via rosdep, fix common failures |

### Testing

| Skill | Usage | Description |
|---|---|---|
| `/ros2-create-test` | `/ros2-create-test <node_or_file> [pytest\|gtest] [--unit\|--integration]` | Generate pytest or gtest unit/integration tests |
| `/ros2-launch-test` | `/ros2-launch-test <launch_file> [--topic ...] [--service ...] [--tf ...] [--param ...]` | Generate launch_testing bringup validation tests |

### Debugging & Inspection

| Skill | Usage | Description |
|---|---|---|
| `/ros2-debug-node` | `/ros2-debug-node <node> [--params] [--qos] [--graph]` | Inspect a running node's connections, surface QoS mismatches and missing publishers |
| `/ros2-node-graph` | `/ros2-node-graph [--node <name>] [--topic <name>] [--orphans] [--compact]` | Print the full computation graph as text — nodes, topics, directions, issues |
| `/ros2-check-tf` | `/ros2-check-tf [parent child] [--tree] [--latency] [--all]` | Validate TF tree, detect broken chains and stale transforms |
| `/ros2-diag` | `/ros2-diag [--duration sec] [--filter name] [--errors-only] [--watch]` | Monitor /diagnostics and render a live hardware health dashboard |
| `/ros2-qos` | `/ros2-qos <topic> [--set publisher\|subscriber] [--explain]` | Diagnose QoS mismatches, explain incompatibilities, generate fix code |
| `/ros2-urdf-check` | `/ros2-urdf-check <file.urdf\|file.xacro> [--tree] [--joints] [--meshes]` | Validate URDF/Xacro — check link/joint consistency, missing meshes |

### Configuration & Setup

| Skill | Usage | Description |
|---|---|---|
| `/ros2-param` | `/ros2-param <get\|set\|list\|dump\|load> <node> [param] [value]` | Get, set, list, dump, or load node parameters |
| `/ros2-gen-params` | `/ros2-gen-params <node> [--output file.yaml] [--template] [--namespace ns]` | Generate a parameter YAML file from a running node's current values |
| `/ros2-lifecycle` | `/ros2-lifecycle [node] [configure\|activate\|deactivate\|cleanup\|shutdown] [--all]` | List and control lifecycle-managed nodes |
| `/ros2-remap` | `/ros2-remap <from_topic> <to_topic> [node] [--launch file] [--find]` | Generate remapping syntax for CLI and launch files, find all topic uses |
| `/ros2-nav2-setup` | `/ros2-nav2-setup [diff_drive\|omnidirectional\|ackermann] [path] [--slam]` | Scaffold Nav2 params.yaml, bringup launch, and costmap configuration |
| `/ros2-docker` | `/ros2-docker [path] [--distro humble\|iron\|jazzy] [--multi-stage] [--gpu]` | Generate Dockerfile, entrypoint, .dockerignore, and Docker Compose |

### Topics, Services & Actions

| Skill | Usage | Description |
|---|---|---|
| `/ros2-pub` | `/ros2-pub <topic> <msg_type> [field:value ...] [--rate hz] [--once]` | Publish messages to a topic |
| `/ros2-sub` | `/ros2-sub <topic> [duration_sec] [--count N] [--raw]` | Subscribe to a topic and summarize received data |
| `/ros2-call-service` | `/ros2-call-service <service> [srv_type] [field:value ...]` | Send a service request and display the response |
| `/ros2-send-action` | `/ros2-send-action <action> [type] [field:value ...] [--timeout sec] [--cancel-after sec]` | Send an action goal and monitor feedback until completion |
| `/ros2-monitor-action` | `/ros2-monitor-action <action> [--cancel] [--timeout sec] [--summary]` | Attach to an **already-running** action and stream its feedback |

### Bag Files

| Skill | Usage | Description |
|---|---|---|
| `/ros2-bag` | `/ros2-bag <record\|play\|info> [topics\|bag_path] [options]` | Record topics, play back bags, and inspect bag contents |

---

## Examples

```bash
# Scaffold a Python package
/ros2-create-pkg my_robot python "Mobile robot controller"

# Generate a node with pub/sub
/ros2-create-node image_processor python \
  --pub /processed:sensor_msgs/Image \
  --sub /camera/image:sensor_msgs/Image

# Register a C++ node as a composable component
/ros2-compose my_pkg::ImageProcessor src/my_pkg

# Install all workspace dependencies
/ros2-rosdep --update

# Build specific packages
/ros2-build my_robot my_interfaces --symlink-install

# Inspect the full computation graph
/ros2-node-graph

# Debug a running node
/ros2-debug-node /move_base --qos --params

# Diagnose QoS mismatch on a topic
/ros2-qos /camera/image_raw

# Check TF tree health
/ros2-check-tf --all

# Monitor hardware health dashboard
/ros2-diag --watch

# Validate a URDF file
/ros2-urdf-check src/my_robot/urdf/robot.xacro --meshes

# Generate a parameter YAML from a running node
/ros2-gen-params /move_base --template --output config/move_base_params.yaml

# Generate topic remapping syntax
/ros2-remap /camera/image_raw /robot/camera/image --find

# Set up Nav2 for a differential drive robot
/ros2-nav2-setup diff_drive

# Generate a Dockerfile for the workspace
/ros2-docker --distro humble --multi-stage

# Monitor an in-flight navigation action
/ros2-monitor-action /navigate_to_pose --summary

# Record a 30-second bag
/ros2-bag record /scan /odom /tf --duration 30

# Inspect a bag
/ros2-bag info rosbag2_2024_01_15/
```

---

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- ROS2 (Humble, Iron, or Jazzy) installed and sourced

---

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [templates/skill-template.md](templates/skill-template.md) for the skill authoring template.

---

## License

MIT — see [LICENSE](LICENSE).
