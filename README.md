# Team Varuna — Underwater ROV Simulation

ROS 2 and Gazebo Sim workspace for developing and testing Team Varuna's underwater ROV model and underwater environment.

> **Current status:** The world and ROV launch/spawn workflow has been tested locally. The ROV can oscillate after spawning; buoyancy, displaced volume, mass distribution, and restoring moments are still being tuned. This is a simulation-development checkpoint, not yet a validated hydrodynamic model.

## Tested software setup

| Component | Version |
|---|---|
| Operating system | Ubuntu 22.04 LTS |
| ROS 2 | Humble |
| Gazebo Sim | 8.x (Gazebo Harmonic family) |
| ROS–Gazebo integration | `ros_gz_sim` and `ros_gz_bridge`, installed/built to match the local Gazebo Sim installation |
| Build system | `colcon` with `ament_cmake` |

**Compatibility note:** ROS 2 Humble's commonly distributed ROS–Gazebo packages may target a different Gazebo release depending on the installation source. Do not mix ROS–Gazebo bridge binaries built for another Gazebo version with Gazebo Sim 8. Confirm that `gz sim`, `ros_gz_sim`, and `ros_gz_bridge` are compatible on your machine before launching.

## Main project files

- `worlds/underwater_world.sdf` — underwater simulation world.
- `models/underwater_rov/model.sdf` — ROV model, links, sensors, and plugins.
- `launch/spawn_rov.launch.py` — starts Gazebo, bridges camera topics, and spawns the ROV.
- `config/rov_bridge.yaml` — Gazebo-to-ROS camera image and camera-info bridge configuration.
- `package.xml` and `CMakeLists.txt` — ROS 2 package metadata and installation rules.

## Prerequisites

Install the ROS 2 Humble desktop tools and build utilities:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  python3-colcon-common-extensions \
  python3-rosdep
```

Make sure **Gazebo Sim 8** and compatible ROS–Gazebo integration packages are installed. The launch file requires these ROS packages:

- `ros_gz_sim`
- `ros_gz_bridge`

If these packages are already installed, verify them rather than reinstalling a potentially incompatible version:

```bash
gz sim --version
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
```

If either `ros2 pkg prefix` command cannot find its package, install/build the ROS–Gazebo integration appropriate for your Gazebo Sim 8 installation before continuing. Avoid mixing packages compiled for different Gazebo major versions.

## Clone the repository

```bash
source /opt/ros/humble/setup.bash
mkdir -p ~/rov_sim_ws/src
cd ~/rov_sim_ws/src
git clone https://github.com/siddddhu22-lab/team-varuna-rov-simulation.git rov_simulation
```

If the repository is already cloned, skip the `git clone` step.

## Build the package

```bash
source /opt/ros/humble/setup.bash
cd ~/rov_sim_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select rov_simulation
source install/setup.bash
```

After opening a new terminal, source both environments before using the package:

```bash
source /opt/ros/humble/setup.bash
source ~/rov_sim_ws/install/setup.bash
```

## Launch the underwater world and ROV

```bash
source /opt/ros/humble/setup.bash
source ~/rov_sim_ws/install/setup.bash
ros2 launch rov_simulation spawn_rov.launch.py
```

The launch file starts Gazebo Sim with `underwater_world.sdf`, starts the configured ROS–Gazebo bridge, and spawns `underwater_rov` after a short delay.

Stop the simulation with **Ctrl+C** in the terminal running the launch command.

## Check the camera topics

In a second terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/rov_sim_ws/install/setup.bash
ros2 topic list
ros2 topic echo /rov/camera/camera_info --once
```

If the camera image topic is present, view it with:

```bash
ros2 run rqt_image_view rqt_image_view
```

Select `/rov/camera/image_raw` in the image viewer. If the topics do not appear, check the Gazebo sensor topic names and bridge output in the launch terminal.

## Troubleshooting

- **Package not found:** source `/opt/ros/humble/setup.bash` and `~/rov_sim_ws/install/setup.bash`; rebuild with `colcon build --packages-select rov_simulation` if needed.
- **Gazebo or bridge library errors:** verify that Gazebo Sim and `ros_gz_*` packages target compatible Gazebo versions.
- **ROV does not spawn:** check the launch terminal for errors and confirm that `models/underwater_rov/model.sdf` is installed under the package share directory.
- **ROV oscillates or sinks:** this is a known development item. Review total modeled mass, displaced volume, buoyancy configuration, center of mass/buoyancy, thruster forces, and joint axes. Do not treat the current motion as physically validated.
- **Camera topics missing:** inspect Gazebo topics with `gz topic -l`, then make the names and message types in `config/rov_bridge.yaml` match the running sensor.

## Development workflow

Keep stable checkpoints before changing world physics or model dynamics:

```bash
git status
git add worlds/underwater_world.sdf models/underwater_rov/model.sdf
git commit -m "Describe simulation change"
```

Use a separate experiment branch for buoyancy and stability work. Commit only files you have reviewed.

## License

See the repository's license file, if present.
