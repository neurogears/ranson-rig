# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 20:44:52 2020

@author: gonca
"""

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