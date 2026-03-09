---
name: ros2-your-skill-name
description: One-line description of what this skill does and when to use it. Usage: /ros2-your-skill-name <required_arg> [optional_arg]
argument-hint: <required_arg> [optional_arg] [--flag]
allowed-tools: Bash, Read, Write, Edit, Glob
---

# ROS2 Your Skill Title

Brief description of what this skill does. Arguments: `$ARGUMENTS`

Parse arguments:
- **first_arg**: first argument — what it represents (e.g. node name). Prepend `/` if missing.
- **second_arg**: second argument — optional, default: `default_value`
- **--flag**: optional flag — describe what it changes

## Steps

1. **Validate inputs** — check that required arguments are present and well-formed:
   ```bash
   # Example: verify a node exists
   ros2 node list
   ```
   If validation fails, show a helpful error and stop.

2. **Detect context** — gather workspace/environment information needed:
   ```bash
   # Example: check ROS distro
   echo $ROS_DISTRO
   # Example: list existing packages
   ls src/ 2>/dev/null
   ```

3. **Main action** — describe the primary work this skill does:
   ```bash
   # Shell command example
   ros2 <command> <args>
   ```
   Or for code generation, write files with correct ROS2 content.

4. **Verify result** — confirm the action succeeded:
   ```bash
   # Example: check the output
   ros2 node info <node>
   ```

5. **Summary** — always end with a clear summary:
   ```
   ✅ Done: <what was accomplished>

   Next steps:
   - <suggested follow-up command or action>
   - <another suggestion>
   ```

## Edge Cases

- If `<condition>`, do `<alternative behavior>`
- If no arguments given, `<default behavior>`
- If `<error condition>`, report clearly and suggest a fix

## Related Skills

- `/ros2-related-skill` — use when `<scenario>`
- `/ros2-another-skill` — use when `<scenario>`
