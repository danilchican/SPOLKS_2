import time
import select
import socket

from _socket import AF_INET, SOCK_RAW, IPPROTO_ICMP
from builder.icmp_builder import ICMPBuilder
from helper.packet_parser import PacketParser
from ip.headers import ICMP_TTL_EXCEEDED, ICMP_ECHO_REPLY
from ip.ipv4 import AUTO_VALUE
from request.ping import PingRequest, SLEEP_TIME_IN_SEC

DEFAULT_HOPS = 30
DEFAULT_TTL = 10
DELAY_IN_MSEC = 1000
SIZE_BUFFER = 1024


class TraceRouteRequest(PingRequest):
    def __init__(self, dest, hops=DEFAULT_HOPS, timeout=SLEEP_TIME_IN_SEC):
        self.hops = hops
        self.ttl = DEFAULT_TTL
        super().__init__(dest, timeout=timeout)

    def run(self):
        print("Tracing route to {} [{}]\nover a maximum of {} hops:\n"
              .format(self.host_name, self.host_addr, self.hops))

        for ttl in range(self.ttl, self.hops + 1):
            with socket.socket(AF_INET, SOCK_RAW, IPPROTO_ICMP) as sock:
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
                latency, host_name, host_addr, complete = self._trace(sock)
            if host_addr is not None:
                print("{:3d} {:>6} ms {:>7} ms {:>7} ms    {} [{}]"
                      .format(ttl, latency[0], latency[1], latency[2], host_name, host_addr))
            else:
                print("{:3d} {:>6}  {:>9}  {:>9}       {}"
                      .format(ttl, "*", "*", "*", "Request timed out."))

            if complete:
                break

    def _trace(self, sock):
        host_addr = None
        host_name = None
        complete = False
        latency = []

        for seq_num in range(0, 3):
            send_time = self._send(sock, seq_num)
            recv_time, host_name, host_addr, complete = self._recv(sock)
            if recv_time is not None:
                delay = (recv_time - send_time) * DELAY_IN_MSEC
                data = "{:.0f}".format(delay)
                latency.append(data)
            else:
                latency.append("*")

        return latency, host_name, host_addr, complete

    def _send(self, sock, packet_index):
        packet = ICMPBuilder.build(packet_index, self.package_id, self.max_payload_size)
        sock.sendto(packet, (self.host_addr, AUTO_VALUE))
        send_time = time.time()

        return send_time

    def _recv(self, sock):
        time_left = self.timeout

        while True:
            begin_time = time.time()
            readable, *_ = select.select([sock], [], [], time_left)
            wait_time = time.time() - begin_time

            if not readable:
                break

            receive_time = time.time()
            packet_data, addr = sock.recvfrom(SIZE_BUFFER)
            (_, icmp_header) = PacketParser.parse(packet_data, self.package_id)

            icmp_result = (icmp_header["type"], icmp_header["code"])

            if icmp_result == ICMP_TTL_EXCEEDED:
                return receive_time, socket.getfqdn(addr[AUTO_VALUE]), addr[AUTO_VALUE], False

            if icmp_result == ICMP_ECHO_REPLY and self.package_id == icmp_header["packet_id"]:
                return receive_time, socket.getfqdn(addr[AUTO_VALUE]), addr[AUTO_VALUE], True

            time_left = time_left - wait_time

            if time_left <= AUTO_VALUE:
                break

        return None, None, None, False
