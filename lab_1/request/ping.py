import socket
import time
import struct
import select

from builder.icmp_builder import ICMPBuilder
from ip.ipv4 import AUTO_VALUE
from request.request import Request
from helper.packet_parser import PacketParser

MILLISECONDS_PRECISION = 1000
SLEEP_TIME_IN_SEC = 1
DEFAULT_PORT = 1
SIZE_BUFFER = 2048
STATISTICS_INCREMENTER = 1
FULL_PERCENTAGE = 100


class PingRequest(Request):
    def run(self):
        print("Ping host: {}, ip: {}".format(self.host_name, self.host_addr))
        print("Data: {}".format(self.max_payload_size))

        for packet in range(self.packets):
            try:
                (latency, host, ip, icmp, size) = self._ping(packet)

                if latency is None:
                    print("Request timed out for {}".format(self.host_addr))
                else:
                    latency *= MILLISECONDS_PRECISION
                    print("Reply from {}: bytes={} icmp_seq={} TTL={} time={:.0f}ms"
                          .format(host, size - len(ip), icmp["seq_num"], ip["ttl"], latency))

            except socket.gaierror as errno:
                print("Socket error: {}".format(errno))
                break

            time.sleep(SLEEP_TIME_IN_SEC)

    def _ping(self, packet_index):
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            send_time = self._send(sock, packet_index)
            (receive_time, addr, ip, icmp, size) = self._receive(sock)

        if receive_time is None:
            return None, AUTO_VALUE, AUTO_VALUE, AUTO_VALUE, AUTO_VALUE

        return receive_time - send_time, addr, ip, icmp, size

    def _send(self, sock, packet_index):
        packet = ICMPBuilder.build(packet_index, self.package_id, self.max_payload_size)

        send_time = time.time()
        sock.sendto(packet, (self.host_addr, DEFAULT_PORT))
        self.sent += STATISTICS_INCREMENTER  # calculate statistics
        return send_time

    def _receive(self, sock):
        time_left = self.timeout

        while True:
            begin_time = time.time()
            sockets = select.select([sock], [], [], time_left)
            wait_time = time.time() - begin_time

            if sockets[0] == []:
                break

            (packet_data, _) = sock.recvfrom(SIZE_BUFFER, socket.MSG_PEEK)
            size = len(packet_data) - 18
            ip_header, icmp_header = PacketParser.parse(packet_data, self.package_id)

            if ip_header is not None:
                (data, _) = sock.recvfrom(SIZE_BUFFER)
                ip, icmp = PacketParser.parse(packet_data, self.package_id)

                receive_time = time.time()
                host_ip = socket.inet_ntoa(
                    struct.pack("I", ip["src_ip"]))
                self.received += STATISTICS_INCREMENTER
                return receive_time, host_ip, ip, icmp, size

            time_left = time_left - wait_time

            if time_left <= AUTO_VALUE:
                break

        return None, AUTO_VALUE, AUTO_VALUE, AUTO_VALUE, AUTO_VALUE

    def statistic(self):
        lost = self.sent - self.received
        lost_percent = (FULL_PERCENTAGE * lost) / self.sent

        print("\nPing statistics for {}:".format(self.host_addr))
        print("\tPackets: Sent = {}, Received = {}, Lost = {} ({:.0f}% loss)"
              .format(self.sent, self.received, lost, lost_percent))
