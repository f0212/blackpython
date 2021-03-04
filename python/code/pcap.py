from scapy.all import  *
import sys
import time


pcap_file = "/home/zy/arp.pcap"

a = rdpcap(pcap_file)

sessions = a.sessions()

for session in sessions:
        http_paylaod = ""
        
        for packet in sessions[session]:
                for v in packet:
                        try:
                                if v[TCP].dport == 80 or v[TCP].sport == 80:
                                        data = v[TCP].payload
                                        print (data)
                                        http_paylaod += data
                        except:
                                pass
        
        
print ("1" + http_paylaod)