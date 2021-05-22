# Copyright (c) 2020 Scott Ramsby
# Cura is released under the terms of the MIT License (https://mit-license.org/).
# Created by Scott Ramsby

import re
from ..Script import Script


class LinearAdvanceTower(Script):
    _layer_regex = re.compile(r";LAYER:(\d+)")

    def getSettingDataString(self):
        return """{
            "name": "Linear Advance Tower",
            "key": "LinearAdvanceTower",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "start":
                {
                    "label": "Starting K Factor",
                    "description": "K factor for layer 0",
                    "type": "float",
                    "default_value": 0
                },
                "increment":
                {
                    "label": "K Factor Increment",
                    "description": "Increase of K factor per layer",
                    "type": "float",
                    "default_value": 0.0005
                }
            }
        }"""

    def execute(self, data):
        start = self.getSettingValueByKey("start")
        increment = self.getSettingValueByKey("increment")

        for index, layer in enumerate(data):
            lines = layer.split("\n")
            for line_number, line in enumerate(lines):
                match = LinearAdvanceTower._layer_regex.match(line)
                if match:
                    layer_number = int(match.group(1))
                    data[index] = "\n".join(lines[:line_number] + [line] + [
                                            f"M900 K{start + increment * layer_number}"] + lines[line_number + 1:])
                    break
        return data
