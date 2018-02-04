import socket

from builder.package_builder import PackageBuilder
from ip.ip_header import IPHeader, DEFAULT_TTL
from ip.ipv4 import PROTOCOL_VERSION
from request.request import Request

if __name__ == '__main__':  # TODO test remove
    request = Request('ya.ru')

    src = socket.inet_aton('192.168.0.1')
    dest = socket.inet_aton('192.168.0.2')

    builder = PackageBuilder(PROTOCOL_VERSION, '192.168.0.1', '192.168.0.2', bytes(123))
    ipheader = IPHeader(PROTOCOL_VERSION, src, dest, DEFAULT_TTL)
    packed = ipheader.pack()
    print('packed: ', packed)
    unpacked = ipheader.unpack(packed)
    print('unpacked: ', unpacked)
