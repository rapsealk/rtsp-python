#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import zlib
try:
    import cPickle as pickle
except:
    import pickle

import cv2
import numpy as np

class TestCompression(unittest.TestCase):

    def test_zlib_compress(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened:
            cap.open(0)
        ret, frame = cap.read()
        print('frame.shape:', frame.shape)
        frame = frame.flatten()
        frame = pickle.dumps(frame)
        print('len(frame):', len(frame))
        compressed = zlib.compress(frame, 5)
        print('len(compressed):', len(compressed))
        self.assertLess(len(compressed), len(frame), msg="Not compressed!")

    def test_zlib_decompress(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened:
            cap.open(0)
        ret, frame = cap.read()
        shape = frame.shape
        print('frame.shape:', frame.shape)
        bframe = frame.flatten()
        bframe = pickle.dumps(bframe)
        print('len(frame):', len(bframe))
        compressed = zlib.compress(bframe, 5)
        print('len(compressed):', len(compressed))
        decompressed = zlib.decompress(compressed)
        print('len(decompressed):', len(decompressed))
        dframe = pickle.loads(decompressed)
        dframe = np.reshape(dframe, shape)
        print('dframe.shape:', dframe.shape)
        self.assertGreaterEqual(len(decompressed), len(compressed), msg="Wrongly decompressed..")
        self.assertEqual(len(decompressed), len(bframe))
        self.assertEqual(frame.shape, dframe.shape)
        

if __name__ == "__main__":
    unittest.main()