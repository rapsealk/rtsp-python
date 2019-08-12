#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/src'
sys.path.append(PATH)
from rtsp.packet import RTPPacket
from rtcp.packet import RTCPPacket

import unittest

class TestRTPPacket(unittest.TestCase):

    def test_bytes_format(self):
        packet = RTPPacket(0, 0)
        self.assertEqual(RTPPacket.HEADER_BYTES, len(packet.header))

    def test_header_unpack(self):
        import copy
        packet = RTPPacket(0, 0)
        packet2 = copy.deepcopy(packet)
        packet.unpack_header()
        self.assertEqual(packet.version, packet2.version)
        self.assertEqual(packet.padding, packet2.padding)
        self.assertEqual(packet.extension, packet2.extension)
        self.assertEqual(packet.crsc_count, packet2.crsc_count)
        self.assertEqual(packet.marker, packet2.marker)
        self.assertEqual(packet.payload_type, packet2.payload_type)
        self.assertEqual(packet.sequence_number, packet2.sequence_number)
        self.assertEqual(packet.timestamp, packet2.timestamp)
        self.assertEqual(packet.ssrc_id, packet2.ssrc_id)

    def test_print(self):
        packet = RTPPacket(0, 0)
        packet.print()
        
class TestRTCPPacket(unittest.TestCase):

    def test_packet_bytes(self):
        packet = RTCPPacket(0, 0, 0)
        self.assertEqual(len(packet.header), RTCPPacket.HEADER_BYTES)
        self.assertEqual(len(packet.body), RTCPPacket.BODY_BYTES)

    def test_print(self):
        packet = RTCPPacket(0, 0, 0)
        packet.print()

    def test_from_bytes(self):
        packet = RTCPPacket(0, 0, 0)
        packet2 = RTCPPacket.from_bytes(packet.header + packet.body)
        packet2.print()

if __name__ == "__main__":
    unittest.main()