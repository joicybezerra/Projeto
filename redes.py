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
    #pemite que o servidor seja reiniciado e o erro "porta ocupada" seja evitado
    return sock #retorna ao socket

def enviar_dados(sock, dados, protocolo, oponente_addr=None, buffer_size=1024):
    #define a função que envia mensagens pela rede
    #sock = socket usado
    #dados = dados a serem enviados
    #protocolo = TCP ou UDP
    #oponente_addr = Usado no UDP para saber o endereço de destino
    #Envia dados (serializados em JSON) através do socket.
    #O oponente_addr é necessário para UDP.
    payload = json.dumps(dados).encode('utf-8')
    #playload = pronto para que o socket possa enviar

    try:
        if protocolo.lower() == 'tcp':
            sock.sendall(payload)
        # O sendall garante que o envio por TCP seja completo.
        else: # UDP
            payload, oponente_addr = sock.recvfrom(buffer_size)

            dados = json.loads(payload.decode('utf-8'))
            return dados, oponente_addr
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f"Erro ao receber dados: {e}")

    return None, None
