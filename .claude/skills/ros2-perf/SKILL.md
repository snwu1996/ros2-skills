---
name: ros2-perf
description: Profile a running ROS2 node's CPU and memory usage, measure topic latency end-to-end, and identify performance bottlenecks. Usage: /ros2-perf <node_name> [--duration sec] [--topics] [--latency topic] [--cpu] [--mem]
argument-hint: <node_name> [--duration sec] [--topics] [--latency <topic>] [--cpu] [--mem]
allowed-tools: Bash
---

# ROS2 Node Performance Profiler

Measure CPU, memory, and message latency for a running ROS2 node. Arguments: `$ARGUMENTS`

Parse arguments:
- **node_name**: first argument — node to profile (e.g. `/move_base`). Prepend `/` if missing.
- **--duration sec**: profiling window in seconds (default: `10`)
- **--topics**: include per-topic message rate and latency stats
- **--latency topic**: measure end-to-end latency on a specific topic (time from publish to receipt)
- **--cpu**: CPU profiling only
- **--mem**: memory profiling only
- If no flags given, run all profiling

## Steps

1. **Verify the node is running**:
   ```bash
   ros2 node list | grep "<node_name>"
   ```
   If not found, stop.

2. **Find the node's PID**:
   ```bash
   # Map node name to process
   ros2 node info <node_name> 2>/dev/null | head -5
   # Find PID via process name
   ps aux | grep -E "ros2|<executable_name>" | grep -v grep | awk '{print $2, $11}'
   ```
   If multiple PIDs found, list them and let the user pick, or use the most recently started.

3. **Sample CPU and memory** over the duration:
   ```bash
   # Poll every second for <duration> seconds
   for i in $(seq 1 <duration>); do
     ps -p <pid> -o pid,pcpu,pmem,rss,vsz --no-headers 2>/dev/null
     sleep 1
   done
   ```
   Collect: CPU%, memory RSS (resident), VSZ (virtual), at each sample.

4. **Compute statistics** from samples:
   - CPU: min, max, mean, stddev
   - RSS memory: min, max, mean, peak
   - Detect: memory growth over time (potential leak)

5. **Check thread count**:
   ```bash
   ps -p <pid> -o nlwp --no-headers 2>/dev/null  # thread count
   ls /proc/<pid>/task/ 2>/dev/null | wc -l
   ```

6. **If --topics or no flags**, collect topic rates:
   ```bash
   # For each topic the node publishes or subscribes to:
   timeout 5 ros2 topic hz <topic> 2>/dev/null | tail -3
   ```
   Run in parallel for all node topics. Report actual vs expected rate.

7. **If --latency topic**, measure message latency:
   ```bash
   # Compare header.stamp to receive time for messages with headers
   timeout <duration> ros2 topic echo <topic> --no-arr 2>/dev/null | grep "stamp\|sec\|nanosec"
   ```
   Calculate: `receive_time - header.stamp` = processing latency.
   For messages without headers, measure round-trip via a test publisher if needed.

8. **Check for CPU spikes** — identify if the node is spinning hot:
   ```bash
   top -b -n 3 -p <pid> | grep <pid>
   ```
   Flag: CPU > 80% sustained → `WARN: node is CPU-bound`
   Flag: CPU spikes to 100% periodically → `INFO: likely timer callback or burst processing`

9. **Check memory growth** — compare first vs last RSS sample:
   - Growth > 10% over duration → `WARN: possible memory leak — RSS grew <N> MB in <duration>s`
   - Stable → `✅ Memory stable`

10. **Display profiling report**:
    ```
    Node Performance: /move_base
    Duration: 10s  |  PID: 12345  |  Threads: 8
    ══════════════════════════════════════════════════════

    CPU Usage:
      Mean:  12.3%   Max: 34.1%   Min: 2.1%
      ⚠  Spikes to >30% — check callback processing time

    Memory:
      RSS Mean: 245 MB   Peak: 251 MB   Growth: +2 MB
      VSZ:      1.2 GB   (virtual — includes shared libs)
      ✅ Memory appears stable

    Threads: 8
      (typical for multi-threaded executor with 4 callbacks)

    Topic Rates:
    ────────────────────────────────────────────────────
    Topic                  Expected    Actual    Status
    ────────────────────────────────────────────────────
    /scan (sub)            10 Hz       9.8 Hz    ✅
    /odom (sub)            50 Hz       49.7 Hz   ✅
    /cmd_vel (pub)          5 Hz        5.0 Hz   ✅
    /move_base/status (pub) 5 Hz        0.2 Hz   ⚠  LOW
    ────────────────────────────────────────────────────

    Latency (/scan → processed):
      Mean: 4.2ms   Max: 18.7ms   P95: 12.1ms

    ══════════════════════════════════════════════════════
    Issues: 2 warnings

    ⚠  CPU spikes >30% — check if callback is blocking:
       Consider async processing or offloading heavy work
    ⚠  /move_base/status publishing at 0.2 Hz (expected 5 Hz):
       Check if publisher timer is set correctly
    ```

11. **Suggest fixes** for detected issues:
    - High CPU → use `rclcpp::MultiThreadedExecutor`, move heavy work off callbacks
    - Memory growth → check for subscriber queue buildup, large message caching
    - Low publish rate → check timer callback is not blocked by long computation
    - High latency → profile the callback itself with timestamps
