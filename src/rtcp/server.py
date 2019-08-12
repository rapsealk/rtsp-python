#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import sys
import socket

class RTCPServer:

    BUFFER_SIZE = 4096

    def __init__(self, port=19001):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", port))

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(RTCPServer.BUFFER_SIZE)
            sys.stdout.write("[RTCP from %d] %s\n" % (addr, data.decode("utf-8")))
            


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    port = args.port
    server = RTCPServer(port)