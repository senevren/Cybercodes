#!/usr/bin/env python
import requests
import re
import urllib.parse as urlparse



target_url = "http://shippinglot.com"
target_links =[]

def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

def crawl(url):

    href_links = extract_links_from(url)
    print(href_links)

    for link in href_links:
        link = urlparse.urljoin(target_url, link)
        # We are combining relative links with the base link of the website.
        if "#" in link:
            link = link.split('#')[0]
        if target_url in link and link not in target_links:
            # This way we are preventing the repeated links.
            target_links.append(link)
            print(link)
            # We are purging the other redirection website links other than our target website.
            crawl(link)
crawl(target_url)
