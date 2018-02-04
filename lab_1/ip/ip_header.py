import struct
from ip.ipv4 import IPv4Header, PacketData

VERSION_IHL_BITS_OFFSET_DIRECT = 4
VERSION_IHL_BITS_OFFSET_REVERSE = 0xF
FLAGS_FRAGMENT_BITS_OFFSET_DIRECT = 13
FLAGS_FRAGMENT_BITS_OFFSET_REVERSE = 0x1FFF
DEFAULT_TTL = 64


class IPHeader(IPv4Header):
    format = 'BBHHHBBH4s4s'

    def pack(self):
        package_obj = (self.version << VERSION_IHL_BITS_OFFSET_DIRECT | self.ihl, self.dscp, self.total_length,
                       self.identification, self.flags << FLAGS_FRAGMENT_BITS_OFFSET_DIRECT | self.fragment_offset,
                       self.ttl, self.protocol, self.checksum, self.src, self.dest)

        return struct.pack(self.format, *package_obj)

    def unpack(self, byte_obj):
        packet = PacketData(*struct.unpack(self.format, byte_obj))

        version = packet.version_ihl >> VERSION_IHL_BITS_OFFSET_DIRECT
        ihl = packet.version_ihl & VERSION_IHL_BITS_OFFSET_REVERSE
        flags = packet.flags_fragment >> FLAGS_FRAGMENT_BITS_OFFSET_DIRECT
        fragment_offset = packet.flags_fragment & FLAGS_FRAGMENT_BITS_OFFSET_REVERSE

        return IPv4Header(version, packet.src, packet.dest, packet.ttl, packet.protocol,
                          ihl, packet.dscp, packet.total_length,
                          packet.identification, flags, fragment_offset, packet.checksum)
