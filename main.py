import socket           # Comunicação em rede
import threading        # Para rodar envio e recebimento em paralelo
from interface import CatChatGUI
import tkinter as tk
import redes

def receber_mensagens(sock, gui, udp_host_addr=None):
    """
    Recebe mensagens do socket e mostra na interface.
    Roda em uma thread separada para não travar a interface.
    """
    while True:
        try:
            if sock.type == socket.SOCK_DGRAM:  # UDP
                dados, addr = sock.recvfrom(1024)
                if not dados:
                    break
                msg = dados.decode()
                gui.log(f"{addr}: {msg}")
                # Para host UDP, salva o endereço do cliente para responder
                if udp_host_addr is not None:
                    udp_host_addr[0] = addr
            else:  # TCP
                dados = sock.recv(1024)
                if not dados:
                    break
                msg = dados.decode()
                gui.log(f"Outro: {msg}")
        except Exception as e:
            gui.log(f"Erro ao receber: {e}")
            break  # Erro ou desconexão

def enviar_mensagens(sock, gui, udp_addr=None, udp_host_addr=None):
    """
    Envia mensagens digitadas pelo usuário via socket.
    Busca mensagens na fila usando get_next_message().
    """
    while True:
        msg = gui.get_next_message()  # Busca próxima mensagem
        if msg:
            try:
                if sock.type == socket.SOCK_DGRAM:
                    # Se for host UDP, envie para o último cliente que enviou mensagem
                    if udp_host_addr and udp_host_addr[0]:
                        sock.sendto(msg.encode(), udp_host_addr[0])
                    elif udp_addr:
                        sock.sendto(msg.encode(), udp_addr)
                else:
                    sock.sendall(msg.encode())  # Envia
            except Exception as e:
                gui.log(f"Erro ao enviar: {e}")
                break  # Conexão encerrada

def main():
    # Cria janela principal do Tkinter
    root = tk.Tk()
    gui = CatChatGUI(root)

    # Obtém dados iniciais (role, protocolo, ip, porta, nome, versão IP)
    role, protocolo, ip, porta, nome, versao_ip = gui.get_initial_data()

    # Escolhe família do IP (IPv4 ou IPv6)
    if versao_ip == "IPv6":
        familia = socket.AF_INET6
        bind_addr = (ip, porta, 0, 0)
    else:
        familia = socket.AF_INET
        bind_addr = ("0.0.0.0", porta)

    # Cria o socket
    sock = redes.criar_socket_comunicacao(protocolo, ip, porta)

    if role == "h":  # Host/Servidor
        sock.bind(bind_addr)
        if protocolo.lower() == "tcp":
            sock.listen(1)
            gui.log("Aguardando conexão...")
            conn, addr = sock.accept()
            gui.log(f"✅ Conexão estabelecida com {addr}")
            # Threads para envio e recebimento
            threading.Thread(target=receber_mensagens, args=(conn, gui), daemon=True).start()
            threading.Thread(target=enviar_mensagens, args=(conn, gui), daemon=True).start()
        else:
            gui.log("Servidor UDP pronto para receber mensagens.")
            # Para UDP, precisamos compartilhar o endereço do cliente entre threads
            udp_host_addr = [None]  # Usando lista mutável para compartilhar entre threads
            threading.Thread(target=receber_mensagens, args=(sock, gui, udp_host_addr), daemon=True).start()
            threading.Thread(target=enviar_mensagens, args=(sock, gui, None, udp_host_addr), daemon=True).start()

    else:  # Cliente
        if protocolo.lower() == "tcp":
            sock.connect((ip, porta))
            gui.log(f"✅ Conectado ao servidor {ip}:{porta}")
            threading.Thread(target=receber_mensagens, args=(sock, gui), daemon=True).start()
            threading.Thread(target=enviar_mensagens, args=(sock, gui), daemon=True).start()
        else:
            gui.log(f"Cliente UDP pronto para enviar mensagens para {ip}:{porta}")
            threading.Thread(target=receber_mensagens, args=(sock, gui), daemon=True).start()
            threading.Thread(target=enviar_mensagens, args=(sock, gui, (ip, porta)), daemon=True).start()

    # Loop principal da interface
    root.mainloop()

if __name__ == "__main__":
    main()