import socket
import sys
import paramiko
import threading

class Server(paramiko.ServerInterface):
        def __init__(self):
                self.event = threading.Event()
                
        def check_channel_request(self, kind, chanid):
                if kind == 'session':
                        return paramiko.OPEN_SUCCEEDED
                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
        def check_auth_password(self, username, password):
                if (username == 'root' and password == 'vv'):
                        return paramiko.AUTH_SUCCESSFUL
                
                return paramiko.AUTH_FAILED

server   = sys.argv[1]
ssh_port = sys.argv[2]

try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)