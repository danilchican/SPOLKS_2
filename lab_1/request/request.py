import socket

import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path[:-9])

# from helper.logger import get_logger
from ip.ipv4 import AUTO_VALUE
from request.exceptions.unable_to_resolve_error import UnableToResolveError

DEFAULT_PACKAGES_COUNT = 3
DEFAULT_MAX_PAYLOAD_SIZE = 32
DEFAULT_TIMEOUT = 1
RETRIEVED_SHIFT = 0xFFFF


class Request:
    def __init__(self, host_name,
                 packets=DEFAULT_PACKAGES_COUNT,
                 timeout=DEFAULT_TIMEOUT,
                 max_payload_size=DEFAULT_MAX_PAYLOAD_SIZE):
        print("{} {} {} {}", host_name, packets, timeout, max_payload_size)

        # self.package_id = threading.current_thread().ident  # 1  TODO HARD
        self.package_id = os.getpid() & RETRIEVED_SHIFT
        print("Process id: {}".format(self.package_id))
        self.host_name = host_name
        self.host_addr = self.resolve()

        self.packets = packets
        self.timeout = timeout
        self.max_payload_size = max_payload_size

        self.sent = AUTO_VALUE
        self.received = AUTO_VALUE

    def resolve(self):
        try:
            host = socket.gethostbyname(self.host_name)
            # get_logger(__file__).info("Resolved host: {}".format(host))
            return host
        except socket.error:
            raise UnableToResolveError("Unable to resolve host: {}".format(self.host_name))
