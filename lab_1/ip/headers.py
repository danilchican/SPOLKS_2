ICMP_HEADER = ["type", "code", "checksum", "packet_id", "seq_num"]

IP_HEADER = [
    "version", "type", "length", "id", "flags", "ttl",
    "protocol", "checksum", "src_ip", "dest_ip"
]

ICMP_HEADER_FORMAT = "BBHHH"
IP_HEADER_FORMAT = "BBHHHBBHII"

ICMP_ECHO_REQUEST = 8
