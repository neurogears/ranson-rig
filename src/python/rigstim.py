# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 20:44:52 2020

@author: gonca
"""

from enum import Enum

class WallType(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    FRONT = 4
    
class TriggerType(Enum):
    NONE = 0
    END_ON_ENTRY = 1
    END_ON_LICK = 2
    TELEPORT_ON_ENTRY = 3
    TELEPORT_ON_LICK = 4
    CHANGE_GAIN_ON_ENTRY = 5
    REWARD_ON_ENTRY = 6
    REWARD_ON_LICK = 7

class RigClient:
    def __init__(self, client):
        self.client = client
        
    def gratings(self, **kwargs):
        angle = float(kwargs.get('angle',0.0))
        size = float(kwargs.get('size',20.0))
        x = float(kwargs.get('x',0.0))
        y = float(kwargs.get('y',0.0))
        
        contrast = float(kwargs.get('contrast',1.0))
        opacity = float(kwargs.get('opacity',1.0))
        phase = float(kwargs.get('phase',0.0))
        freq = float(kwargs.get('freq',0.1))
        speed = float(kwargs.get('speed',0.0))
        dcycle = float(kwargs.get('dcycle',float('nan')))
        
        onset = float(kwargs.get('onset',0.0))
        duration = float(kwargs.get('duration',1.0))
        
        self.client.send_message("/gratings",
                                 [[angle,size,x,y],
                                  [contrast,opacity,phase,freq,speed,dcycle],
                                  [onset,duration]])
    
    def video(self, name, **kwargs):
        angle = float(kwargs.get('angle',0.0))
        width = float(kwargs.get('width',20.0))
        height = float(kwargs.get('height',20.0))
        x = float(kwargs.get('x',0.0))
        y = float(kwargs.get('y',0.0))
        
        loop = float(kwargs.get('loop',1.0))
        speed = float(kwargs.get('speed',30.0))
        
        onset = float(kwargs.get('onset',0.0))
        duration = float(kwargs.get('duration',2.0))
        
        self.client.send_message("/video",
                                 [[angle,width,height,x,y],
                                  [loop,speed,name],
                                  [onset,duration]])
    
    def start(self):
        self.client.send_message("/start", 0)
    
    def go(self, duration):
        self.client.send_message("/go", [duration])
        
    def nogo(self, duration):
        self.client.send_message("/nogo", [duration])
    
    def tile(self, wall, **kwargs):
        position = float(kwargs.get('position',0.0))
        extent = float(kwargs.get('extent',1.0))
        texture = str(kwargs.get('texture',"Transparent"))
        interaction = kwargs.get('interaction',TriggerType.NONE)
        argument = float(kwargs.get('argument',0.0))
        repetitions = int(kwargs.get('repetitions',1))
        self.client.send_message("/tile",
                                 [int(wall.value),
                                  position,
                                  extent,
                                  texture,
                                  int(interaction.value),
                                  argument,
                                  repetitions])
    
    def corridor(self, length, **kwargs):
        width = float(kwargs.get('width',1.0))
        height = float(kwargs.get('height',1.0))
        x = float(kwargs.get('x',0.0))
        y = float(kwargs.get('y',0.0))
        position = float(kwargs.get('position',0.0))
        self.client.send_message("/corridor",
                                 [length,
                                  width,
                                  height,
                                  x, y,
                                  position])