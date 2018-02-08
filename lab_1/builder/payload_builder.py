import string
import random

import struct
# from helper.logger import get_logger
from request.request import DEFAULT_MAX_PAYLOAD_SIZE


class PayloadBuilder:

    @staticmethod
    def build(length=DEFAULT_MAX_PAYLOAD_SIZE):
        """Generate payload for ICMP package as random string.

        :param length: length of generated
        :return: package payload
        """
        payload = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        # get_logger(__file__).info("Payload generated: " + payload)
        return struct.pack('p', bytes(payload, 'utf-8')).ljust(length, b'\x00')
