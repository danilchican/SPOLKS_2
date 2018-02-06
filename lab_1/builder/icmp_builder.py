import struct

from builder.payload_builder import PayloadBuilder
from helper.helper import Helper
from ip.headers import ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST
from ip.ipv4 import AUTO_VALUE
from request.request import DEFAULT_MAX_PAYLOAD_SIZE


class ICMPBuilder:

    @staticmethod
    def build(packet_index, packet_id, payload_size=DEFAULT_MAX_PAYLOAD_SIZE):
        """Build ICMP package by packet_id

        :param packet_index: packet index in sequence
        :param packet_id:
        :param payload_size:
        :return: ICMP packet
        """
        pre_header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST,
                                 AUTO_VALUE, AUTO_VALUE,
                                 packet_id, packet_index)

        data = PayloadBuilder.build(payload_size)
        checksum = Helper.find_checksum(pre_header + data)

        header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST,
                             AUTO_VALUE, checksum,
                             packet_id, packet_index)

        packet = header + data
        return packet
