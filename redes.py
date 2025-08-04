import socket;
import ipaddress;
import json;

def get_ip_family(host):
    try:
        ip = ipaddress.ip_address(host);
        if isinstance(ip, ipaddress.IPv4Address):
            return socket.AF_INET;
        elif isinstance(ip, ipaddress.IPv6Address):
            return socket.AF_INET6;
    except ValueError:
        pass

    try:
        info = socket.getaddrinfo(host, None);
        if info:
            return info[0][0];
    except socket.gaierror:
        pass

    return None;