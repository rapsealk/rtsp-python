#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from abc import ABCMeta, abstractmethod

RPI = sys.platform == "linux"

if sys.platform == "linux":
    import picamera
    import picamera.array
elif sys.platform == "darwin" or sys.platform == "win32":
    import cv2
    import numpy as np

try:
    import cPickle as pickle
except:
    import pickle
import zlib

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

class BaseCamera(object):

    __meta__ = ABCMeta

    @abstractmethod
    def capture(self):
        pass

class RpiCamera(BaseCamera):
    
    def __init__(self, size=(IMAGE_WIDTH, IMAGE_HEIGHT)):
        self.camera = picamera.PiCamera()
        self.camera.resolution = size
        self.stream = picamera.array.PiRGBArray(self.camera)

    def capture(self):
        while True:
            self.camera.capture(self.stream, 'bgr', use_video_port=True)
            shape = self.stream.array.shape # (height, width, channel)
            yield self.stream.array
            self.stream.seek(0)
            self.stream.truncate()

class CvCamera(BaseCamera):

    def __init__(self, size=(IMAGE_WIDTH, IMAGE_HEIGHT)):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        #self.camera.set(cv2.CAP_PROP_FPS, FPS)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def capture(self):
        while self.camera.isOpened:
            ret, frame = self.camera.read()
            print(frame.shape)
            """
            frame = frame.flatten()
            frame = pickle.dumps(frame)
            frame = pickle.loads(frame)
            print(len(frame))
            frame = np.reshape(frame, (IMAGE_HEIGHT, IMAGE_WIDTH, 3))
            """
            yield frame

    def compress(self, data: bytes, level=5) -> bytes:
        assert(type(data) == bytes)
        return zlib.compress(data, level)

    def decompress(self, data: bytes) -> bytes:
        return zlib.decompress(data)

class CameraFactory:
    @staticmethod
    def get_camera():
        if sys.platform == "linux":
            return RpiCamera(size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        return CvCamera(size=(IMAGE_WIDTH, IMAGE_HEIGHT))


if __name__ == "__main__":
    camera = CameraFactory.get_camera()    
    generator = camera.capture()
    while True:
        frame = next(generator)
        cv2.imshow("CvCamera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break