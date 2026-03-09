---
name: ros2-create-node
description: Generate a ROS2 node (Python or C++) with configurable publishers, subscribers, services, and actions. Usage: /ros2-create-node <node_name> [python|cpp] [--pub topic:type] [--sub topic:type] [--srv name:type] [--action name:type]
argument-hint: <node_name> [python|cpp] [--pub topic:MsgType] [--sub topic:MsgType] [--srv name:SrvType] [--action name:ActionType]
allowed-tools: Read, Write, Edit, Glob, Bash
---

# ROS2 Node Generator

Generate a complete, idiomatic ROS2 node. Arguments: `$ARGUMENTS`

Parse the arguments:
- **node_name**: first argument (snake_case)
- **language**: `python` or `cpp` (default: `python`)
- **--pub topic:MsgType**: add a publisher (can repeat)
- **--sub topic:MsgType**: add a subscriber (can repeat)
- **--srv name:SrvType**: add a service server (can repeat)
- **--action name:ActionType**: add an action server (can repeat)
- **--timer hz**: add a timer callback at given frequency (default: 1.0 if publishers exist)

If no flags are given, generate a minimal skeleton node.

## Steps

1. **Detect or confirm** the target package — look for `package.xml` in the current directory or ask if ambiguous.

2. **Determine output path**:
   - Python: `<pkg>/<node_name>.py` (or `<pkg>/nodes/<node_name>.py`)
   - C++: `src/<node_name>.cpp`

3. **Generate the node file** following these patterns:

### Python node template
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# imports for each msg/srv/action type

class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')
        # declare and get parameters
        # create publishers
        # create subscribers with callbacks
        # create service servers with callbacks
        # create action servers with callbacks
        # create timer if needed

    # callback methods

def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### C++ node template
```cpp
#include <rclcpp/rclcpp.hpp>
// includes for each msg/srv/action type

class <ClassName> : public rclcpp::Node {
public:
    <ClassName>() : Node("<node_name>") {
        // declare parameters
        // create publishers, subscribers, services, actions, timers
    }

private:
    // callback methods
    // member variables for pubs/subs/etc
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ClassName>());
    rclcpp::shutdown();
    return 0;
}
```

4. **Apply best practices**:
   - Use `self.declare_parameter` / `this->declare_parameter` for any configurable values
   - Use `RCLCPP_INFO` / `self.get_logger().info()` for logging
   - Subscriber callbacks should be `const&` in C++ and handle exceptions gracefully in Python
   - Action servers should handle cancel requests
   - Use `qos_profile_sensor_data` for high-frequency sensor topics

5. **Update build files**:
   - **Python**: add entry point to `setup.py`:
     ```python
     '<node_name> = <pkg>.<node_name>:main'
     ```
   - **C++**: add to `CMakeLists.txt`:
     ```cmake
     add_executable(<node_name> src/<node_name>.cpp)
     ament_target_dependencies(<node_name> rclcpp <msg_deps>)
     install(TARGETS <node_name> DESTINATION lib/${PROJECT_NAME})
     ```

6. **Update `package.xml`** — add any missing message/service/action package dependencies.

7. Print a summary of what was generated and how to run it:
   ```bash
   colcon build --packages-select <pkg> && source install/setup.bash
   ros2 run <pkg> <node_name>
   ```
