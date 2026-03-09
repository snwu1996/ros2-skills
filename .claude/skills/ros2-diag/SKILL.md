---
name: ros2-diag
description: Monitor the /diagnostics topic and render a live health dashboard — OK, WARN, ERROR per component. Usage: /ros2-diag [--duration sec] [--filter name] [--errors-only] [--watch]
argument-hint: [--duration sec] [--filter name] [--errors-only] [--watch]
allowed-tools: Bash
---

# ROS2 Diagnostics Monitor

Subscribe to `/diagnostics` and render a component health dashboard. Arguments: `$ARGUMENTS`

Parse arguments:
- **--duration sec**: collect for this many seconds then summarize (default: `5`)
- **--filter name**: only show components whose name contains this string
- **--errors-only**: only show WARN and ERROR components
- **--watch**: collect for `--duration` then repeat (continuous mode, Ctrl-C to stop)

## Steps

1. **Check /diagnostics is being published**:
   ```bash
   ros2 topic info /diagnostics
   ```
   If no publishers found, check for `/diagnostics_agg` (aggregated):
   ```bash
   ros2 topic info /diagnostics_agg
   ```
   Report which topic is available. If neither exists, warn: no diagnostics publisher running. Suggest starting `diagnostic_aggregator` or checking that hardware drivers are up.

2. **Collect diagnostics messages**:
   ```bash
   timeout <duration> ros2 topic echo /diagnostics
   ```
   Use `/diagnostics_agg` if that's what's available.

3. **Parse the DiagnosticArray messages** — each message contains a list of `DiagnosticStatus` entries with:
   - `level`: 0=OK, 1=WARN, 2=ERROR, 3=STALE
   - `name`: component name (e.g. `"motor_driver: left_motor"`)
   - `message`: human-readable status string
   - `values`: key-value hardware metrics

4. **Aggregate across collection window**:
   - Track worst level seen per component name
   - Collect all unique messages per component
   - Collect all key-value pairs seen

5. **Render the dashboard**:
   ```
   ROS2 Diagnostics Dashboard  (collected 5.0s, 47 messages)
   ══════════════════════════════════════════════════════════

   ✅ OK    camera_driver: rgb_camera       "Publishing at 30 Hz"
   ✅ OK    camera_driver: depth_camera     "Publishing at 30 Hz"
   ✅ OK    imu_driver: imu_sensor          "IMU data nominal"
   ⚠  WARN  motor_driver: left_motor        "Temperature 72°C (limit: 75°C)"
              └─ temperature: 72.3°C
              └─ current: 2.1A
              └─ voltage: 24.1V
   ❌ ERROR  lidar_driver: rplidar          "Connection timeout"
              └─ last_scan_age: 3.21s
              └─ error_count: 14
   🕐 STALE  gps_driver: nmea_fix          "No data received"
   ══════════════════════════════════════════════════════════
   Summary: 3 OK  1 WARN  1 ERROR  1 STALE
   ```

   Level indicators:
   - `✅ OK` — green
   - `⚠  WARN` — yellow
   - `❌ ERROR` — red
   - `🕐 STALE` — grey (no update received)

6. **If --filter flag**, only show components whose name contains the filter string (case-insensitive).

7. **If --errors-only flag**, suppress OK entries — only show WARN, ERROR, STALE.

8. **Surface actionable suggestions** for each non-OK component:
   - Temperature near limit → "Check cooling / reduce load on motor_driver: left_motor"
   - Connection timeout → "Check USB/serial connection to lidar_driver: rplidar; run `ls /dev/tty*`"
   - STALE → "Component may have crashed; check: `ros2 node list | grep <driver>`"

9. **If --watch flag**, repeat the collection + render loop continuously. Clear screen between iterations. Show timestamp at top of each render.
