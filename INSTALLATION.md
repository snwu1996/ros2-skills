# Installation Guide

Complete installation guide for ros2-claude-skills — 18 ROS2 skills for Claude Code.

## Prerequisites

- [Claude Code](https://claude.ai/claude-code) CLI installed
- ROS2 (Humble, Iron, or Jazzy) installed and sourced in your shell

---

## Option 1: Project-level (Recommended)

Skills are scoped to a specific ROS2 workspace. Activate automatically when Claude Code is opened in that directory.

```bash
cd ~/ros2_ws

# Clone the skills repo
git clone git@github.com:snwu1996/ros2-skills.git .ros2-skills

# Copy skills into the project's Claude config
mkdir -p .claude/skills
cp -r .ros2-skills/.claude/skills/* .claude/skills/
```

Open Claude Code in `~/ros2_ws` — skills are immediately available.

---

## Option 2: User-level (Global)

Skills are available in every Claude Code session, regardless of which directory you open.

```bash
# Clone anywhere
git clone git@github.com:snwu1996/ros2-skills.git ~/ros2-claude-skills

# Copy into user-level Claude config
mkdir -p ~/.claude/skills
cp -r ~/ros2-claude-skills/.claude/skills/* ~/.claude/skills/
```

---

## Option 3: Symlink (Stay Up to Date)

Instead of copying, symlink each skill so `git pull` updates them automatically.

```bash
git clone git@github.com:snwu1996/ros2-skills.git ~/ros2-claude-skills
mkdir -p ~/.claude/skills

for skill_dir in ~/ros2-claude-skills/.claude/skills/*/; do
    skill_name=$(basename "$skill_dir")
    ln -sf "$skill_dir" ~/.claude/skills/"$skill_name"
done
```

---

## Verify Installation

Open Claude Code in a directory where the skills are installed and type `/ros2-` — you should see all 18 skills in the autocomplete dropdown.

Or test a skill directly (no ROS2 needed for this check):

```
/ros2-create-pkg test_pkg python
```

Claude should scaffold a Python ROS2 package.

---

## Install Individual Skills

If you only want specific skills, copy just those directories:

```bash
# Example: only install the debugging and inspection skills
mkdir -p ~/.claude/skills
cp -r ~/ros2-claude-skills/.claude/skills/ros2-debug-node ~/.claude/skills/
cp -r ~/ros2-claude-skills/.claude/skills/ros2-check-tf ~/.claude/skills/
cp -r ~/ros2-claude-skills/.claude/skills/ros2-lifecycle ~/.claude/skills/
```

---

## Updating

### If you copied the files:

```bash
cd ~/ros2-claude-skills
git pull
cp -r .claude/skills/* ~/.claude/skills/
```

### If you used symlinks:

```bash
cd ~/ros2-claude-skills
git pull
# Symlinks automatically point to updated files
```

---

## Uninstalling

### Remove all skills

```bash
# User-level
rm -rf ~/.claude/skills/ros2-*

# Project-level
rm -rf ~/ros2_ws/.claude/skills/ros2-*
```

### Remove a specific skill

```bash
rm -rf ~/.claude/skills/ros2-debug-node
```

---

## Skill Locations Reference

| Scope | Location | When active |
|---|---|---|
| User-level | `~/.claude/skills/` | All Claude Code sessions |
| Project-level | `<project>/.claude/skills/` | When Claude Code is opened in `<project>` |

Project-level skills take priority over user-level skills when both exist.

---

## Troubleshooting

**Skills not appearing in autocomplete:**
- Make sure the SKILL.md file exists: `ls ~/.claude/skills/ros2-build/SKILL.md`
- Restart Claude Code after copying skills
- Check that the skill directory name matches the `name:` field in the YAML frontmatter

**Skill runs but ROS2 commands fail:**
- Ensure your ROS2 environment is sourced: `echo $ROS_DISTRO`
- Source it before opening Claude Code: `source /opt/ros/humble/setup.bash`

**"Command not found: ros2":**
- Source your ROS2 setup: `source /opt/ros/humble/setup.bash`
- Or add it to your shell profile: `echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc`
