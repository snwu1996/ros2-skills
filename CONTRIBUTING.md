# Contributing to ros2-claude-skills

Thank you for your interest in contributing! This repository aims to give Claude Code deep, production-ready ROS2 expertise through modular skill packages.

## Ways to Contribute

### 1. Create New Skills

Add skills for ROS2 workflows not yet covered:
- Debug and introspection tools (`/ros2-debug-node`, `/ros2-check-tf`)
- Bag file analysis (`/ros2-analyze-bag`)
- Framework setup (`/ros2-nav2-setup`, `/ros2-moveit-setup`)
- URDF/Xacro tools (`/ros2-urdf-check`, `/ros2-xacro-build`)
- Simulation (`/ros2-gazebo-world`)
- Parameter file generation (`/ros2-gen-params`)

### 2. Improve Existing Skills

- Better argument parsing and defaults
- Additional generated code patterns
- Support for more message/service types
- Edge case handling
- Updated best practices for newer ROS2 distros

### 3. Improve Documentation

- More usage examples in README
- Better argument-hint strings
- Clearer step-by-step instructions in SKILL.md

### 4. Fix Bugs

- Generated code that doesn't compile
- Incorrect CMakeLists.txt patterns
- Wrong package.xml format version
- Shell commands that fail in certain environments

---

## Getting Started

### Prerequisites

- ROS2 installed (Humble, Iron, or Jazzy)
- Claude Code CLI
- Git and GitHub account

### Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/ros2-claude-skills.git
cd ros2-claude-skills
git remote add upstream https://github.com/YOUR_USERNAME/ros2-claude-skills.git
```

### Create a Branch

```bash
git checkout -b feature/ros2-my-new-skill
# Or for improvements:
git checkout -b improvement/ros2-build-error-detection
```

---

## Skill Creation Guidelines

### Required Structure

```
.claude/skills/<skill-name>/
└── SKILL.md      # Required — YAML frontmatter + markdown instructions
```

### SKILL.md Requirements

**YAML Frontmatter (required):**
```yaml
---
name: ros2-skill-name
description: What it does and when to use it. Include usage hint. Usage: /ros2-skill-name <arg> [options]
argument-hint: <required_arg> [optional_arg]
allowed-tools: Read, Write, Edit, Glob, Bash
---
```

**Frontmatter rules:**
- `name`: must match the folder name exactly
- `description`: should include usage syntax at the end (as in existing skills)
- `argument-hint`: shown in autocomplete — make it useful
- `allowed-tools`: only list tools the skill actually needs

**Skill body (required):**
- Parse `$ARGUMENTS` at the top
- List all steps clearly
- Show exact file content to generate (use code blocks)
- End with a summary of what was created and next steps

### Argument Parsing Pattern

```markdown
Parse the arguments from `$ARGUMENTS`:
- **First arg**: required, describe what it is
- **Second arg**: optional, default value if not provided
- **Remaining args**: treated as X
```

### Dynamic Context

Use inline shell commands to detect workspace state:

```markdown
Current ROS2 environment: !`echo $ROS_DISTRO`
Existing packages: !`ls src/ 2>/dev/null || echo "no src/ directory"`
```

### Code Generation Standards

Generated ROS2 code must be:
- Syntactically correct and buildable
- Idiomatic for ROS2 Humble (minimum target)
- Using correct package.xml format 3
- Using `ament_cmake` or `ament_python` as appropriate

---

## Contribution Process

### Step 1: Develop

Follow the skill creation guidelines. See `templates/skill-template.md` for the canonical starting point.

### Step 2: Test

Test your skill manually in a ROS2 workspace:

```bash
# Open Claude Code in a ROS2 workspace
cd ~/ros2_ws
# Invoke your skill
/ros2-my-new-skill test_pkg python
# Verify the generated files are correct
colcon build --packages-select test_pkg
```

**Checklist:**
- [ ] YAML frontmatter is valid
- [ ] Skill parses `$ARGUMENTS` correctly
- [ ] Generated files are syntactically correct
- [ ] Generated files build with `colcon build`
- [ ] Skill handles missing/invalid arguments gracefully
- [ ] Summary at the end is accurate

### Step 3: Submit Pull Request

```bash
git add .claude/skills/ros2-my-new-skill/
git commit -m "feat(skill): add ros2-my-new-skill with [capabilities]"
git push origin feature/ros2-my-new-skill
```

**PR title format:**
- `feat(skill): add ros2-<name> for <purpose>`
- `fix(ros2-build): handle missing colcon output`
- `docs(readme): add examples for ros2-create-node`
- `improvement(ros2-create-pkg): add Python test scaffold`

**PR description must include:**
- What: what does this add/change/fix?
- Why: why is this valuable for ROS2 developers?
- Testing: how was it tested (ROS2 distro, workspace type)?

---

## Quality Standards

### Skill Quality Checklist

**SKILL.md:**
- [ ] Valid YAML frontmatter (name, description, argument-hint, allowed-tools)
- [ ] Argument parsing section clear
- [ ] All generated file content shown explicitly
- [ ] Next steps section at the end

**Generated Code:**
- [ ] Builds successfully with `colcon build`
- [ ] Follows ROS2 naming conventions
- [ ] Uses correct package.xml format 3
- [ ] No hardcoded paths

**Documentation:**
- [ ] README.md skills table updated
- [ ] CHANGELOG.md entry added

---

## What NOT to Contribute

We will not accept:
- Skills that require non-standard ROS2 packages without clear documentation
- Generated code that doesn't build
- Skills that duplicate existing functionality without clear improvement
- Skills for deprecated ROS2 versions (ROS2 Foxy, Galactic)

---

## Questions?

- **Bug Reports:** Use the bug report issue template
- **New Skill Ideas:** Use the feature request issue template
- **General Discussion:** Open a GitHub Discussion

---

**Happy contributing!**
