#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import socket

class UDPClient:

    BUFFER_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        while True:
            message = input("Input: ")
            self.socket.sendto(message.encode("utf-8"), ("127.0.0.1", 7777))
            if message == 'q':
                break


if __name__ == "__main__":
    client = UDPClient()
    client.run()