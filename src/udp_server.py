#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import sys
import socket

class UDPServer:

    BUFFER_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", 7777))

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(UDPServer.BUFFER_SIZE)
            data = data.decode("utf-8")
            sys.stdout.write("server received: [%s]\n" % data)
            if data == 'q':
                break


if __name__ == "__main__":
    server = UDPServer()
    server.run()