---
name: ros2-param
description: Get, set, list, or dump ROS2 node parameters. Usage: /ros2-param get <node> [param] | set <node> <param> <value> | list <node> | dump <node> | load <node> <yaml_file>
argument-hint: <get|set|list|dump|load> <node_name> [param_name] [value]
allowed-tools: Bash, Read, Write
---

# ROS2 Parameter Tool

Get, set, list, or dump ROS2 node parameters. Arguments: `$ARGUMENTS`

Parse arguments — first argument is the subcommand:
- `get <node> [param]` — get one param or all params for a node
- `set <node> <param> <value>` — set a parameter on a running node
- `list [node]` — list all parameters for a node (or all nodes)
- `dump <node> [output_file]` — dump all params to YAML (optionally save to file)
- `load <node> <yaml_file>` — load parameters from a YAML file into a running node

If no subcommand is given, default to `list` behavior.

## Steps

### `list [node]`

1. If node given:
   ```bash
   ros2 param list <node>
   ```
2. If no node given, list all nodes first then get params for each:
   ```bash
   ros2 node list
   ros2 param list  # lists all params across all nodes
   ```
3. Group output by node, filter out internal `use_sim_time` and `qos_*` params unless `--all` flag given.

---

### `get <node> [param]`

1. Verify node exists:
   ```bash
   ros2 node list
   ```
2. If specific param given:
   ```bash
   ros2 param get <node> <param>
   ```
   Display the value with its type clearly labeled.

3. If no param given, get all params:
   ```bash
   ros2 param list <node>
   ```
   Then for each parameter:
   ```bash
   ros2 param get <node> <param_name>
   ```
   Present as a clean table:
   ```
   Node: /my_node
   ┌─────────────────────┬──────────┬─────────────────┐
   │ Parameter           │ Type     │ Value           │
   ├─────────────────────┼──────────┼─────────────────┤
   │ max_velocity        │ float64  │ 1.5             │
   │ enable_logging      │ bool     │ true            │
   │ robot_name          │ string   │ "my_robot"      │
   └─────────────────────┴──────────┴─────────────────┘
   ```

---

### `set <node> <param> <value>`

1. First **get the current value** and type:
   ```bash
   ros2 param get <node> <param>
   ```
   Show the current value before changing.

2. **Infer the type** from the current value. Cast the new value to match:
   - If current is `bool`: accept `true/false/1/0/yes/no`
   - If current is `int`: parse as integer
   - If current is `float`/`double`: parse as float
   - If current is `string`: use as-is

3. Run the set command:
   ```bash
   ros2 param set <node> <param> <value>
   ```

4. **Verify the change**:
   ```bash
   ros2 param get <node> <param>
   ```
   Confirm old → new value transition.

5. **Warn** that parameter changes on a running node are ephemeral — they won't persist after restart. Suggest saving with `dump` or adding to a YAML config file.

---

### `dump <node> [output_file]`

1. ```bash
   ros2 param dump <node>
   ```
2. If output_file given, write the YAML to that file using the Write tool.
3. Otherwise display the YAML output and suggest saving it.
4. Note which parameters are at non-default values (if detectable from context).

---

### `load <node> <yaml_file>`

1. Read the YAML file to verify it exists and is valid.
2. Show the user what parameters will be set before applying.
3. ```bash
   ros2 param load <node> <yaml_file>
   ```
4. Verify a sample of the params were applied with `ros2 param get`.

---

## Error handling

- **Node not found**: show `ros2 node list` output and suggest close matches
- **Param not found**: show `ros2 param list <node>` and suggest close matches
- **Read-only param**: report that the parameter is not dynamically settable; suggest restarting the node with the parameter in a YAML file or as a launch argument
- **Type mismatch**: show the expected type and an example of the correct value format
