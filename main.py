import redes
import threading
import os
 

opcao = input("Deseja hostear (h) ou conectar-se (c) a uma sala? h/c: ").strip().lower()

while opcao not in ["h", "c"]:
    opcao = input("Modo inválido. Use 'h' ou 'c': ").strip().lower()
if opcao == "h":
    print("Qual protocolo deseja usar para a sala? tpc/udp:")
else:
    print("Qual o protocolo da sala? tcp/udp:")

while True:
    protocolo = input().strip().lower()
    if  protocolo in ["tcp", "udp"]: 
        break
    print("Protocolo não compatível, peço que por favor use TCP/UDP:")

if opcao == "h":
    ipHost = input("Qual o seu IP (IPv4 ou IPv6)? ")
else:
    ipHost = input("Qual o IP do host? ")

if opcao == "h":
	print("Qual a porta para a sua sala? (ex: 12345): ")
else:
	print("Qual a porta da sala?")
    
while True:
    try:
        portaSala = int(input())
        if portaSala <65535 and portaSala > 1023: 
            break
        print("Porta inválida, escolha uma porta válida:")
    except ValueError as e:
	    print("Porta inválida, escolha uma porta válida")

apelido =  input("Qual apelido deseja usar na conversa?: ")

nomeDoOutroUsuario = "falhaAoConseguirApelido"

sock = redes.crirSocket(protocolo, ipHost, portaSala)
sockconectado = sock
enderecoconectado = (ipHost, portaSala)


if opcao == 'h':
    sock.bind((ipHost, portaSala))
    sock.settimeout(180)
    if protocolo == "tcp":
       sock.listen()
       print("Aguardando conexão por 3min...")              
       try:
            sockconectado, enderecoConexao= sock.accept()
       except:
            print("Erro ao estabelecer conexão. TEMPO EXCEDIDO.")
            os._exit(1)

       sockconectado.settimeout(None)

       IP, PORTA = enderecoconectado
       print(f"Conectado por {IP}:{PORTA} utilizando {protocolo.upper()}.")
       dados, _ = redes.receberDados(sockconectado, protocolo)


    else:
        print("Aguardando conexão por 3min...")
        dados, enderecoconectado = redes.receberDados(sock, protocolo)
        sock.settimeout(None)
        IP, PORTA = enderecoconectado
        print(f"Conectado por {IP}:{PORTA} utilizando {protocolo.upper()}.")


    nomeDoOutroUsuario = dados.get("Apelido", nomeDoOutroUsuario)
    redes.enviarDados(sockconectado, {"Apelido": apelido}, protocolo, enderecoconectado)

else:

    if protocolo == "tcp":
        sock.connect((ipHost, portaSala))
        print(f"Conectado a {ipHost}:{portaSala} utilizando {protocolo.upper()}.")
        redes.enviarDados(sock, {"Mensagem": "conectar"}, protocolo)
        dados, _ = redes.receberDados(sock, protocolo)
    else:
        enderecoconectado = (ipHost, portaSala)
        redes.enviarDados(sock, {"Mensagem": "conectar"}, protocolo, enderecoconectado)
        print(f"Conectado a {ipHost}:{portaSala} utilizando {protocolo.upper()}.")
        dados, _ = redes.receberDados(sock, protocolo)

    nomeDoOutroUsuario = dados.get("Apelido", nomeDoOutroUsuario)
    redes.enviarDados(sock, {"Apelido": apelido}, protocolo, enderecoconectado)



from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


rodando = True

def finalizarAplicacao(msg=""):
    print(msg, end="")
    try:
        if sockconectado:
            sockconectado.shutdown(redes.socket.SHUT_RDWR)
        if sock:
            sock.shutdown(redes.socket.SHUT_RDWR)
    except Exception:
        pass

def receberMensagens(sessao):
    global rodando
    while rodando:
        dados = None
        dados, _ = redes.receberDados(sockconectado, protocolo)

        if not rodando or not sockconectado:
            msg = f"{nomeDoOutroUsuario} encerrou a conexão. Encerrando..."
            finalizarAplicacao(msg)
            break

        if dados:
            if dados.get("Comando") == "desconectar":
                msg = f"{nomeDoOutroUsuario} encerrou a conexão. Encerrando..."
                print(msg)
                rodando = False
                sessao.app.loop.call_soon_threadsafe(sessao.app.exit)
                break

            print(f"{nomeDoOutroUsuario}: {dados.get('Mensagem')}")
        else:
            if rodando:
                rodando = False
                finalizarAplicacao("Conexão perdida. Encerrando...")
            break

def mandarMensagens(sessao):
    global rodando
    while rodando:
        try:
            comando = ""
            conteudo = sessao.prompt()

            if conteudo == "/sair":
                rodando = False
                comando = "desconectar"
                mensagem = {"Comando": comando, "Mensagem": ""}
                redes.enviarDados(sockconectado, mensagem, protocolo, enderecoconectado)
                print("Desconectando...")
                finalizarAplicacao("")
                break

            if rodando:
                mensagem = {"Comando": comando, "Mensagem": conteudo}
                redes.enviarDados(sockconectado, mensagem, protocolo, enderecoconectado)

        except (EOFError, KeyboardInterrupt):
            rodando = False
            break

# === EXECUÇÃO DOS THREADS ===
sessao = PromptSession(f"{apelido}(Você): ")

with patch_stdout():
    threadEntrada = threading.Thread(target=receberMensagens, args=(sessao,))
    threadSaida = threading.Thread(target=mandarMensagens, args=(sessao,))

    threadEntrada.start()
    threadSaida.start()

    threadEntrada.join()
    threadSaida.join()

finalizarAplicacao("Conversa finalizada.")

