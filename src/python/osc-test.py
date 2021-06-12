# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:44:13 2020

@author: gonca
"""

import rigstim
from datetime import datetime
from rigstim import WallType as Wall
from pyOSC3fix.OSC3 import OSCStreamingClient
import threading
import time

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

ip = "127.0.0.1"
request_port = 4002

sessiontime = datetime.now()
metadata = "{0}_{1}-{2}-{3}_S1".format(
        sessiontime.date(),
        sessiontime.hour,
        sessiontime.minute,
        sessiontime.second)
client = OSCStreamingClient()  # Create client
try:
    client.connect((ip, request_port))
    rig = rigstim.RigClient(client)
    rig.dataset('Data')

    rig.resource("Videos/Blink")
    rig.preload()
    
    rig.experiment(metadata)
    rig.gratings(size=30, x=-15, y=-5, angle=0, freq=0.1, duration=2.0) # grating 1
    rig.gratings(size=15, x=15, y=-5, angle=45, freq=0.1, duration=2.0, speed=1) # grating 2
    rig.video("Blink", y=20, speed=2.0, onset=1.0, duration=2.0) # video 1
    rig.start()

    rig.receive()  # Wait for end trial
    rig.clear()
    
    rig.experiment(metadata)
    rig.gratings(size=120, angle=30, freq=0.1, duration=2.0) # go gratings
    rig.go(suppress=1000, start=500, duration=1000.0, threshold=2) # go trial
    rig.receive()  # Wait for end trial

    rig.experiment(metadata)
    rig.gratings(size=120, angle=0, freq=0.1, duration=2.0) # nogo gratings
    rig.nogo(suppress=500, start=0.0, duration=2000.0) # no-go trial
    rig.receive()  # Wait for end trial

    rig.experiment(metadata)
    rig.interaction('rewardLick', [2, 1]) # lickthreshold, max activations
    rig.interaction('endLick', [3, 3000.0]) # lickthreshold, delay
    rig.tile(Wall.LEFT, position=0, extent=1, texture="White")
    rig.tile(Wall.RIGHT, position=0, extent=1, texture="Black")
    
    rig.interaction('teleportLick', [0.0, 3, 3])
    rig.tile(Wall.LEFT, position=1, extent=1, texture="Black")
    
    rig.interaction('rewardEntry', [1000.0, 2])
    rig.tile(Wall.RIGHT, position=1, extent=1, texture="White")
    
    rig.interaction('endEntry', 2000.0)
    rig.tile(Wall.LEFT, position=2, extent=1, texture="White")
    
    rig.interaction('teleportEntry', [0.0, 2])
    rig.tile(Wall.RIGHT, position=2, extent=1, texture="Black")
    
    rig.interaction('gainEntry', [0.1, 1])
    rig.tile(Wall.TOP, position=1, extent=1, texture="Black")
    rig.corridor(length=3.0, width=1.2, height=1.0, x=0.0, y=0.0, position=0.0)
    rig.receive()  # Wait for end trial
    
    rig.experiment(metadata)
    rig.replay(metadata, 3)
    rig.receive()  # Wait for end trial

    rig.experiment(None)
finally:
    client.close()