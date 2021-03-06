import socket

from ip.ip_header import DEFAULT_TTL, IPHeader
from ip.ipv4 import PROTOCOL_VERSION, HEADER_LENGTH_IN_WORDS, AUTO_VALUE

DEFAULT_PACKAGE_ID = 22244


class IPPackageBuilder:
    def __init__(self, protocol, src, dest, payload):
        self.protocol = protocol
        self.src = src
        self.dest = dest
        self.payload = payload

    def build(self, ttl=DEFAULT_TTL):  # build package
        src = socket.inet_aton(self.src)
        dest = socket.inet_aton(self.dest)

        header = IPHeader(PROTOCOL_VERSION, src, dest, ttl, self.protocol, HEADER_LENGTH_IN_WORDS,
                          AUTO_VALUE, DEFAULT_PACKAGE_ID)

        return header.pack() + self.payload  # return package
