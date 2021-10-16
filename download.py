#!/usr/bin/env python
import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    # split method returns a list and we need to know last element of this list as a file extension.
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

download("ENTER A URL")
