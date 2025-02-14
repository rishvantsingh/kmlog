# Copyright 2021 - 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>, Dr. Rajesh Kumar <Rajesh.Kumar@hofstra.edu>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from base.backends.yaml_driver import YAMLDriver
import os
from base.user_ops.generic_ops import *


def user_id_to_yaml_file_path(user_id: str) -> str:
    # NOTE: We have to deal with the edge case where part of a user_id can exist in another (eg the user_id 123 is in the user_id 1234)
    directory = os.path.join(os.getcwd(), "src", "users")
    for file in os.scandir(directory):
        if file.path.endswith(".yaml") and file.is_file:
            # Trim the extension from the file path and see if it matches the user_id given
            file_with_ext = os.path.basename(file.path)
            file_name = os.path.splitext(file_with_ext)[0]
            if file_name == user_id:
                return os.path.join(directory, file_with_ext)


def tuple_to_dict(data: tuple, labels: list):
    assert (
        len(data) == len(labels),
        "Cannot create a dictionary from a tuple if the length of the tuple != length of the labels",
    )
    data_list = list(data)
    data_dict = {}
    for i in range(len(data_list)):
        data_dict[labels[i]] = data_list[i]
    return data_dict


def create_user(user_id: str):
    (
        first,
        last,
        handedness,
        gender,
        age,
        education_level,
        social_platform,
    ) = generic_create_user()

    part = expand_user_data(
        str(gender), str(handedness), str(education_level), str(social_platform)
    )
    # FIXME: We have to figure out a way so the string fields actually have quotes around them
    pl = list(part)
    pl.insert(0, f'"{str(last)}"')
    pl.insert(0, f'"{str(first)}"')
    pl.insert(0, int(user_id))
    pl.insert(4, int(age))
    t = tuple(pl)
    labels = [
        "user_id",
        "first_name",
        "last_name",
        "gender",
        "age",
        "handedness",
        "education",
        "platform",
    ]

    data = tuple_to_dict(t, labels)
    yml = YAMLDriver()
    yml.write_to_yaml_file(user_id, data)
