# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:44:13 2020

@author: gonca
"""

import rigstim
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
    client.send_message("/start", 0)
    server.handle_request()  # Wait for end trial
    
    rig.gratings(size=120, angle=30, freq=0.1, duration=2.0) # go gratings
    client.send_message("/go", [30.0, 2.0, 0.5]) # go trial
    server.handle_request()  # Wait for end trial

    rig.gratings(size=120, angle=0, freq=0.1, duration=2.0) # nogo gratings
    client.send_message("/nogo", [0.0, 2.0, 0.5]) # no-go trial
    server.handle_request()  # Wait for end trial
    
    client.send_message("/tile", [0, 1.25, 1.0, "Black", 0])
    client.send_message("/tile", [1, 1.25, 1.0, "White", 0])
    client.send_message("/tile", [0, 2.25, 1.0, "White", 0])
    client.send_message("/tile", [1, 2.25, 1.0, "Black", 0])
    client.send_message("/tile", [2, 1.25, 1.0, "Black", 0])
    client.send_message("/tile", [3, 1.25, 1.0, "mask", 0])
    client.send_message("/startcorridor", 10.0)
    server.handle_request()  # Wait for end trial