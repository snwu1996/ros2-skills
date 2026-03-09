---
name: ros2-test
description: Run ROS2 tests for one or more packages using colcon test. Parse pytest and gtest results, show pass/fail/error summary with failure details. Usage: /ros2-test [packages...] [--pytest] [--gtest] [--rerun-failed] [--verbose]
argument-hint: [package_name ...] [--rerun-failed] [--verbose] [--pytest] [--gtest]
allowed-tools: Bash, Glob, Read
---

# ROS2 Test Runner

Run colcon tests and parse the results. Arguments: `$ARGUMENTS`

Parse arguments:
- **packages**: optional list of package names to test (default: all packages)
- **--rerun-failed**: only re-run tests that failed in the last run
- **--verbose**: stream full test output (default: summary only)
- **--pytest**: only run pytest tests
- **--gtest**: only run gtest/ament_cmake tests

## Steps

1. **Detect workspace root** — find `build/` and `install/`:
   ```bash
   ls build/ install/ 2>/dev/null
   ```
   If not found, stop: must be run from the workspace root.

2. **Check packages are built** — if specific packages given:
   ```bash
   ls build/<package>/ 2>/dev/null
   ```
   If any package is not built, warn and offer to build first: `/ros2-build <package>`

3. **Run the tests**:

   All packages:
   ```bash
   colcon test --event-handlers console_cohesion+
   ```

   Specific packages:
   ```bash
   colcon test --packages-select <pkg1> <pkg2> --event-handlers console_cohesion+
   ```

   Rerun failed only:
   ```bash
   colcon test --packages-select $(colcon test-result --verbose 2>/dev/null | grep "^Failed" | awk '{print $2}' | sort -u)
   ```

   With pytest args:
   ```bash
   colcon test --packages-select <pkg> --pytest-args -v
   ```

4. **Collect test results**:
   ```bash
   colcon test-result --verbose 2>/dev/null
   ```
   Also scan individual result files:
   ```bash
   find build/ -name "*.xml" -path "*/test_results/*" 2>/dev/null
   ```

5. **Parse and display results** — do NOT dump raw XML. Format as:

   ```
   Test Results
   ══════════════════════════════════════════════════════
   my_package           8 passed   0 failed   0 errors  ✅
   my_interfaces        3 passed   0 failed   0 errors  ✅
   my_robot_controller  5 passed   2 failed   1 error   ❌
   ══════════════════════════════════════════════════════
   Total: 16 passed, 2 failed, 1 error  (3 packages)
   ```

6. **For each failed test**, show details:
   ```
   ❌ my_robot_controller — FAILURES (2)

   FAIL: test_velocity_limits (test_controller.py:42)
     AssertionError: max velocity exceeded
     Expected: cmd_vel.linear.x <= 0.5
     Got:      cmd_vel.linear.x = 0.73

   FAIL: test_emergency_stop (test_controller.py:78)
     AssertionError: node did not stop within timeout
     Timeout: 1.0s
     Node state: active

   ERROR: test_hardware_interface (test_hardware.py:12)
     ImportError: No module named 'hardware_interface_mock'
   ```

7. **Parse gtest output** from XML:
   ```bash
   find build/ -name "*.xml" -path "*/test_results/*" | xargs grep -l "testcase" 2>/dev/null
   ```
   Extract `<failure>` and `<error>` nodes and format similarly.

8. **If --verbose**, also show full stdout for each failed test:
   ```bash
   find build/<package>/test_results/ -name "*.txt" 2>/dev/null | xargs cat
   ```

9. **Coverage report** — if pytest-cov was used:
   ```bash
   find build/ -name "coverage.xml" 2>/dev/null | head -1 | xargs cat 2>/dev/null
   ```
   Show per-file coverage summary if available.

10. **Summary and next steps**:

    All passed:
    ```
    ✅ All 16 tests passed across 3 packages.
    ```

    Failures:
    ```
    ❌ 3 failures detected.

    Quick fixes:
      ImportError  → /ros2-add-dep hardware_interface_mock
      AssertionError on velocity → check controller parameter: max_linear_vel
      Timeout failure → check if node initializes correctly: /ros2-debug-node /robot_controller

    Re-run failed tests only:
      /ros2-test my_robot_controller --rerun-failed

    Full output:
      /ros2-test my_robot_controller --verbose
    ```
