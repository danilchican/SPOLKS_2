import string
from random import random

import struct

from helper.logger import get_logger
from request.request import DEFAULT_MAX_PAYLOAD_SIZE


class PayloadBuilder:

    @staticmethod
    def build(length=DEFAULT_MAX_PAYLOAD_SIZE):
        """Generate payload for ICMP package as random string.

        :param length: length of generated
        :return: package payload
        """
        payload = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        get_logger(__file__).info("Payload generated: " + payload)
        return struct.pack('d', payload).ljust(length, b'\x00')
