import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_ip = bind_ip.encode()
server.bind((bind_ip,bind_port))

server.listen(5)

print ("[*] Listening on %s:%d" % (bind_ip,bind_port))

def handle_client(client_socket):
        
        request = client_socket.recv(1024)
        
        print ("[*] Received: %s" % request )
       
        ack = "ACK!"
        ack = ack.encode()
        client_socket.send(ack)
        client_socket.close()

while True:
        
        client,addr = server.accept()
        
        print ("[*] Accepted connection from : %s:%d" % (addr[0],addr[1]))
        
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()