# tos = dscp
# ecn - unused
# options - unused
import socket

PROTOCOL_VERSION = 4
HEADER_LENGTH_IN_WORDS = 5
AUTO_VALUE = 0
NO_FRAGMENTATION = 2


class IPv4Header:
    def __init__(self, version, src, dest, ttl, protocol=AUTO_VALUE, ihl=HEADER_LENGTH_IN_WORDS, dscp=AUTO_VALUE,
                 total_length=AUTO_VALUE, identification=AUTO_VALUE, flags=NO_FRAGMENTATION, fragment_offset=AUTO_VALUE,
                 checksum=AUTO_VALUE):
        self.version = version
        self.ihl = ihl
        self.dscp = dscp
        self.total_length = total_length
        self.identification = identification
        self.flags = flags
        self.fragment_offset = fragment_offset
        self.ttl = ttl
        self.protocol = protocol
        self.checksum = checksum
        self.src = src
        self.dest = dest
