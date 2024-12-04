# Copyright (C) 2021 Intel Corporation 
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information

from .sensor import *
from .sensorcontroller import *

class RfsSensor(SensorController):
    def __init__(self,name='rfsSensors', real=False, offset=0x0) -> None:
        self.name = name
        self.modules = {
            'lux'           : Sensor('lux',             'float', real,        offset+0x4*2),
            'humidity'      : Sensor('humidity',        'float', real,        offset+0x4*3),
            'temperature'   : Sensor('temperature',     'float', real,        offset+0x4*4)
        }