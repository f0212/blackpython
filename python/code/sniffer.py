import socket
import os
import struct
from ctypes import *



class IP(Structure):
        _fields_ = [
                ("ihl",            c_ubyte, 4),
                ("version",        c_ubyte, 4),
                ("tos",            c_ubyte),
                ("len",            c_ushort),
                ("id",             c_ushort),
                ("offset",         c_ushort),
                ("ttl",            c_ubyte),
                ("protocol_num",   c_ubyte),
                ("sum",            c_ushort),
                ("src",            c_ulong),
                ("dsc",            c_ulong)
        ]
        
        def __new__(self, socket_buffer = None):
                return self.from_buffer_copy(socket_buffer)
        
        
        def __init__(self, socket_buffer = None):
                self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
                
                self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
                self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
                
                try:
                        self.protocol = self.protocol_map[self.protocol_num]
                except:
                        self.protocol = str(self.protocol_num]
                

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

host = "192.168.0.51"
host = host.encode()

sniffer.bind((host, 0))

sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

data = sniffer.recvfrom(65535)

print (data)