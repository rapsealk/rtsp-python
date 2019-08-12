#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import struct

class RTCPPacket:

    """
            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    header |V=2|P|    RC   |   PT=RR=201   |             length            |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |                     SSRC of packet sender                     |
           +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
    report |                           fraction lost                       |
    block  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      1    |              cumulative number of packets lost                |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |           extended highest sequence number received           |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |                      interarrival jitter                      |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |                         last SR (LSR)                         |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |                   delay since last SR (DLSR)                  |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """

    FORMAT = ">B"

    HEADER_BYTES = 8
    BODY_BYTES = 24

    VERSION = 2
    PADDING = 0
    RC      = 1 # Reception Report Count (1 for one receiver)
    PAYLOAD_TYPE = 201  # 201 for Receiver Report

    def __init__(self, fraction_loss, cumulative_loss, highest_sequence_number):
        self.version = RTCPPacket.VERSION
        self.padding = RTCPPacket.PADDING
        self.rc = RTCPPacket.RC
        self.payload_type = RTCPPacket.PAYLOAD_TYPE
        self.length = RTCPPacket.HEADER_BYTES + RTCPPacket.BODY_BYTES
        
        self.ssrc = 0
        
        self.fraction_loss = fraction_loss
        self.cumulative_loss = cumulative_loss
        self.highest_sequence_number = highest_sequence_number

        self.pack_header()
        self.pack_body()

    @staticmethod
    def from_bytes(packet):
        header = packet[:RTCPPacket.HEADER_BYTES]
        body = packet[RTCPPacket.HEADER_BYTES:RTCPPacket.BODY_BYTES]

        version = (struct.unpack(RTCPPacket.FORMAT, header[0:1])[0] & 0xFF) >> 6
        payload_type = struct.unpack(RTCPPacket.FORMAT, header[1:2])[0] & 0xFF
        length = struct.unpack(">H", header[2:4])[0]
        ssrc = struct.unpack(">I", header[4:8])[0]

        unpacked = struct.unpack(">f", body[:4])
        print("unpacked:", unpacked)
        fraction_loss = unpacked[0]
        cumulative_loss = struct.unpack(">i", body[4:8])[0]
        highest_sequence_number = struct.unpack(">i", body[8:12])[0]

        rtcp = RTCPPacket(fraction_loss, cumulative_loss, highest_sequence_number)
        rtcp.version = version
        rtcp.payload_type = payload_type
        rtcp.length = length
        rtcp.ssrc = ssrc

        return rtcp

    def pack_header(self):
        self.header = b''
        self.header += struct.pack(RTCPPacket.FORMAT, self.version << 6 | self.padding << 5 | self.rc)
        self.header += struct.pack(RTCPPacket.FORMAT, self.payload_type & 0xFF)
        self.header += struct.pack(RTCPPacket.FORMAT, self.length >> 8)
        self.header += struct.pack(RTCPPacket.FORMAT, self.length & 0xFF)
        self.header += struct.pack(RTCPPacket.FORMAT, self.ssrc >> 24)
        self.header += struct.pack(RTCPPacket.FORMAT, self.ssrc >> 16 & 0xFF)
        self.header += struct.pack(RTCPPacket.FORMAT, self.ssrc >> 8 & 0xFF)
        self.header += struct.pack(RTCPPacket.FORMAT, self.ssrc & 0xFF)

    def pack_body(self):
        self.body = b''
        self.body += struct.pack(">f", self.fraction_loss)
        self.body += struct.pack(">i", self.cumulative_loss)
        self.body += struct.pack(">i", self.highest_sequence_number)
        # Make sure that body is 24 bytes.
        self.body += bytes(RTCPPacket.BODY_BYTES)[:RTCPPacket.BODY_BYTES-len(self.body)]

    def print(self, file=sys.stdout):
        args = (self.version, self.fraction_loss, self.cumulative_loss, self.highest_sequence_number)
        message = """
        [RTCPPacket Header]
        - Version: %d
        - Fraction Loss: %d
        - Cumulative Loss: %d
        - Highest Sequence Number: %d
        """ % args
        try:
            file.write(message)
        except Exception as e:
            sys.stderr.write("%s\n" % e)