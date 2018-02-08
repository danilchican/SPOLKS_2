import struct

from ip.headers import ICMP_HEADER, IP_HEADER, ICMP_HEADER_FORMAT, IP_HEADER_FORMAT


class PacketParser:

    @staticmethod
    def parse(packet, packet_id):
        """Extract IP and ICMP headers from package.

        :param packet:
        :param packet_id:
        :return: IP and ICMP headers
        """
        ip_header = None

        icmp_header = PacketParser._build_map(ICMP_HEADER, ICMP_HEADER_FORMAT, data=packet[20:28])

        if icmp_header["packet_id"] == packet_id:
            ip_header = PacketParser._build_map(IP_HEADER, IP_HEADER_FORMAT, data=packet[:20])

        return ip_header, icmp_header

    @staticmethod
    def _build_map(keys, format, data):
        """Build map like key => value.

        :param keys: List of headers
        :param format:
        :param data:
        :return: mapped keys and data
        """
        unpacked_data = struct.unpack(format, data)
        return dict(zip(keys, unpacked_data))
