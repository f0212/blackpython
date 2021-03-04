import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip,username=user,password=passwd)
        
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
                while True:
                        command = input("#$")
                        ssh_session.exec_command(command)
                        print (ssh_session.recv(1024))
                
        return
        
ssh_command("192.168.0.11","root","vv")