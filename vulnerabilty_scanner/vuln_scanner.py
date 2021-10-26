#!/usr/bin/env pyhton
import scanner

target_url = "http://example.com"
data_dict = {"username":"admin", "password":"password", "login":"submit"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post("login url", data=data_dict)
vuln_scanner.crawl()
vuln_scanner.run_scanner()
