# testbed_navigation

## Overview
Built a fully modular ROS2 navigation pipeline for the Testbed-T1.0.0 robot by directly orchestrating individual Nav2 plugins — completely bypassing `nav2_bringup`. Each component was manually instantiated, parameterized, and lifecycle-managed giving full control over the navigation stack.

## Environment Setup
- Original system configured with ROS2 Jazzy and Ignition Gazebo
- Nav2 required ROS2 Humble + Gazebo Classic
- Resolved via Docker-based isolated environment with X11 forwarding for RViz2 and Gazebo GUI

## Package Structure
\```
testbed_navigation/
├── config/
│   ├── amcl_params.yaml
│   └── nav2_params.yaml
├── launch/
│   ├── map_loader.launch.py
│   ├── localization.launch.py
│   ├── navigation.launch.py
│   └── master.launch.py
├── navigation.rviz
└── README.md
\```

## Architecture
Three independently managed subsystems each with their own launch file and lifecycle manager:

**Map Loading** — Serves occupancy grid with transient local QoS ensuring late-joining nodes always receive the map.

**Localization** — AMCL configured with tuned particle filter parameters. Initial pose automatically injected at robot's known spawn position — no manual RViz2 intervention needed.

**Navigation Stack** — Six plugins manually configured:
- `planner_server` — Global path planning via NavfnPlanner
- `controller_server` — Local trajectory execution via DWB with 6 tuned critics
- `bt_navigator` — Behavior tree orchestration with replanning and recovery
- `behavior_server` — Spin, BackUp and Wait recovery behaviors
- `velocity_smoother` — Enforces acceleration limits before commands reach hardware

## Master Launch Orchestration
Single command launches the entire pipeline in a time-synchronized sequence:
\```
t = 0s  → Map server starts
t = 3s  → AMCL starts and receives map
t = 6s  → Initial pose injected, map→odom transform established
t = 10s → Navigation stack starts with all transforms ready
\```

## Challenges
- Configured Docker environment with X11 forwarding and DDS networking for ROS2 Humble + Gazebo Classic compatibility
- AMCL requires initial pose to publish `map→odom` transform — solved via automatic pose injection in launch file
- DWB controller generating only rotational velocity — fixed by adding missing `sim_time`, `min_speed_xy` and sampling parameters
- Velocity smoother publishing to `/cmd_vel_smoothed` but robot expecting `/cmd_vel` — fixed via topic remapping
- Lifecycle node race conditions on startup — resolved using `TimerAction` delays in master launch file

## How to Run
\```bash
cd ~/assignment_ws
colcon build --packages-select testbed_navigation
source install/setup.bash
ros2 launch testbed_navigation master.launch.py
\```
Robot localizes and is ready for navigation goals via **2D Goal Pose** in RViz2 within ~15 seconds.

## Dependencies
- ROS2 Humble, Nav2, Gazebo Classic 11
- `dwb_core`, `nav2_navfn_planner`, `nav2_velocity_smoother`
