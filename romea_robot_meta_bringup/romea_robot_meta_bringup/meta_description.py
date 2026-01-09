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

import importlib
import os
import sys
from io import StringIO
import xml.etree.ElementTree as ET

from ruamel.yaml import YAML

def include_args(name, value):
    return {"name": name, "value": value }

class RobotMetaDescription:

    class Device:
        def __init__(self, device, robot_name):
            self.type = device["type"]
            self.meta_description_file_path = device["meta_description"]
            self.meta_bringup_package = f"romea_{self.type}_meta_bringup"

            module_name = f"{self.meta_bringup_package}.meta_description"
            self.python_module = importlib.import_module(module_name)

            self.meta_description = self.python_module.load_meta_description(
                self.meta_description_file_path, robot_name
            )

        def generate_xml_urdf_description(self, mode):
            urdf_str = self.python_module.generate_urdf_description(mode, self.meta_description)
            return ET.fromstring(urdf_str)

        def generate_yaml_configuration(self, extended):
            str = self.python_module.generate_configuration_file(self.meta_description, extended)
            return {self.meta_description.get_name(): YAML().load(str)}


        def generate_yaml_launch_file(self, additional_args =[]):
            arguments = [
                include_args("mode", "$(var mode)"),
                include_args("robot_namespace", self.meta_description.get_robot_name()),
                include_args("meta_description_file_path", self.meta_description_file_path),
            ]
            file = f"$(find-pkg-share {self.meta_bringup_package})/launch/{self.type}.launch.py"
            return {
                "include": { 
                    "file": file, 
                    "arg": list(arguments)
                }
            }


    def __init__(self, meta_description_file_path, robot_name=None):
        self.__robot_name = str(robot_name or "")

        if not os.path.exists(meta_description_file_path):
            raise LookupError(
                +" robot meta description file " + meta_description_file_path + " does not exists"
            )

        with open(meta_description_file_path) as f:
            description = YAML().load(f)
            description["base"]["type"] = "mobile_base"
            description["joystick"]["type"] = "joystick"

        self.base = self.Device(description["base"], self.__robot_name)
        self.joystick = self.Device(description["joystick"], self.__robot_name)

        self.devices = []
        for device in description.get("devices", []):
            self.devices.append(self.Device(device, self.__robot_name))


def generate_yaml_launch_file_str(meta_description):
    launch_file=[]
    launch_file.append({"arg" : {"name": "mode", "default": "live"}})
    launch_file.append(meta_description.joystick.generate_yaml_launch_file())

    arguments = [
        include_args("mode", "$(var mode)"),
        include_args("robot_namespace", meta_description.base.meta_description.get_robot_name()),
        include_args("mobile_base_meta_description_file_path", meta_description.base.meta_description_file_path),
        include_args("joystick_meta_description_file_path", meta_description.joystick.meta_description_file_path),
    ]
    # arguments = [
    #     include_args("mode", "$(var mode)"),
    #     include_args("robot_namespace", meta_description.base.meta_description.get_robot_name()),
    #     include_args("mobile_base_meta_description_file_path", meta_description.base.meta_description_file_path),
    #     include_args("joystick_meta_description_file_path", meta_description.joystick.meta_description_file_path),
    # ],
    file = "$(find-pkg-share romea_mobile_base_meta_bringup)/launch/mobile_base.launch.py"
    launch_file.append({
            "include": { 
                "file": file,
                "arg": list(arguments),
            }
        }
    )



    for device in meta_description.devices:
        launch_file.append(device.generate_yaml_launch_file())

    
    yaml = YAML()
    buf = StringIO()
    yaml.dump({"launch" : launch_file}, buf)
    return buf.getvalue()


def generate_xml_urdf_description_str(mode, meta_description):

    urdf = meta_description.base.generate_xml_urdf_description(mode)

    for device in meta_description.devices:
        urdf.extend(device.generate_xml_urdf_description(mode))

    return ET.tostring(urdf, encoding="unicode")


def generate_yaml_configuration_str(meta_description, extended):

    config = {}
    config.update(meta_description.base.generate_yaml_configuration(extended))
    # config.update(meta_description.joystick.generate_yaml_configuration(extended))

    for device in meta_description.devices:
        config.update(device.generate_yaml_configuration(extended))

    yaml = YAML()
    buf = StringIO()
    yaml.dump(config, buf)
    return buf.getvalue()
