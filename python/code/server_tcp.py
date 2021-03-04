import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999
bind_ip = bind_ip.encode()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))
server.listen(5)

print ("[*] Listening on %s:%d" % (bind_ip,bind_port))

def handler_client(client_socket):
        recvs = client_socket.recv(1024)
        print ("[*] Received %s " % (recvs))
        
        ack = "ACK!"
        ack = ack.encode()
        
        client_socket.send(ack)
        client_socket.close()
        

while True:
        client, addr = server.accept()
        print ("[*] Accepted connection from : %s:%d" % (addr[0],addr[1]))
        
        client_handler = threading.Thread(target=handler_client,args=(client,))
        client_handler.start()
        