# Copyright 2022 INRAE, French National Research Institute for Agriculture, Food and Environment
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import GroupAction, OpaqueFunction
from launch_ros.actions import Node, PushRosNamespace, SetParameter

import romea_common_meta_bringup.ros_launch as common
import romea_robot_meta_bringup.ros_launch as robot
from romea_robot_meta_bringup.meta_description import generate_xml_urdf_description_str

def launch_setup(context, *args, **kwargs):

    mode = common.get_mode(context)
    robot_namespace = common.get_robot_namespace(context)
    robot_meta_description = robot.get_meta_description(context)
    robot_urdf_description = generate_xml_urdf_description_str(mode, robot_meta_description)

    base_name = robot_meta_description.base.meta_description.get_name()
    joint_states_source_list = [f"{base_name}/joint_states"]
    for device in robot_meta_description.devices:
        if device.type == "arm":
            device_name = device.meta_description.get_name()
            joint_states_source_list.append(f"{device_name}/joint_states")

    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        parameters=[
            {"source_list": joint_states_source_list},
            {"rate": 100},
        ],
        output={
            'stdout': 'log',
            'stderr': 'log',
        },
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_urdf_description}],
        output={
            'stdout': 'log',
            'stderr': 'log',
        },
    )

    return [
        GroupAction(
            actions=[
                SetParameter(name="use_sim_time", value=(mode != "live")),
                PushRosNamespace(robot_namespace),
                joint_state_publisher,
                robot_state_publisher,
            ]
        )
    ]


def generate_launch_description():

    return LaunchDescription(
        [
            common.declare_mode(),
            common.declare_robot_namespace(),
            common.declare_meta_description_file_path("robot"),
            OpaqueFunction(function=launch_setup)
        ]
    )
