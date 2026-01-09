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


import os
import subprocess
import xml.etree.ElementTree as ET

from ament_index_python import get_package_prefix
import pytest


@pytest.fixture(scope="module")
def urdf():

    exe = (
        get_package_prefix("romea_lidar_meta_bringup")
        + "/lib/romea_lidar_meta_bringup/generate_urdf_description.py"
    )

    meta_description_file_path = os.path.join(os.getcwd(), "test_lidar_meta_bringup.yaml")

    return ET.fromstring(
        subprocess.check_output(
            [
                exe,
                "mode:simulation_gazebo_classic",
                "robot_namespace:robot",
                "meta_description_file_path:" + meta_description_file_path,
            ],
            encoding="utf-8",
        )
    )


def test_lidar_name(urdf):
    assert urdf.find("link").get("name") == "robot_lidar_link"


def test_lidar_position(urdf):
    print("xyz", urdf.find("joint/origin").get("xyz"))
    assert urdf.find("joint/origin").get("xyz") == "1.0 2.0 3.0"


def test_lidar_orientation(urdf):
    print("orientation", urdf.find("joint/origin").get("rpy"))
    assert (
        urdf.find("joint/origin").get("rpy")
        == "0.06981317007977318 0.08726646259971647 0.10471975511965977"
    )


def test_lidar_parent_link(urdf):
    assert urdf.find("joint/parent").get("link") == "robot_base_link"


def test_lidar_rate(urdf):
    assert urdf.find("gazebo/sensor/update_rate").text == "50"


def test_plugin_namespace(urdf):
    assert urdf.find("gazebo/sensor/plugin/ros/namespace").text == "/robot/ns/lidar"
