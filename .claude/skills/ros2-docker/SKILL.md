---
name: ros2-docker
description: Generate a Dockerfile and .dockerignore for a ROS2 workspace or package — with rosdep install, colcon build, and correct entrypoint sourcing. Supports multi-stage builds. Usage: /ros2-docker [package_path] [--distro humble|iron|jazzy] [--multi-stage] [--gpu]
argument-hint: [package_path] [--distro humble|iron|jazzy] [--multi-stage] [--gpu]
allowed-tools: Read, Write, Glob, Bash
---

# ROS2 Dockerfile Generator

Generate a production-ready Dockerfile for a ROS2 workspace. Arguments: `$ARGUMENTS`

Parse arguments:
- **package_path**: path to workspace root (default: current directory)
- **--distro**: ROS2 distro — `humble`, `iron`, or `jazzy` (default: detect from `$ROS_DISTRO` or `humble`)
- **--multi-stage**: generate a multi-stage build (builder + runtime) for smaller images
- **--gpu**: add NVIDIA GPU support (nvidia/cuda base, `--gpus all` runtime flag)

## Steps

1. **Detect the workspace structure**:
   ```bash
   ls src/
   find src/ -name package.xml -maxdepth 3
   ```
   Collect all package names and their build types (cmake vs python).

2. **Detect ROS2 distro** — check argument, then env var, then default:
   ```bash
   echo $ROS_DISTRO
   ```

3. **Determine base image**:
   - Standard: `ros:<distro>-ros-base`
   - With GPU: `nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04` (Humble/Iron) or `ubuntu:24.04` (Jazzy)
   - Desktop (if rviz/rqt needed): `ros:<distro>-desktop`

4. **Generate `Dockerfile`** at the workspace root:

   **Single-stage (default):**
   ```dockerfile
   FROM ros:humble-ros-base

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       python3-colcon-common-extensions \
       python3-rosdep \
       && rm -rf /var/lib/apt/lists/*

   # Set up workspace
   WORKDIR /ros2_ws
   COPY src/ src/

   # Install ROS dependencies
   RUN . /opt/ros/humble/setup.sh && \
       rosdep update && \
       rosdep install --from-paths src --ignore-src -r -y

   # Build workspace
   RUN . /opt/ros/humble/setup.sh && \
       colcon build --symlink-install

   # Source workspace in entrypoint
   COPY docker/entrypoint.sh /entrypoint.sh
   RUN chmod +x /entrypoint.sh

   ENTRYPOINT ["/entrypoint.sh"]
   CMD ["bash"]
   ```

   **Multi-stage (with --multi-stage):**
   ```dockerfile
   # ── Stage 1: Builder ──────────────────────────────────────────
   FROM ros:humble-ros-base AS builder

   RUN apt-get update && apt-get install -y \
       python3-colcon-common-extensions \
       python3-rosdep \
       && rm -rf /var/lib/apt/lists/*

   WORKDIR /ros2_ws
   COPY src/ src/

   RUN . /opt/ros/humble/setup.sh && \
       rosdep update && \
       rosdep install --from-paths src --ignore-src -r -y

   RUN . /opt/ros/humble/setup.sh && \
       colcon build --merge-install

   # ── Stage 2: Runtime ──────────────────────────────────────────
   FROM ros:humble-ros-base AS runtime

   RUN apt-get update && apt-get install -y \
       python3-rosdep \
       && rm -rf /var/lib/apt/lists/*

   WORKDIR /ros2_ws

   # Copy only the install directory from builder
   COPY --from=builder /ros2_ws/install/ install/

   # Re-install runtime-only ROS deps
   COPY src/ src/
   RUN . /opt/ros/humble/setup.sh && \
       rosdep update && \
       rosdep install --from-paths src --ignore-src -r -y --dependency-types exec && \
       rm -rf src/

   COPY docker/entrypoint.sh /entrypoint.sh
   RUN chmod +x /entrypoint.sh

   ENTRYPOINT ["/entrypoint.sh"]
   CMD ["bash"]
   ```

5. **Generate `docker/entrypoint.sh`**:
   ```bash
   #!/bin/bash
   set -e

   # Source ROS2
   source /opt/ros/humble/setup.bash

   # Source workspace if built
   if [ -f /ros2_ws/install/setup.bash ]; then
     source /ros2_ws/install/setup.bash
   fi

   exec "$@"
   ```

6. **Generate `.dockerignore`**:
   ```
   # Build artifacts
   build/
   install/
   log/

   # IDE and OS
   .vscode/
   .git/
   **/.DS_Store

   # Python
   **/__pycache__/
   **/*.pyc

   # ROS2 logs
   ~/.ros/
   ```

7. **Generate `docker/compose.yaml`** (Docker Compose for easy use):
   ```yaml
   services:
     ros2_app:
       build: .
       image: my_robot:latest
       network_mode: host
       ipc: host
       environment:
         - ROS_DOMAIN_ID=0
         - DISPLAY=${DISPLAY}
       volumes:
         - /tmp/.X11-unix:/tmp/.X11-unix
       command: bash
   ```
   For GPU support, add:
   ```yaml
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: all
                 capabilities: [gpu]
   ```

8. **Print summary**:
   ```
   ✅ Docker setup generated

   Files created:
     Dockerfile              — <single|multi>-stage build
     docker/entrypoint.sh    — sources ROS2 + workspace
     docker/compose.yaml     — Docker Compose config
     .dockerignore           — excludes build/ install/ log/

   Build:
     docker build -t my_robot:latest .

   Run:
     docker run --rm -it --network host my_robot:latest

   With Compose:
     docker compose -f docker/compose.yaml up

   With GUI (X11):
     xhost +local:docker
     docker compose -f docker/compose.yaml up
   ```
