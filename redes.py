import socket;
import ipaddress;
import json;

def get_ip_family(host):
    #identifica se o endereço IP é IPv4 ou IPv6
    try:
        ip = ipaddress.ip_address(host);
        if isinstance(ip, ipaddress.IPv4Address):
              #verifica se o endereço IP dp host é válido
            return socket.AF_INET;
        elif isinstance(ip, ipaddress.IPv6Address):
            return socket.AF_INET6;
    except ValueError: 
