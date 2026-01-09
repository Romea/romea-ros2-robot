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

import pytest

from romea_lidar_meta_bringup.meta_description import (
    get_complete_configuration,
    get_geometry,
    get_specifications,
    LIDARMetaDescription,
)


@pytest.fixture(scope="module")
def meta_description():
    meta_description_file_path = os.path.join(os.getcwd(), "test_lidar_meta_bringup.yaml")
    return LIDARMetaDescription(meta_description_file_path)


def test_get_name(meta_description):
    assert meta_description.get_name() == "lidar"


def test_get_namespace(meta_description):
    assert meta_description.get_namespace() == "ns"


def test_get_launch_file(meta_description):
    assert meta_description.get_launch_file() is not None


def test_get_model(meta_description):
    assert meta_description.get_model() == "lms"


def test_get_version(meta_description):
    assert meta_description.get_version() == "151"


def test_get_rate(meta_description):
    assert meta_description.get_rate() == 50


def test_get_azimut_resolution(meta_description):
    assert meta_description.get_azimut_resolution() == 0.5


def test_get_parent_link(meta_description):
    assert meta_description.get_parent_link() == "base_link"


def test_get_xyz(meta_description):
    assert meta_description.get_xyz() == [1.0, 2.0, 3.0]


def test_get_rpy(meta_description):
    assert meta_description.get_rpy() == [4.0, 5.0, 6.0]


def test_get_records(meta_description):
    records = meta_description.get_records()
    assert records["scan"] is True
    assert records["cloud"] is False


def test_get_specifications(meta_description):
    lidar_specifactions = get_specifications(meta_description)
    assert lidar_specifactions['maximal_range']['dict']['15x'] == 50.0


def test_get_geometry(meta_description):
    lidar_geometry = get_geometry(meta_description)
    assert lidar_geometry['mass'] == 1.1


def test_get_complete_configuration(meta_description):
    lidar_configuration = get_complete_configuration(meta_description)
    assert lidar_configuration['maximal_range'] == 50.0
