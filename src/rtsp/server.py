#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import socket
import uuid
from threading import Thread

import cv2
import numpy as np

from util.camera import CameraFactory

class RTSPServer:

    MJPEG_TYPE = 26

    def __init__(self, port=8080, preview=False):
        self.preview = preview
        self.camera = CameraFactory.get_camera()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", port))

    def __del__(self):
        #self.command_thread.do_run = False
        #self.preview_thread.do_run = False
        #self.command_thread.join()
        #self.preview_thread.join()
        self.socket.close()

    def command(self):
        while True:
            command = input("Command: ")
            if command == 'q':
                self.command_thread.do_run = False
                self.preview_thread.do_run = False

    def run(self):
        self.command_thread = Thread(target=self.command)
        self.command_thread.daemon = True
        self.command_thread.start()

        self.preview_thread = Thread(target=self.run_camera)
        self.preview_thread.daemon = True
        if self.preview:
            self.preview_thread.start()

        self.command_thread.join()
        self.preview_thread.join()

    def run_camera(self):
        frame_generator = self.camera.capture()
        while True:
            frame = next(frame_generator)
            cv2.imshow('camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--preview", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    """
    args = parse_args()
    server = RTSPServer(port=args.port, preview=args.preview)
    server.run()
    """
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.release()