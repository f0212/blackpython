import  socket

target_ip = "127.0.0.1"
target_ip = target_ip.encode()
target_port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

a = "aaa"
a = a.encode()
server.sendto(a,(target_ip,target_port))
data,adddr = server.recvfrom(4064)

print (data)


import socket
import threading
import sys


def bind_serive(client):
        pass


target = "0.0.0.0"
port   = 7001
target = target.encode()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.bind((target, port))

client.listen(5)

print ("[*] Listeing %s port" % (port))
while True:
        sock, addr = client.accept()
        print ("%d:%s connect" % (addr[0], addr[1]))
        
        thread_sock = threading.Thread(target=bind_serive, args=(sock,))
        thread_sock.start()