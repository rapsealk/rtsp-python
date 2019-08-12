#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import socket
import uuid

class RTSPServer:

    MJPEG_TYPE = 26

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", 8080))


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    port = args.port
    print(port)
    server = RTSPServer()