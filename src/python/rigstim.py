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

class RigClient:
    def __init__(self, client):
        self.client = client
        
    def experiment(self,expid):
        self.client.send_message("/experiment", expid)
        
    def replay(self, expid, trial):
        self.client.send_message("/replay", [expid, trial])
        
    def resource(self, path):
        self.client.send_message("/resource", path)
        
    def preload(self):
        self.client.send_message("/preload", 0)
        
    def clear(self):
        self.client.send_message("/clear", 0)
        
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
        
    def success(self):
        self.client.send_message("/success", 0)
        
    def failure(self):
        self.client.send_message("/failure", 0)
    
    def go(self, suppress=2000, start=500, duration=1000, threshold=1):
        self.client.send_message("/go",
                                 [float(suppress),
                                  float(start),
                                  float(duration),
                                  int(threshold)])
        
    def nogo(self, suppress=2000, start=500, duration=1000, threshold=1):
        self.client.send_message("/nogo",
                                 [float(suppress),
                                  float(start),
                                  float(duration),
                                  int(threshold)])
        
    def interaction(self, name, arguments):
        self.client.send_message('/interaction/{0}'.format(name), arguments)
    
    def tile(self, wall, **kwargs):
        position = float(kwargs.get('position',0.0))
        extent = float(kwargs.get('extent',1.0))
        texture = str(kwargs.get('texture',"Transparent"))
        self.client.send_message("/tile",
                                 [int(wall.value),
                                  position,
                                  extent,
                                  texture])
    
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