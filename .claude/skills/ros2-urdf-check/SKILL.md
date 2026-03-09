---
name: ros2-urdf-check
description: Validate a URDF or Xacro file — parse XML, check joint/link consistency, detect missing meshes, display the link tree, and flag common errors. Usage: /ros2-urdf-check <urdf_or_xacro_file> [--tree] [--joints] [--meshes]
argument-hint: <file.urdf|file.xacro> [--tree] [--joints] [--meshes]
allowed-tools: Bash, Read, Glob
---

# ROS2 URDF/Xacro Checker

Validate a URDF or Xacro robot description file. Arguments: `$ARGUMENTS`

Parse arguments:
- **file**: first argument — path to `.urdf` or `.xacro` file
- **--tree**: display the full link tree (default: always shown)
- **--joints**: show detailed joint info (type, limits, axis)
- **--meshes**: check that all referenced mesh files exist
- If no arguments given, search for URDF/Xacro files in the current directory

## Steps

1. **Find the file** — if no path given, search:
   ```bash
   find . -name "*.urdf" -o -name "*.xacro" | head -20
   ```
   If multiple found, list them and ask which to check.

2. **If Xacro file**, process it first:
   ```bash
   ros2 run xacro xacro <file.xacro> -o /tmp/robot_processed.urdf
   ```
   If this fails, show the xacro error (usually a missing include or undefined property) and stop.
   Work with `/tmp/robot_processed.urdf` for all subsequent steps.

3. **Validate with check_urdf**:
   ```bash
   check_urdf <file.urdf>
   ```
   If `check_urdf` is not installed:
   ```bash
   ros2 run urdfdom check_urdf <file.urdf>
   ```
   Display any errors directly — these are parse/structural errors that must be fixed first.

4. **Parse the URDF XML** to extract structure:
   ```bash
   python3 -c "
   import xml.etree.ElementTree as ET
   tree = ET.parse('<file>')
   root = tree.getroot()
   links = [l.attrib['name'] for l in root.findall('link')]
   joints = [(j.attrib['name'], j.attrib.get('type',''), j.find('parent').attrib['link'], j.find('child').attrib['link']) for j in root.findall('joint')]
   print('LINKS:', links)
   print('JOINTS:', joints)
   "
   ```

5. **Display the link tree** (parent → child via joints):
   ```
   Link Tree:
   base_link
   ├─ base_footprint         [fixed]
   ├─ left_wheel             [continuous]  axis: (0,1,0)
   ├─ right_wheel            [continuous]  axis: (0,1,0)
   └─ base_laser_link        [fixed]
      └─ laser_frame         [fixed]

   chassis_link
   └─ camera_link            [fixed]
      └─ camera_optical_frame [fixed]
   ```

6. **Check link/joint consistency**:
   - Every joint must reference links that exist: flag `ERROR: joint '<j>' references unknown link '<l>'`
   - Every link (except the root) must appear as a child in exactly one joint: flag `WARN: link '<l>' has no parent joint — possible disconnected island`
   - Multiple root links (no parent) → flag `WARN: multiple root links: [<list>] — expected exactly one`
   - Joint child = joint parent → flag `ERROR: joint '<j>' has same parent and child link`

7. **Check joint limits**:
   For revolute and prismatic joints, verify:
   - `<limit>` element exists: flag `WARN: revolute joint '<j>' has no limits defined`
   - `upper > lower`: flag `ERROR: joint '<j>' has upper limit < lower limit`
   - `effort > 0` and `velocity > 0`

8. **If --meshes flag**, find all mesh references and check they exist:
   ```bash
   grep -o 'filename="[^"]*"' <file.urdf> | sort -u
   ```
   For each mesh path (usually `package://pkg_name/meshes/file.stl`):
   - Resolve the package path: `ros2 pkg prefix <pkg_name>`
   - Check the file exists on disk
   - Flag: `❌ MISSING: package://my_robot/meshes/base.stl`

9. **If --joints flag**, display detailed joint table:
   ```
   Joint Details:
   ─────────────────────────────────────────────────────────────────
   Name              Type        Parent         Child          Limits
   ─────────────────────────────────────────────────────────────────
   base_to_wheel_l   continuous  base_link      left_wheel     vel:10 eff:100
   base_to_wheel_r   continuous  base_link      right_wheel    vel:10 eff:100
   camera_joint      fixed       base_link      camera_link    —
   arm_joint_1       revolute    base_link      arm_link_1     [-π, π] vel:3 eff:50
   ─────────────────────────────────────────────────────────────────
   ```

10. **Summary report**:
    ```
    ══════════════════════════════════════════════════════
    URDF Check: robot.urdf
    ══════════════════════════════════════════════════════
    Links:  14   Joints: 13   Meshes: 8
    ──────────────────────────────────────────────────────
    ❌ ERROR   joint 'arm_joint_3' references unknown link 'arm_3'
    ⚠  WARN    revolute joint 'wrist_joint' has no limits defined
    ⚠  WARN    link 'sensor_mount' has no parent joint
    ❌ MISSING  package://my_robot/meshes/gripper.dae
    ══════════════════════════════════════════════════════
    Issues: 2 errors, 2 warnings
    ```
    If clean: `✅ URDF is valid — no issues found`

11. **Suggest next steps**:
    - Load in robot_state_publisher: `ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro <file>)"`
    - Visualize in RViz: add `RobotModel` display, set Fixed Frame to `base_link`
    - Check TF: `/ros2-check-tf --tree`
