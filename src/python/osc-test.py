# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:44:13 2020

@author: gonca
"""

import rigstim
from rigstim import WallType as Wall
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/print", print_handler)
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
request_port = 4002
reply_port = 4007

client = SimpleUDPClient(ip, request_port)  # Create client
rig = rigstim.RigClient(client)
with BlockingOSCUDPServer((ip, reply_port), dispatcher) as server:
    
    rig.gratings(size=30, x=-15, y=-5, angle=0, freq=0.1, duration=2.0) # grating 1
    rig.gratings(size=15, x=15, y=-5, angle=45, freq=0.1, duration=2.0, speed=1) # grating 2
    rig.video("Blink", y=20, speed=2.0, onset=1.0, duration=2.0) # video 1
    rig.start()
    server.handle_request()  # Wait for end trial
    
    rig.gratings(size=120, angle=30, freq=0.1, duration=2.0) # go gratings
    rig.go(suppress=1000, response=500) # go trial
    server.handle_request()  # Wait for end trial

    rig.gratings(size=120, angle=0, freq=0.1, duration=2.0) # nogo gratings
    rig.nogo(suppress=500, response=500) # no-go trial
    server.handle_request()  # Wait for end trial

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
    rig.tile(Wall.FRONT, position=3, texture="mask")
    rig.corridor(length=3.0, width=1.2, height=1.0, x=0.0, y=0.0, position=0.0)
    server.handle_request()  # Wait for end trial