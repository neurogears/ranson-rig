# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:44:13 2020

@author: gonca
"""

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
request_port = 4002
reply_port = 4007

client = SimpleUDPClient(ip, request_port)  # Create client
with BlockingOSCUDPServer((ip, reply_port), dispatcher) as server:
    
    client.send_message("/gratings", [0.7, 0.0, -0.5, 0.0, 10.0, 0.0, 0.0, 2.0]) # grating 1
    client.send_message("/gratings", [0.5, 45.0, 0.5, 0.0, 20.0, 0.0, 0.0, 2.0]) # grating 2
    client.send_message("/startgratings", 0)
    server.handle_request()  # Wait for end trial