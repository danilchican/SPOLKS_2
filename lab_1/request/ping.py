import socket
import time

from builder.icmp_builder import ICMPBuilder
from request.request import Request

MILLISECONDS_PRECISION = 1000
SLEEP_TIME_IN_SEC = 1
DEFAULT_PORT = 1


class PingRequest(Request):
    def run(self):
        print("Ping host:" + self.host_name + ", ip: " + self.host_addr)
        print("Data: " + self.max_payload_size)

        for packet in range(self.packets):
            try:
                (latency, host, ip, icmp, size) = self._ping(packet)

                if latency is None:
                    print("Request timed out for {}".format(self.host_addr))
                else:
                    latency *= MILLISECONDS_PRECISION
                    print("Reply from {}: bytes={} icmp_seq={} TTL={} time={:.0f}ms"
                          .format(host, size - len(ip), icmp["seq_num"], ip["ttl"], latency))

                time.sleep(SLEEP_TIME_IN_SEC)
            except socket.gaierror as errno:
                print("Socket error: {}".format(errno))
                break

    def _ping(self, packet_index):
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            send_time = self._send(sock, packet_index)
            (receive_time, addr, ip, icmp, size) = self._receive(sock)  # TODO

        if receive_time is None:
            return None, 0, 0, 0, 0

        return receive_time - send_time, addr, ip, icmp, size

    def _send(self, sock, packet_index):
        packet = ICMPBuilder.build(packet_index, self.package_id, self.max_payload_size)

        send_time = time.time()
        sock.sendto(packet, (self.host_addr, DEFAULT_PORT))
        self.sent += 1  # calculate statistics

        return send_time
