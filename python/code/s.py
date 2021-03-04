import socket
import os


host = "192.168.0.51"
host= host.encode()

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sniffer.bind((host, 0))

sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

try:
        while True:
                data = sniffer.recvfrom(65565)
                print (data)
except KeyboardInterrupt:
        pass
        