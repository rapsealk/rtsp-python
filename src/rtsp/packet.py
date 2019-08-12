#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import struct

class Packet:
    FORMAT = ">B"    # unsigned char (https://docs.python.org/3/library/struct.html#format-strings)

class RTPPacket(Packet):

    """
    Format: http://www.ktword.co.kr/word/abbr_view.php?m_temp1=3394

    Type (bit)
    * CSRC: Contributing Source
    +------------------------------------------------------------+
    | Version (2) | Padding (1) | Extension (1) | CSRC Count (4) |
    +------------------------------------------------------------+
    | Marker (1) |               Payload Type (7)                |
    +------------------------------------------------------------+
    |                       Sequence Number                      |
    |                             (16)                           |
    +------------------------------------------------------------+
    |                                                            |
    |                         Timestamp                          |
    |                            (32)                            |
    |                                                            |
    +------------------------------------------------------------+
    |                                                            |
    |            Synchronization Source ID (SSRC ID)             |
    |                             (32)                           |
    |                                                            |
    +------------------------------------------------------------+
    """

    HEADER_BYTES = 12

    VERSION = 2
    PADDING = 0
    EXTENSION = 0
    CC = 0
    MARKER = 0
    SSRC_ID = 1337  # Identifies the server

    def __init__(self, payload_type, sequence_number, timestamp=time.time()):
        """ RTP header field
            TODO: https://github.com/mutaphore/RTSP-Client-Server/blob/master/RTPpacket.java#L74-L104 """
        self.version            = RTPPacket.VERSION
        self.padding            = RTPPacket.PADDING
        self.extension          = RTPPacket.EXTENSION
        self.crsc_count         = RTPPacket.CC
        self.marker             = RTPPacket.MARKER
        self.payload_type       = payload_type
        self.sequence_number    = sequence_number
        self.timestamp          = int(timestamp)
        self.ssrc_id            = RTPPacket.SSRC_ID
        #self.payload_size = 0
        #self.payload = b''
        """ RTP header """
        self.pack_header()

    def pack_header(self):
        self.header = b''
        self.header += struct.pack(Packet.FORMAT, self.version << 6 | self.padding << 5 | self.extension << 4 | self.crsc_count)
        self.header += struct.pack(Packet.FORMAT, self.marker << 7 | self.payload_type & 0b01111111)
        self.header += struct.pack(Packet.FORMAT, self.sequence_number >> 8)
        self.header += struct.pack(Packet.FORMAT, self.sequence_number & 0xFF)
        self.header += struct.pack(Packet.FORMAT, self.timestamp >> 24)
        self.header += struct.pack(Packet.FORMAT, self.timestamp >> 16 & 0xFF)
        self.header += struct.pack(Packet.FORMAT, self.timestamp >> 8 & 0xFF)
        self.header += struct.pack(Packet.FORMAT, self.timestamp & 0xFF)
        self.header += struct.pack(Packet.FORMAT, self.ssrc_id >> 24)
        self.header += struct.pack(Packet.FORMAT, self.ssrc_id >> 16)
        self.header += struct.pack(Packet.FORMAT, self.ssrc_id >> 8)
        self.header += struct.pack(Packet.FORMAT, self.ssrc_id & 0xFF)
    
    def unpack_header(self):
        unpacked = struct.unpack(Packet.FORMAT, self.header[0:1])
        self.version = (unpacked[0] & 0b11000000) >> 6
        self.padding = (unpacked[0] & 0b00100000) >> 5
        self.extension = (unpacked[0] & 0b00010000) >> 4
        self.crsc_count = unpacked[0] & 0b00001111
        unpacked = struct.unpack(Packet.FORMAT, self.header[1:2])
        self.marker = (unpacked[0] & 0b10000000) >> 7
        self.payload_type = unpacked[0] & 0b01111111
        unpacked = struct.unpack(">H", self.header[2:4])
        self.sequence_number = unpacked[0]
        unpacked = struct.unpack(">I", self.header[4:8])
        self.timestamp = unpacked[0]
        unpacked = struct.unpack(">I", self.header[8:12])
        self.ssrc_id = unpacked[0]

    def print(self, file=sys.stdout):
        args = (self.version, self.padding, self.extension, self.crsc_count,
                self.marker, self.payload_type, self.sequence_number, self.timestamp)
        message = """
        [RTPPacket Header]
        - Version: %d
        - Padding: %d
        - Extension: %d
        - CC: %d
        - Marker: %d
        - Payload type: %d
        - Sequence number: %d
        - Timestamp: %d
        """ % args
        try:
            file.write(message)
        except Exception as e:
            sys.stderr.write("%s\n" % e)