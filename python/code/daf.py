import sys 
import subprocess
import socket
import getopt
import threading

target     = ""
port       = 4444
cmd        = False
upload     = False
licent     = False
upload_dit = ""
execute    = ""


def tis():
        print ("--------------NC 中文版------------")
        print ("帮助: ncc.py -t 目标  -p 端口")
        print ("-l  监 听                            在[host]：[port]上侦听传入连接")
        print ("-e  运行文件绝对路径                 在接收到连接时执行给定的文件")
        print ("-c                                   初始化命令shell")
        print ("-u  上传文件路径                     收到连接后，上传文件并写入[目的地]")
        
        print ()
        print ()
        
        print ("例如：")
        print ("ncc.py -t 192.168.0.1 -p 1234 -c ")
        print ("ncc.py -t 192.168.0.1 -p 1234 -u=/home/targe       t.exe")
        print ("ncc.py -t 192.168.0.1 -p 1234 -e=\"cat /etc/passwd\" ")
        print ("echo \"Hello\" | ncc.py -t 192.168.0.1 -p 1234")


def main():
        

        global target
        global port
        global licent
        global execute
        global cmd
        global upload_dit
        
        if not (sys.argv[1:]):
                tis()
                sys.exit()
        
        
        try:    
                opts, aa = getopt.getopt(sys.argv[1:],"t:p:le:cu:h",["help"])
        except getopt.GetoptError as err:
                print (err)
                sys.exit()
        
        for o, v in opts:
                if o in ("-h","--help"):
                        tis()
                elif o in ("-t"):
                        target = v
                elif o in ("-c"):
                        cmd = True
                elif o in ("-l"):
                        licent = True
                elif o in ("-u"):
                        upload_dit = v
                elif o in ("-p"):
                        port = int(v)
                elif o in ("-e"):
                        execute = v
                else:
                        assert False, "未知参数"

        if not licent and len(target) and port:
                
                print ("[*] Ctrl + D 尝试连接")
                buffer = sys.stdin.read()
                server_socket(buffer)
        
        if licent:
                bind_handler()
                

def server_socket(buffer):
        
        global target
        global port
   
        target = target.encode()
        buffer = buffer.encode()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
                client.connect((target,port))

                if buffer:
                        client.send(buffer)
                
                while True:
                        recv_len = 1
                        response = ""
                        while recv_len:
                                data = client.recv(4096)
                                recv_len = len(data)
                                data = data.decode()
                                response = response + data
                                if recv_len < 4096:
                                        break

                        print (response)
                        
                        buffer = input("")
                        buffer += "\n"
                        buffer = buffer.encode()
                        client.send(buffer)
        except:
                print ("[*] 未建立连接")
                sys.exit()
                
def bind_handler():
        
        global target
        global port

                
        if not target:
                target = "0.0.0.0"
        
        target = target.encode()
        bind_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        bind_client.bind((target,port))
        bind_client.listen(5)
        print ("[*] %s 开始侦听端口" % (port))
        
        try :
                while True:
                        client, addr = bind_client.accept()
                        print ("[*] %s:%d  已连接 " % (addr[0],addr[1]))
                        
                        socket_thread = threading.Thread(target=bind_socket,args=(client,))
 
                        socket_thread.start()
        except:
                print ("[*] 未建立连接")
                sys.exit()



def run_command(cmd):
        try:
                optout = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
        except:
                optout = "[*] 命令执行错误"
                
        return optout


def bind_socket(client):
        
        global execute
        global upload_dit
        global upload
        global cmd
        
        a = "建立连接"
        a = a.encode()
        client.send(a)
        
        if len(execute):
                execute = execute.encode()
                response = run_command(execute)
                client.send(response)
                client.close()

        if cmd:
                while True:
                        a = "#"
                        a = a.encode()
                        client.send(a)
                        cmd_buffer = ""
                          
                        cmd_buffer = client.recv(4096)                        
                        cmd_buffer = cmd_buffer.decode()
                        
                        response = run_command(cmd_buffer)
                        client.send(response)
                        
                        
        if len(upload_dit):                          
                file_buffer = ""
                
                while True:
                        
                        data = client.recv(4096)
                        data = data.decode()
                     
                        file_buffer += data
                        
                        if not data:
                                break
                        
                try:
                        
                        file_open = open(upload_dit,"wb")
                        file_buffer = file_buffer.encode()
                        file_open.write(file_buffer)
                
                        file_open.close()
                        
                        print("[*] 文件写入成功")
                except:
                        print("[*] 文件写入失败")
                
main()