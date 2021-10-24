#!/usr/bin/env python
import requests
url = "example.com"
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass
with open("/root/Downloads/subdomains-wordlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + url
        response = request(test_url)
        if response:
            print("[+] Discovered a subdomain-->" + test_url)
