# Copyright (c) 2020 Scott Ramsby
# Cura is released under the terms of the MIT License (https://mit-license.org/).
# Created by Scott Ramsby

import re
from typing import Any, Dict, List, OrderedDict
from ..Script import Script


class LinearAdvanceTower(Script):
    _layer_regex = re.compile(r";LAYER:(\d+)")

    def getSettingData(self) -> Dict[str, Any]:
        return {
            "name": "Linear Advance Tower",
            "key": "LinearAdvanceTower",
            "metadata": {},
            "version": 2,
            "settings": OrderedDict(
                start={
                    "label": "Starting Factor",
                    "description": "Factor for layer 0",
                    "type": "float",
                    "default_value": 0
                },
                increment={
                    "label": "Factor Increment",
                    "description": "Increase of factor per layer",
                    "type": "float",
                    "default_value": 0.0005
                },
                offset={
                    "label": "Offset",
                    "description": "Number of layers to offset before layer 0",
                    "type": "int",
                    "default_value": 3
                },
                base={
                    "label": "Base Factor",
                    "description": "Factor for layers before layer 0",
                    "type": "float",
                    "default_value": 0.0415
                }
            )
        }

    def execute(self, data: List[str]) -> List[str]:
        start = self.getSettingValueByKey("start")
        increment = self.getSettingValueByKey("increment")
        offset = self.getSettingValueByKey("offset")
        base = self.getSettingValueByKey("base")

        for index, layer in enumerate(data):
            lines = layer.split("\n")
            for line_number, line in enumerate(lines):
                match = LinearAdvanceTower._layer_regex.match(line)
                if match:
                    layer_number = int(match.group(1))
                    k_factor = base if layer_number < offset else (
                        start + increment * (layer_number - offset))
                    data[index] = "\n".join(lines[:line_number] + [line] + [
                                            f"M900 K{k_factor}"] + lines[line_number + 1:])
                    break
        return data
