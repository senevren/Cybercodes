#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        # We are creating a session object which represents our current session.
        # After get request method is done session is closed but thanks to session object it continues.
        self.target_url = url
        self.target_links =[]
        self.links_to_ignore = ignore_links # We want to ignore the logout link to prevent from being logged out.

    def extract_links_from(self, url):
        response = self.session.requests.get(url)
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

    def crawl(self, url=None):
        if url == None:
            url = self.target_url

        href_links = self.extract_links_from(self, url)
        print(href_links)

        for link in href_links:
            link = urlparse.urljoin(self.target_url, link)
            # We are combining relative links with the base link of the website.
            if "#" in link:
                link = link.split('#')[0]
            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                # This way we are preventing the repeated links.
                self.target_links.append(link)
                print(link)
                # We are purging the other redirection website links other than our target website.
                self.crawl(link)
    def extract_forms(self, url):
        # We are extracting forms from a specific url.
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content)
        return parsed_html.findAll("form")

    def submit_forms(self, form, value, url):
        # We are submitting some values into the forms we have extracted by way of extract_forms method.
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        # In the case that only the relative part is displayed in the action.
        method = form.get("method")

        input_list = form.findAll("input")
        post_data = {}
        for input in input_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)
    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_vulnerable_to_xss =self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link + "in the following ")
                    print(form)
            if "=" in link:
                print("[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link)

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        url = url.replace("=","=" + xss_test_script)
        response = self.session.get(url)
        # Because we want to stay in the same session, not wanting to start a new session.
        return xss_test_script.encode() in response.content
    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        response = self.submit_forms(form, xss_test_script, url)
        return xss_test_script.encode() in response.content
        # It will return True or a False value.





