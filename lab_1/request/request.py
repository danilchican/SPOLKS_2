import socket
import threading

from helper.logger import get_logger
from ip.ipv4 import AUTO_VALUE
from request.exceptions.unable_to_resolve_error import UnableToResolveError

DEFAULT_PACKAGES_COUNT = 4
DEFAULT_MAX_PAYLOAD_SIZE = 64
DEFAULT_TIMEOUT = 5


class Request:
    def __init__(self, host_name,
                 packets=DEFAULT_PACKAGES_COUNT,
                 timeout=DEFAULT_TIMEOUT,
                 max_payload_size=DEFAULT_MAX_PAYLOAD_SIZE):
        self.package_id = threading.get_ident
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
            get_logger(__file__).info("Resolved host: " + host)
            return host
        except socket.error:
            raise UnableToResolveError('Unable to resolve host: ' + self.host_name)
