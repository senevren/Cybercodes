#!/usr/bin/env python
# coding: utf-8

# In[19]:


import scapy.all as scapy

def scan(ip):

    arp_request = scapy.ARP(pdst=ip) 
    broadcast = scapy.Ether(dest='ff:ff:ff:ff:ff:ff')
    arp_request_boadcast = broadcast/ arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_boadcast, timeout=1,verbose=False)[1]
    print(answered_list.summary())
    
    print('IP\t\t\t\tMAC Address\n............')
    client_list =[]
    
    for element in answered_list:
        client_dict ={'ip': element[1].psrc, 'MAC' : element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(results_list):
    print('IP\t\t\tMAC Address\n............................')
    for client in results_list:
        print(client['ip'] + '\t\t' + client['MAC'])
scan_result = scan('10.0.0.1/24')
print_result(scan_result)
    #print(arp_request.summary()) #Use this to see the result of the function
    #print(scapy.ls(scapy.ARP())) # This gives us all the fileds that we can set


# In[ ]:



