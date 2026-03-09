---
name: ros2-create-test
description: Generate unit or integration tests for a ROS2 node using pytest (Python) or gtest (C++). Usage: /ros2-create-test <node_or_file> [pytest|gtest] [--unit|--integration]
argument-hint: <node_name_or_file> [pytest|gtest] [--unit] [--integration]
allowed-tools: Read, Write, Edit, Glob, Bash, Grep
---

# ROS2 Test Generator

Generate tests for a ROS2 node or module. Arguments: `$ARGUMENTS`

Parse arguments:
- **target**: node name or source file path to test
- **framework**: `pytest` (default for Python) or `gtest` (default for C++)
- **--unit**: generate unit tests (isolated, mock dependencies)
- **--integration**: generate integration tests (spin actual node, check topics/services)
- If neither flag given, generate both

## Steps

1. **Read the target file** to understand:
   - Node class name, publishers, subscribers, services, actions
   - Parameters declared
   - Public methods and callbacks

2. **Determine test framework** from argument or from package build type (ament_python → pytest, ament_cmake → gtest).

3. **Create `test/` directory** if it doesn't exist.

---

### pytest (Python)

Generate `test/test_<node_name>.py`:

```python
import pytest
import rclpy
from rclpy.node import Node
# import node under test

@pytest.fixture(autouse=True)
def init_rclpy():
    rclpy.init()
    yield
    rclpy.shutdown()


class TestUnitNodeName:
    """Unit tests — no spinning required."""

    def test_node_creation(self):
        node = MyNode()
        assert node.get_name() == 'expected_name'
        node.destroy_node()

    def test_parameter_defaults(self):
        node = MyNode()
        assert node.get_parameter('param_name').value == expected_default
        node.destroy_node()

    # test each callback method with mock messages


class TestIntegrationNodeName:
    """Integration tests — publish/subscribe across nodes."""

    def test_publishes_on_timer(self):
        node = MyNode()
        received = []

        helper = rclpy.create_node('test_helper')
        sub = helper.create_subscription(
            MsgType, '/topic', lambda msg: received.append(msg), 10
        )

        # spin both nodes briefly
        executor = rclpy.executors.SingleThreadedExecutor()
        executor.add_node(node)
        executor.add_node(helper)
        executor.spin_once(timeout_sec=0.1)
        executor.spin_once(timeout_sec=0.5)

        assert len(received) > 0
        node.destroy_node()
        helper.destroy_node()
```

Update `package.xml`:
```xml
<test_depend>pytest</test_depend>
<test_depend>ament_pytest</test_depend>
```

Update `CMakeLists.txt` or check `setup.cfg` has:
```ini
[tool:pytest]
junit_suite_name = <pkg>
```

For `ament_cmake` Python tests, add:
```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(<pkg>_test test/)
endif()
```

---

### gtest (C++)

Generate `test/test_<node_name>.cpp`:

```cpp
#include <gtest/gtest.h>
#include <rclcpp/rclcpp.hpp>
// include node header

class TestNodeName : public ::testing::Test {
protected:
    void SetUp() override {
        rclcpp::init(0, nullptr);
        node_ = std::make_shared<MyNode>();
    }

    void TearDown() override {
        node_.reset();
        rclcpp::shutdown();
    }

    std::shared_ptr<MyNode> node_;
};

TEST_F(TestNodeName, NodeCreation) {
    ASSERT_NE(node_, nullptr);
    EXPECT_EQ(node_->get_name(), std::string("expected_name"));
}

TEST_F(TestNodeName, ParameterDefaults) {
    auto param = node_->get_parameter("param_name");
    EXPECT_EQ(param.as_double(), expected_value);
}

// add tests for each subscriber callback and service

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

Add to `CMakeLists.txt`:
```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_<node_name> test/test_<node_name>.cpp)
  target_link_libraries(test_<node_name> <node_lib>)
  ament_target_dependencies(test_<node_name> rclcpp <other_deps>)
endif()
```

Add to `package.xml`:
```xml
<test_depend>ament_cmake_gtest</test_depend>
```

---

4. **Generate meaningful test cases** based on what was read from the node:
   - One test per subscriber callback (send a message, verify side effects)
   - One test per service (call it, verify response)
   - One test per parameter (verify default, verify behavior when changed)
   - One happy-path integration test per publisher

5. Print how to run:
   ```bash
   colcon test --packages-select <pkg>
   colcon test-result --verbose
   ```
