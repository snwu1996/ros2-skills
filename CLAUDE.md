# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Purpose

This is a **ROS2 skills library** for Claude Code — reusable, production-ready skill packages that give AI coding agents deep ROS2 expertise. Each skill is a modular instruction package covering the full ROS2 development lifecycle: from package scaffolding and node generation to building, testing, and runtime inspection.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be used directly inside Claude Code projects.

## Repository Structure

```
ros2-claude-skills/
├── .claude/
│   └── skills/                  # All skills live here
│       ├── ros2-create-pkg/     # Package scaffolding
│       ├── ros2-build/          # Workspace build
│       ├── ros2-add-dep/        # Dependency management
│       ├── ros2-create-node/    # Node generation
│       ├── ros2-create-interface/ # Msg/srv/action interfaces
│       ├── ros2-create-launch/  # Launch file generation
│       ├── ros2-create-test/    # Test generation
│       ├── ros2-launch-test/    # Launch testing
│       ├── ros2-test/           # Run colcon tests + parse results
│       ├── ros2-workspace/      # Scaffold new workspace
│       ├── ros2-clean/          # Clean build/install/log artifacts
│       ├── ros2-param/          # Parameter management
│       ├── ros2-pub/            # Topic publishing
│       ├── ros2-sub/            # Topic subscribing
│       ├── ros2-call-service/   # Service calls
│       ├── ros2-send-action/    # Action goals (send new goal)
│       ├── ros2-monitor-action/ # Action feedback monitoring (in-flight)
│       ├── ros2-debug-node/     # Node inspection & issue detection
│       ├── ros2-node-graph/     # Computation graph visualization
│       ├── ros2-check-tf/       # TF tree validation
│       ├── ros2-diag/           # /diagnostics health dashboard
│       ├── ros2-qos/            # QoS mismatch diagnostics
│       ├── ros2-lifecycle/      # Lifecycle node management
│       ├── ros2-gen-params/     # Parameter YAML generation
│       ├── ros2-remap/          # Topic remapping helper
│       ├── ros2-urdf-check/     # URDF/Xacro validation
│       ├── ros2-compose/        # Composable node setup
│       ├── ros2-docker/         # Dockerfile generation
│       ├── ros2-rosdep/         # rosdep dependency installer
│       ├── ros2-nav2-setup/     # Nav2 configuration scaffold
│       ├── ros2-bag/            # Bag record / play / info
│       ├── ros2-launch/         # Run a launch file
│       ├── ros2-run/            # Run a single node standalone
│       ├── ros2-log/            # View and filter ~/.ros/log/ logs
│       ├── ros2-pkg-info/       # Inspect installed packages
│       ├── ros2-perf/           # CPU/memory/latency profiling
│       ├── ros2-gazebo/         # Launch Gazebo + spawn robot
│       ├── ros2-sim-time/       # Manage use_sim_time
│       └── ros2-domain/         # Manage ROS_DOMAIN_ID
├── templates/
│   └── skill-template.md        # Template for new skills
├── .github/
│   ├── ISSUE_TEMPLATE/          # Bug report, feature request
│   └── pull_request_template.md
├── CLAUDE.md                    # This file
├── CONTRIBUTING.md              # Contribution guide
├── INSTALLATION.md              # Detailed install instructions
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT
└── README.md                    # Overview and quick start
```

## Skill Package Pattern

Each skill follows this structure:
```
.claude/skills/<skill-name>/
└── SKILL.md              # YAML frontmatter + markdown instructions
```

**YAML Frontmatter fields:**
- `name`: kebab-case skill name
- `description`: trigger description for Claude (include usage hint)
- `argument-hint`: argument syntax shown in slash command autocomplete
- `allowed-tools`: list of Claude tools the skill may use

**Template variable:** `$ARGUMENTS` — expands to whatever the user passed after the slash command.

**Dynamic context:** `` !`command` `` — runs a shell command inline when the skill loads (e.g., to detect ROS distro, list packages, etc.)

## Skill Design Principles

1. **Argument-driven** — parse `$ARGUMENTS` to determine behavior, with sensible defaults
2. **Context-aware** — use shell commands to detect workspace state (sourced distro, existing packages, build system)
3. **Idiomatic output** — generated code should match ROS2 Humble/Iron/Jazzy conventions
4. **Fail-safe** — check for existing files/directories before overwriting
5. **Actionable summary** — always end with what was created and next steps

## Git Workflow

```bash
git checkout -b feature/ros2-<skill-name>
# Develop and test skill
git commit -m "feat(skill): add ros2-<skill-name>"
git push origin feature/ros2-<skill-name>
# Create PR to main
```

## Adding a New Skill

1. Copy `templates/skill-template.md` to `.claude/skills/<skill-name>/SKILL.md`
2. Fill in frontmatter: name, description, argument-hint, allowed-tools
3. Write the skill body — parse `$ARGUMENTS`, describe steps, generate output
4. Test by opening Claude Code in a ROS2 workspace and invoking the slash command
5. Update `README.md` skills table
6. Add an entry to `CHANGELOG.md`

## Testing Skills

Skills are tested manually with Claude Code:
1. Open a ROS2 workspace in Claude Code
2. Invoke the skill: `/ros2-<skill-name> <args>`
3. Verify the skill parses arguments correctly
4. Verify generated files are syntactically correct and build successfully

## Key Conventions

- ROS2 target distros: Humble, Iron, Jazzy (prefer Humble as baseline)
- Python nodes: use `rclpy`, `Node` subclass, `main()` entry point
- C++ nodes: use `rclcpp`, `Node` subclass, `rclcpp::spin`
- Package names: `snake_case`
- Node names: `snake_case`
- Topic/service names: `/snake_case` with leading slash

---

**Last Updated:** March 2026
**Version:** v1.3.0
**Skills:** 39 production-ready ROS2 skills
