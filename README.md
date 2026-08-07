# romea_ros2_robot

## Overview

`romea_ros2_robot` groups the ROS2 packages used to assemble, describe and launch complete robot systems in the ROMEA ecosystem.

This repository-level README gives a map of the stack. Detailed behavior, robot meta-description formats, generated files and launch examples are documented in the README of each package listed below.

## Packages

| Package | Role |
| --- | --- |
| `romea_robot` | Metapackage for the robot stack. |
| `romea_robot_meta_bringup` | Main user entry point: robot meta-description parser, robot-level configuration generation, URDF generation and launch generation. |

## Usage

This stack is usually consumed from a larger ROMEA workspace or from a demo configuration that already selects the mobile base, joystick, sensors, implements and manipulators that compose the robot.

In most cases, start with `romea_robot_meta_bringup`. It is the user-facing entry point of the stack. A robot meta-description does not describe each component in detail; it lists the meta-description files selected for the mobile base, joystick and optional devices such as GPS, IMU, lidar, cameras, implements and arms.

From this composition, `romea_robot_meta_bringup` can generate the robot-level configuration file, generate the complete robot URDF, generate the launch description that includes all selected components, and start the robot state publisher.

The robot stack does not describe each component itself. It delegates mobile bases, joysticks, sensors, implements and arms to their own `<component>_meta_bringup` packages, then combines the generated artifacts into a robot-level runtime.

Use the specialized package README files when you need to inspect or extend a specific part of the stack:

* `romea_robot_meta_bringup` to write robot meta-descriptions, generate full robot artifacts and launch complete robot systems;
* the corresponding component meta-bringup packages to configure mobile bases, joysticks, sensors, implements and arms.

## License

This project is released under the Apache License 2.0. See the `LICENSE` file for details.

## Authors

The `romea_ros2_robot` stack was developed by Jean Laneurit in the context of research projects carried out at INRAE.

## Contact

For questions or comments about this stack, contact [Jean Laneurit](mailto:jean.laneurit@inrae.fr).
