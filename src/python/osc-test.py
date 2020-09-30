# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:44:13 2020

@author: gonca
"""

import rigstim
from rigstim import WallType as Wall
from rigstim import TriggerType as Trigger
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
    rig.go(0.5) # go trial
    server.handle_request()  # Wait for end trial

    rig.gratings(size=120, angle=0, freq=0.1, duration=2.0) # nogo gratings
    rig.nogo(0.5) # no-go trial
    server.handle_request()  # Wait for end trial

    rig.tile(Wall.LEFT, position=0, extent=1, texture="White",
             interaction=Trigger.REWARD_ON_LICK, argument=2, repetitions=1) 
    rig.tile(Wall.RIGHT, position=0, extent=1, texture="Black",
             interaction=Trigger.END_ON_LICK, argument=3000, repetitions=3)
    rig.tile(Wall.LEFT, position=1, extent=1, texture="Black",
             interaction=Trigger.TELEPORT_ON_LICK, argument=3.0, repetitions=3)
    rig.tile(Wall.RIGHT, position=1, extent=1, texture="White",
             interaction=Trigger.REWARD_ON_ENTRY, argument=1000.0, repetitions=2)
    rig.tile(Wall.LEFT, position=2, extent=1, texture="White",
             interaction=Trigger.END_ON_ENTRY, argument=2000.0)
    rig.tile(Wall.RIGHT, position=2, extent=1, texture="Black",
             interaction=Trigger.TELEPORT_ON_ENTRY, repetitions=2)
    rig.tile(Wall.TOP, position=1, extent=1, texture="Black",
             interaction=Trigger.CHANGE_GAIN_ON_ENTRY, argument=0.1)
    rig.tile(Wall.FRONT, position=3, texture="mask")
    rig.corridor(length=3.0, width=1.2, height=1.0, position=0.0)
    server.handle_request()  # Wait for end trial