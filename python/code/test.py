import sys
import socket
import threading
import time


FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump2(src, length=8):
        src = src.decode()
        result=[]
        for i in range(0, len(src), length):
                s = src[i:i+length]
                hexa = ' '.join(["%02X"%ord(x) for x in s])
                printable = s.translate(FILTER)
                result.append("%04X   %-*s   %s\n" % (i, length*3, hexa, printable))
        return ''.join(result)


def local_replace(buffer):
        
        return buffer

def remote_replace(buffer):
        
        return buffer

def recvive_from(connection):
        buffer = ""
        
       
        connection.settimeout(5)

        try:
                while True:
                        
                        data = connection.recv(4096)
                        data = data.decode()

                        if not data:
                                break
                        
                        buffer += data
                        
        except:
                pass

        return buffer.encode()


def proxy_handler(local_socket,remote_host,remote_port,yanzheng):
        global remote_socket
        global remote_buffer
        
        
        try:
              
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((remote_host, remote_port))             
                               
        except:
                print ("[!!] 未建立连接 检查目标是否为开放状态")
                sys.exit(0)

        data = "[*] 成功建立连接\n\n[*] exit 断开连接\n\n"
        data = data.encode()
        local_socket.send(data)
        remote_socket.send(data)
                             
        
        if yanzheng:
                remote_data = ""
                
                a = "[*] 输入验证信息 "
                a = a.encode()
                print ("[==>] %s" % (a))
        
                local_socket.send()
                local_socket.send(a)
                
                a = "[*] overo 结束验证"
                a = a.encode()
                print ("[==>] %s" % (a))
                print()
                local_socket.send(a)
                
                data = recvive_from(remote_socket)
                print (data)
                data = data.encode()                
                local_socket.send(data)
                print ("1")                
                
                a = "#$"
                a = a.encode()
                local_socket.send(a)
                
                
                buffer = recvive_from(local_socket)
                
                
                while buffer not in ("overo"):
                        
                        print (buffer)
                       # buffer = buffer.encode()
                        remote_socket.send(buffer)
                        
                        reomte_data = recvive_from(remote_socket)
                        
                        print (remote_data)
                        remote_data = remote_data.encode()
                        local_socket.send(remote_data)
                        
                        a = "#$"
                        a = a.encode()                        
                        local_socket.send(a)
                        
                        buffer = recvive_from(local_socket)                      
                                               
        
        
        local_buffer  = ""
        remote_buffer = ""        
        
        while True:
                
                print ()
                local_buffer  = recvive_from(local_socket)
                remote_buffer = recvive_from(remote_socket) 
                remote_buffer = remote_buffer.decode()
                local_buffer  = local_buffer.decode()                
                
                if "exit" in remote_buffer:
                        data = "[!!]连接断开\n"
                        data = data.encode()
                        data = "[!!]对方已将连接断开\n"
                        data = data.encode()
                        remote_socket.send(data)
                        
                        local_socket.close()
                        remote_socket.close()
                        sys.exit()
                if "exit" in local_buffer:
                        data = "[!!]连接断开\n"
                        data = data.encode()
                        local_socket.send(data)
                        data = "[!!]对方已将连接断开\n"
                        data = data.encode()
                        remote_socket.send(data)
                                
                        local_socket.close()
                        remote_socket.close()
                        sys.exit()  
                
                remote_buffer = remote_buffer.encode()
                local_buffer  = local_buffer.encode()                
                
                if len(local_buffer):
                        
                        print ("[==>] 发送数据 %s " % (local_buffer))
                        
                     #   local_buffer.encode()
                        print ()
                        a = dump2(local_buffer)
                        print (a)
                        remote_socket.send(local_buffer)
                        
                        print ("[==>] 发送到远端主机")
                        
                        
                
                print ()
                
                if len(remote_buffer):
                        
                        print ("[<==] 接受数据 %s " % (remote_buffer))
                      # remote_buffer.encode()
                        print ()
                        a = dump2(remote_buffer)
                        print (a)
                        local_socket.send(remote_buffer)
                        
                        print ("[<==] 发送本地主机")
        
                
                        
                        
                #if not len(local_buffer) or not len(remote_buffer):
                #        print ("[!!] 未检测到数据")
                 #       print ("[!!] 断开连接")
                  #      local_socket.close()
                   #     remote_socket.close()   
                    #    sys.exit(0)
                        
                        
                        
def server_loop(local_host,local_port,remote_host, remote_port, yanzheng):
        
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #try:
                #local_socket.bind((local_host,local_port))
        #except:
                #print ("[!!]")
                #sys.exit(0)
        local_socket.bind((local_host,local_port))        
        print ("[*] %s %d 启动侦听 " % (local_host,local_port))
        
        local_socket.listen(5)
        
        while True:
                client, addr = local_socket.accept()
                print ("[*] %s:%d 已连接 " % (addr[0], addr[1]))
                prxoy_thread = threading.Thread(target=proxy_handler,args=(client,remote_host,remote_port,yanzheng,))
                prxoy_thread.start()
        
        

      
def main():
        global local_host
        global local_port
        global remote_host
        global remote_port
        
        
        if len(sys.argv) != 6:
                
                print ("使用方法: ./proxy.py 侦听主机 侦听端口 远程主机 远程端口 是否验证")
                print ("实例:")
                print ("./proxy.py 0.0.0.0 7001 192.168.0.1 21 Ture")
                sys.exit(0)
        
        local_host  = sys.argv[1]
        local_port  = int(sys.argv[2])
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])        
        yanzheng = sys.argv[5] 
        
        if local_host not in ("127.0.0.1","0.0.0.0"):
                
                print ("[!!]local_host is  0.0.0.0 / 127.0.0.1 ")
                sys.exit(0)
                
        
        local_host  = local_host.encode()
        remote_host = remote_host.encode()        
        
        
        if "Ture" not in yanzheng:
                yanzheng = False
        else:
                yanzheng = True
        
        
        server_loop(local_host,local_port,remote_host, remote_port, yanzheng)
                


main()

