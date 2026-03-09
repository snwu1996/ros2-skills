---
name: ros2-call-service
description: Send a ROS2 service request and display the response. Usage: /ros2-call-service <service> [srv_type] [field:value ...]
argument-hint: <service_name> [srv_type_or_auto] [field:value ...]
allowed-tools: Bash
---

# ROS2 Service Caller

Send a request to a ROS2 service and display the response. Arguments: `$ARGUMENTS`

Parse arguments:
- **service**: first argument — service name (e.g. `/set_bool`, `robot/reset`). Prepend `/` if missing.
- **srv_type**: second argument — full type like `std_srvs/srv/SetBool`, or `auto` to detect
- **field:value pairs**: request fields as `field:value` or YAML `{field: value}` pairs

## Steps

1. **List available services** and verify the service exists:
   ```bash
   ros2 service list
   ```
   If not found, show the full service list and any close matches. Stop.

2. **Get the service type** if not provided or `auto`:
   ```bash
   ros2 service type <service>
   ```

3. **Show the request/response interface**:
   ```bash
   ros2 interface show <srv_type>
   ```
   Display this to the user so they can see the available fields and types.

4. **Build the request YAML** from the provided field:value pairs:
   - Parse `field:value` pairs into a YAML dict
   - If no fields provided, use `{}` for empty request types (e.g. `Trigger`)
   - Validate field names against the interface definition; warn on unknown fields

   Common service patterns:
   | Service type | Typical request |
   |---|---|
   | `std_srvs/srv/Trigger` | `{}` (no fields) |
   | `std_srvs/srv/SetBool` | `{data: true}` |
   | `std_srvs/srv/Empty` | `{}` |
   | `rcl_interfaces/srv/SetParameters` | complex — ask user for values |

5. **Display the command** before running:
   ```bash
   ros2 service call <service> <srv_type> '<yaml_dict>'
   ```

6. **Run the call** with a timeout:
   ```bash
   timeout 10 ros2 service call <service> <srv_type> '<yaml_dict>'
   ```

7. **Parse and display the response** clearly:
   - Show `success: true/false` prominently if present
   - Show `message` field if present
   - Format nested fields with indentation
   - If the call timed out, diagnose: check if the service server node is alive with `ros2 node list`

8. **On error**, provide targeted help:
   - Service unavailable → check which node serves it: `ros2 service info <service>`
   - Wrong field type → show interface definition again with types highlighted
   - Timeout → suggest checking node with `ros2 node info <node>`
