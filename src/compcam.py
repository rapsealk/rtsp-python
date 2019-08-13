#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pickle
import zlib

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

class CvCamera:

    def __init__(self, size=(IMAGE_WIDTH, IMAGE_HEIGHT)):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        #self.camera.set(cv2.CAP_PROP_FPS, FPS)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def run(self):
        while self.camera.isOpened:
            ret, frame = self.camera.read()
            cv2.imshow('frame', frame)
            # Process
            dframe = frame.flatten()
            dframe = pickle.dumps(dframe)
            print('len(original):', len(dframe))
            dframe = zlib.compress(dframe, level=5)
            print('len(compressed):', len(dframe))
            dframe = zlib.decompress(dframe)
            dframe = pickle.loads(dframe)
            dframe = np.reshape(dframe, frame.shape)
            cv2.imshow('decompressed', dframe)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    camera = CvCamera()
    camera.run()