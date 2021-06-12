# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 20:44:52 2020

@author: gonca
"""

import queue
from enum import Enum
from pyOSC3.OSC3 import OSCMessage

class WallType(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    FRONT = 4

class RigClient:
    def __init__(self, client):
        self.client = client
        self.client.addMsgHandler("default", self.msg_handler)
        self.msgs = queue.Queue()

    def msg_handler(self, address, *args):
        msg = OSCMessage(address, args)
        self.msgs.put(msg)
        print(msg)

    def send(self, address="", *args):
        message = OSCMessage(address, *args)
        return self.client.sendOSC(message)

    def receive(self):
        return self.msgs.get()

    def dataset(self, path):
        self.send("/dataset", path)
        
    def experiment(self,expid):
        self.send("/experiment", "" if expid is None else expid)
        
    def replay(self, expid, trial):
        self.send("/replay", [expid, trial])
        
    def resource(self, path):
        self.send("/resource", path)
        
    def preload(self):
        self.send("/preload", 0)
        
    def clear(self):
        self.send("/clear", 0)
        
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
        
        self.send("/gratings",
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
        
        self.send("/video",
                  [[angle,width,height,x,y],
                   [loop,speed,name],
                   [onset,duration]])
    
    def start(self):
        self.send("/start", 0)
        
    def success(self):
        self.send("/success", 0)
        
    def failure(self):
        self.send("/failure", 0)
    
    def go(self, suppress=2000, start=500, duration=1000, threshold=1):
        self.send("/go",
                  [float(suppress),
                   float(start),
                   float(duration),
                   int(threshold)])
        
    def nogo(self, suppress=2000, start=500, duration=1000, threshold=1):
        self.send("/nogo",
                  [float(suppress),
                   float(start),
                   float(duration),
                   int(threshold)])
        
    def interaction(self, name, arguments):
        self.send('/interaction/{0}'.format(name), arguments)
    
    def tile(self, wall, **kwargs):
        position = float(kwargs.get('position',0.0))
        extent = float(kwargs.get('extent',1.0))
        texture = str(kwargs.get('texture',"Transparent"))
        self.send("/tile",
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
        self.send("/corridor",
                  [length,
                   width,
                   height,
                   x, y,
                   position])