---
name: ros2-launch-test
description: Generate a ROS2 launch test that spins up nodes via a launch file and validates their runtime behavior (topics, services, TF, parameters). Usage: /ros2-launch-test <launch_file> [checks...]
argument-hint: <launch_file_or_pkg> [--topic /name:MsgType] [--service /name:SrvType] [--param node:key:value] [--tf parent:child]
allowed-tools: Read, Write, Edit, Glob, Bash, Grep
---

# ROS2 Launch Test Generator

Generate an `ament_ros2launch` / `launch_testing` test. Arguments: `$ARGUMENTS`

Parse arguments:
- **launch_file**: path to `.launch.py` or `package::launch_file.launch.py`
- **--topic /name:MsgType**: verify this topic publishes within timeout
- **--service /name:SrvType**: verify this service is advertised and callable
- **--param node_name:key:expected_value**: verify node has parameter with value
- **--tf parent:child**: verify TF frame exists
- **--timeout seconds**: overall test timeout (default: 10)

## Steps

1. **Read the launch file** to understand which nodes are launched, their names, packages, and parameters.

2. **Create `test/` directory** if needed.

3. **Generate `test/test_<name>.py`** using `launch_testing`:

```python
import unittest
import launch
import launch_ros
import launch_testing
import launch_testing.actions
import launch_testing.markers
import pytest
import rclpy

# --- Launch description to test ---
@pytest.mark.launch_test
def generate_test_description():
    # Include the launch file under test
    launch_file = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            '<path_to_launch_file>'
        ),
        launch_arguments={'arg': 'value'}.items(),
    )

    return launch.LaunchDescription([
        launch_file,
        # Required: signal that the system is ready for tests
        launch_testing.actions.ReadyToTest(),
    ]), {
        # Optionally expose launched processes for inspection
    }


# --- Test class ---
class TestLaunchSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = rclpy.create_node('test_launch_validator')

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_topics_advertised(self):
        """Verify expected topics appear within timeout."""
        import time
        timeout = 10.0
        start = time.time()
        topic_names = []
        while time.time() - start < timeout:
            topic_names = [t for t, _ in self.node.get_topic_names_and_types()]
            if '/expected_topic' in topic_names:
                break
            rclpy.spin_once(self.node, timeout_sec=0.1)
        self.assertIn('/expected_topic', topic_names)

    def test_topic_publishes(self):
        """Verify a topic receives messages within timeout."""
        from <msg_pkg>.msg import <MsgType>
        import threading

        received = []
        sub = self.node.create_subscription(
            <MsgType>, '/topic_name',
            lambda msg: received.append(msg), 10
        )

        end_time = self.node.get_clock().now() + rclpy.duration.Duration(seconds=5.0)
        while self.node.get_clock().now() < end_time and not received:
            rclpy.spin_once(self.node, timeout_sec=0.1)

        self.assertGreater(len(received), 0, "No messages received on /topic_name")
        self.node.destroy_subscription(sub)

    def test_service_available(self):
        """Verify a service is advertised."""
        from <srv_pkg>.srv import <SrvType>
        client = self.node.create_client(<SrvType>, '/service_name')
        available = client.wait_for_service(timeout_sec=5.0)
        self.assertTrue(available, "Service /service_name not available")
        self.node.destroy_client(client)

    def test_node_parameters(self):
        """Verify node parameters have expected values."""
        import subprocess, json
        result = subprocess.run(
            ['ros2', 'param', 'get', '/node_name', 'param_key'],
            capture_output=True, text=True, timeout=5
        )
        self.assertIn('expected_value', result.stdout)
```

4. **Customize the template** based on the arguments and the launch file content:
   - Add one `test_topic_*` test per `--topic` argument
   - Add one `test_service_*` test per `--service` argument
   - Add one `test_parameter_*` test per `--param` argument
   - For `--tf`, add a TF listener test

5. **Update `CMakeLists.txt`** (for ament_cmake packages):
```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_ros REQUIRED)
  find_package(launch_testing_ament_cmake REQUIRED)
  add_launch_test(test/test_<name>.py)
endif()
```

   **Or for Python packages**, add to `setup.py`:
```python
tests_require=['pytest'],
```
And ensure `ament_cmake_python` or `ament_pytest` is configured.

6. **Update `package.xml`**:
```xml
<test_depend>launch_testing</test_depend>
<test_depend>launch_testing_ament_cmake</test_depend>
<test_depend>launch_testing_ros</test_depend>
```

7. Print how to run and debug:
```bash
# Run via colcon
colcon test --packages-select <pkg>
colcon test-result --verbose

# Run directly for debugging
python3 -m pytest test/test_<name>.py -s -v

# With launch_testing directly
launch_test test/test_<name>.py
```
