import socket; #Permite a conexão de rede
import ipaddress; #verifica o tipo de IP
import json; #Convertes dados

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
        raise ValueError(f "Este endereço de IP está inválido: {host}");
    
def criar_socket_comunicacao(protocolo, host, porta):
    #Cria um socket de comunicação adaptado para get_ip_family
    family = get_ip_family(host) #usa a função anterior que determina o tipo de IP do socket
    sock_type = socket.SOCK_STREAM if protocolo.lower() == 'tcp' else socket.SOCK_DGRAM
    #SOCK_STREAM = TCP; SOCK_DGRAM = UDP
    sock = socket.socket(family, sock_type)
    #criar socket com a familia IP e o tipo de protocolo escolhido
    sock.setsockopt(socket.socketsetsockopt(socket.SOL_SOCKET, socket.SO_REUSEADOR, 1))
    return sock #retorna ao socket

def enviar_dados(sock, dados, protocolo, oponente_addr=None)