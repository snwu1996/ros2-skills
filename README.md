# ros2-claude-skills

**18 production-ready Claude Code skills for ROS2 development** — covering the full robot software lifecycle from package scaffolding and node generation to runtime debugging, TF inspection, bag recording, and lifecycle management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-18-brightgreen.svg)](#skills)
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

### User-level (skills available in all your Claude Code sessions)

```bash
git clone https://github.com/YOUR_USERNAME/ros2-claude-skills.git ~/ros2-claude-skills
mkdir -p ~/.claude/skills
cp -r ~/ros2-claude-skills/.claude/skills/* ~/.claude/skills/
```

> Skills in `.claude/skills/` inside a project directory take priority over user-level skills.

---

## Skills

### Code Generation

| Skill | Usage | Description |
|---|---|---|
| `/ros2-create-pkg` | `/ros2-create-pkg <name> [cmake\|python] [desc]` | Scaffold a ROS2 package with package.xml, CMakeLists.txt or setup.py, and directory structure |
| `/ros2-create-node` | `/ros2-create-node <name> [python\|cpp] [--pub topic:type] [--sub topic:type] [--srv name:type] [--action name:type]` | Generate a Python or C++ node with publishers, subscribers, services, and actions |
| `/ros2-create-interface` | `/ros2-create-interface <Name> [msg\|srv\|action] [field type ...]` | Create .msg, .srv, or .action interface files and update CMakeLists.txt |
| `/ros2-create-launch` | `/ros2-create-launch <name> [node:pkg ...] [--param k:v] [--ns ns]` | Generate a Python launch file with parameters, remappings, and namespaces |

### Build & Dependencies

| Skill | Usage | Description |
|---|---|---|
| `/ros2-build` | `/ros2-build [packages] [--symlink-install] [--cmake-args ...]` | Build workspace with colcon, detect errors, and suggest targeted fixes |
| `/ros2-add-dep` | `/ros2-add-dep <dependency> [package_path]` | Add a dependency to package.xml and CMakeLists.txt or setup.py |

### Testing

| Skill | Usage | Description |
|---|---|---|
| `/ros2-create-test` | `/ros2-create-test <node_or_file> [pytest\|gtest] [--unit\|--integration]` | Generate pytest or gtest unit/integration tests |
| `/ros2-launch-test` | `/ros2-launch-test <launch_file> [--topic ...] [--service ...] [--tf ...] [--param ...]` | Generate launch_testing tests for full node bringup validation |

### Runtime Inspection & Debugging

| Skill | Usage | Description |
|---|---|---|
| `/ros2-debug-node` | `/ros2-debug-node <node> [--params] [--qos] [--graph]` | Inspect a running node's connections and surface QoS mismatches, missing publishers, stale topics |
| `/ros2-check-tf` | `/ros2-check-tf [parent child] [--tree] [--latency] [--all]` | Validate TF tree, detect broken chains, stale transforms, and frame conflicts |
| `/ros2-lifecycle` | `/ros2-lifecycle [node] [configure\|activate\|deactivate\|cleanup\|shutdown] [--all]` | List and control lifecycle-managed nodes |
| `/ros2-param` | `/ros2-param <get\|set\|list\|dump\|load> <node> [param] [value]` | Get, set, list, dump, or load ROS2 node parameters |

### Topics, Services & Actions

| Skill | Usage | Description |
|---|---|---|
| `/ros2-pub` | `/ros2-pub <topic> <msg_type> [field:value ...] [--rate hz] [--once]` | Publish messages to a topic |
| `/ros2-sub` | `/ros2-sub <topic> [duration_sec] [--count N] [--raw]` | Subscribe to a topic and summarize received data |
| `/ros2-call-service` | `/ros2-call-service <service> [srv_type] [field:value ...]` | Send a service request and display the response |
| `/ros2-send-action` | `/ros2-send-action <action> [type] [field:value ...] [--timeout sec] [--cancel-after sec]` | Send an action goal and monitor feedback until completion |
| `/ros2-monitor-action` | `/ros2-monitor-action <action> [--cancel] [--timeout sec] [--summary]` | Attach to an **in-progress** action and stream its feedback without sending a new goal |

### Bag Files

| Skill | Usage | Description |
|---|---|---|
| `/ros2-bag` | `/ros2-bag record [topics] [--duration sec]` | Record, play back, and inspect ROS2 bag files |

---

## Examples

```bash
# Scaffold a Python package
/ros2-create-pkg my_robot python "Mobile robot controller"

# Generate a node with pub/sub
/ros2-create-node image_processor python \
  --pub /processed:sensor_msgs/Image \
  --sub /camera/image:sensor_msgs/Image

# Build specific packages
/ros2-build my_robot my_interfaces --symlink-install

# Add a dependency
/ros2-add-dep rclcpp

# Create a custom service
/ros2-create-interface SetMode srv string mode bool success string message

# Generate a launch file with namespace
/ros2-create-launch bringup robot_node:my_robot --param use_sim_time:true --ns /robot1

# Debug a running node
/ros2-debug-node /move_base --qos --params

# Check TF tree health
/ros2-check-tf --all

# Echo a specific transform
/ros2-check-tf map base_link

# Monitor a nav goal already in flight
/ros2-monitor-action /navigate_to_pose --summary

# Manage a lifecycle driver
/ros2-lifecycle /camera_driver activate

# Record a bag for 30 seconds
/ros2-bag record /scan /odom /tf --duration 30

# Inspect a bag file
/ros2-bag info rosbag2_2024_01_15/

# Subscribe to a topic for 5 seconds
/ros2-sub /scan 5

# Call a service
/ros2-call-service /set_mode std_srvs/srv/SetBool data:true
```

---

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- ROS2 (Humble, Iron, or Jazzy) installed and sourced in your shell

---

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Each skill lives in `.claude/skills/<skill-name>/SKILL.md` — a YAML frontmatter header followed by markdown instructions that Claude Code executes when you invoke the slash command.

---

## License

MIT — see [LICENSE](LICENSE) for details.
