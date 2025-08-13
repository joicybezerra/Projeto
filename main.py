import redes # import de redes
import threading  # serve para rodar envio e recebimento em paralelo
import os # importa funções do sistema operacional
 

opcao = input("Deseja hostear (h) ou conectar-se (c) a uma sala? h/c: ").strip().lower() # lê a escolha do usuário, remove espaços e padroniza o texto em letras minúsculas

while opcao not in ["h", "c"]: # analisa se a opção é "h" (host) ou "c" (cliente)
    opcao = input("Modo inválido. Use 'h' ou 'c': ").strip().lower() # pede para que o usuário insira novamente até ser válido
if opcao == "h": # se o usuário escolher "h" (host)
    print("Qual protocolo deseja usar para a sala? tcp/udp:") # exibe a pergunta para o protocolo da sala a ser criada
else:
    print("Qual o protocolo da sala? tcp/udp:") # exibe a pergunta para o protocolo da sala já existente

while True: # enquanto o protocolo for válido
    protocolo = input().strip().lower() # lê e analisa o protocolo inserido
    if  protocolo in ["tcp", "udp"]: # aceita apenas tcp ou udp
        break # o loop é quebrado se o valor for válido
    print("Protocolo não compatível, peço que por favor use TCP/UDP:") # exibe uma mensagem de erro

if opcao == "h": #coleta o IP do host
    ipHost = input("Qual o seu IP (IPv4 ou IPv6)? ") # irá pedir o IP local do host
else:
    ipHost = input("Qual o IP do host? ") # irá pedir o IP do host se for cliente

if opcao == "h": # coleta a porta do host
	print("Qual a porta para a sua sala? (ex: 12345): ") # pergunta a porta da sala do host se o usuário for um
else:
	print("Qual a porta da sala?") # se for cliente, irá perguntar a porta do host para poder se conectar
    
while True: # loop para validar a porta
    try:
        portaSala = int(input()) # converte a entrada para uma variável inteira
        if portaSala <65535 and portaSala > 1023: # verifica se o valor está entre 65535 e 1023
            break # se sim, é válido
        print("Porta inválida, escolha uma porta válida:") # exibe que a porta é inválida por não se encaixar no intervalo
    except ValueError as e: # captura erro se não houver número
	    print("Porta inválida, escolha uma porta válida") # mensagem de erro

apelido =  input("Qual apelido deseja usar na conversa?: ") # campo para inserir e ler o apelido/nickname do usuário

nomeDoOutroUsuario = "falhaAoConseguirApelido" # caso não seja recebido um nickname/apelido, o sistema irá guardar um nickname padrão

sock = redes.crirSocket(protocolo, ipHost, portaSala) # cria o socket por meio da função do módulo "redes"
sockconectado = sock # referencia o socket principal (se for tcp, pode virar guardar um socket em específico)
enderecoconectado = (ipHost, portaSala) # endereço padrão com IP e a porta coletadas


if opcao == 'h': # se o usuário for host
    sock.bind((ipHost, portaSala)) # associa o socket ao ip e porta informados
    sock.settimeout(180) # define um tempo de 180 segundos para poder esperar a conexão entre o host e o cliente
    if protocolo == "tcp": # se o usuário escolher tcp
       sock.listen() # o socket irá aceitar as conexões
       print("Aguardando conexão por 3min...") # mensagem de espera           
       try:
            sockconectado, enderecoConexao= sock.accept() # aguarda a conexão do cliente
       except:
            print("Erro ao estabelecer conexão. TEMPO EXCEDIDO.") # se não houver conexão dentro do prazo, a operação é cancelada
            os._exit(1) # encerra o processo

       sockconectado.settimeout(None) # remove o timeout

       IP, PORTA = enderecoconectado # extrai ip e porta da variável de endereço
       print(f"Conectado por {IP}:{PORTA} utilizando {protocolo.upper()}.") # mensagem de conexão
       dados, _ = redes.receberDados(sockconectado, protocolo) # recebe a mensagem do cliente


    else: #se for udp
        print("Aguardando conexão por 3min...") # mensagem de espera
        dados, enderecoconectado = redes.receberDados(sock, protocolo) # recebe os dados
        sock.settimeout(None) # remove o timeout após o primeiro contato
        IP, PORTA = enderecoconectado # guarda ip/porta do remetente
        print(f"Conectado por {IP}:{PORTA} utilizando {protocolo.upper()}.") # confirmação de conexão lógica em udp


    nomeDoOutroUsuario = dados.get("Apelido", nomeDoOutroUsuario)
    redes.enviarDados(sockconectado, {"Apelido": apelido}, protocolo, enderecoconectado)

else: # se o usuário for cliente

    if protocolo == "tcp": # se o protocolo do cliente for tcp
        sock.connect((ipHost, portaSala)) # conecta o host na porta
        print(f"Conectado a {ipHost}:{portaSala} utilizando {protocolo.upper()}.") # confrima a conexão
        redes.enviarDados(sock, {"Mensagem": "conectar"}, protocolo) # envia uma mensagem inicial de conexão
        dados, _ = redes.receberDados(sock, protocolo) # aguarda a resposta do servidor
    else: # se o cliente escolher udp
        enderecoconectado = (ipHost, portaSala) # define o endereço do servidor para o envio das mensagens
        redes.enviarDados(sock, {"Mensagem": "conectar"}, protocolo, enderecoconectado) # mensagem de confirmação lógica
        print(f"Conectado a {ipHost}:{portaSala} utilizando {protocolo.upper()}.") # recebe a resposta do servidor
        dados, _ = redes.receberDados(sock, protocolo)

    nomeDoOutroUsuario = dados.get("Apelido", nomeDoOutroUsuario) # captura o apelido retornado
    redes.enviarDados(sock, {"Apelido": apelido}, protocolo, enderecoconectado) # envia o próprio apelido para o host



from prompt_toolkit import PromptSession # importa promptsession 
from prompt_toolkit.patch_stdout import patch_stdout # evita que prints concorram com o prmpt/threads


rodando = True # controla o loops das threads

def finalizarAplicacao(msg=""): # finaliza a aplicação
    print(msg, end="") # imprime mensagem final 
    try: # tenta encerrar os sockets utilizando o shutdown
        if sockconectado: #se tiver conexão tcp 
            sockconectado.shutdown(redes.socket.SHUT_RDWR) # solicita o encerramento do processo de leitura/escrita
        if sock: #se houver um socket base
            sock.shutdown(redes.socket.SHUT_RDWR) # encerra o processo de leitura/escrita
    except Exception: # ignora exceções
        pass # não faz nada se houver erro

def receberMensagens(sessao): # imprime e recebe as mensagens do outro usuário
    global rodando # irá usar/modificar a variável global (que pode ser acessada em qualquer lugar do código) "rodando"
    while rodando: # enquanto "rodando" estiver ativa
        dados = None # inicia a variável de dados
        dados, _ = redes.receberDados(sockconectado, protocolo) # bloqueia aguardando dados do socket

        if not rodando or not sockconectado: # se não houver aplicação ou se não houver socket
            msg = f"{nomeDoOutroUsuario} encerrou a conexão. Encerrando..." # mensagem de encerramento
            finalizarAplicacao(msg) # finaliza os sockets e imprime
            break # encerra o processo

        if dados: # se teve conteúdo
            if dados.get("Comando") == "desconectar": # checa se houve o pedido de desconexão do outro usuário
                msg = f"{nomeDoOutroUsuario} encerrou a conexão. Encerrando..." # mensagem de desconexão do outro usuário
                print(msg) # exibe no terminal
                rodando = False # para a aplicação
                sessao.app.loop.call_soon_threadsafe(sessao.app.exit) # solicita término do prompt
                break # encerra o processo

            print(f"{nomeDoOutroUsuario}: {dados.get('Mensagem')}") # exibe a mensagem do outro usuário
        else: # se houver algum erro ou desconexão
            if rodando: # se ainda havia a variável "rodando"
                rodando = False # atualiza sinalizador
                finalizarAplicacao("Conexão perdida. Encerrando...") # encerra a aplicação
            break # encerra o processo

def mandarMensagens(sessao): # lê o teclado e envia a mensagem
    global rodando # usa o sinalizador global
    while rodando: # enquanto a aplicação está ativa
        try:
            comando = "" # armazena instruções especiais se for preenchida. se ficar vazia, é uma mensagem comum
            conteudo = sessao.prompt() # lê uma linha do usuário

            if conteudo == "/sair": # comando para sair do chat
                rodando = False # atualiza o sinalizador para encerrar
                comando = "desconectar" # define o comando de desconexão
                mensagem = {"Comando": comando, "Mensagem": ""} # recebe dados sem texto
                redes.enviarDados(sockconectado, mensagem, protocolo, enderecoconectado) # informa o outro usuário
                print("Desconectando...") # mensagem de exibição para o usuário local
                finalizarAplicacao("") # encerra os sockets
                break # encerra o loop

            if rodando: # se ainda houver conexão
                mensagem = {"Comando": comando, "Mensagem": conteudo} # monta a mensagem do chat
                redes.enviarDados(sockconectado, mensagem, protocolo, enderecoconectado) # envia por meio do módulo "redes"

        except (EOFError, KeyboardInterrupt): # prepara o sistema se for pressionado ctrl + D (que é usado no terminal para encerrar a entrada dos dados) ou ctrl+c (que encerra o programa)
            rodando = False # encerra a variável
            break # encerra o loop

# === EXECUÇÃO DOS THREADS ===
sessao = PromptSession(f"{apelido}(Você): ") # cria uma sessão se prompt com prefixo do apelido

with patch_stdout(): # faz com outros prints não encerrem o prompt
    threadEntrada = threading.Thread(target=receberMensagens, args=(sessao,)) # recebe as mensagens
    threadSaida = threading.Thread(target=mandarMensagens, args=(sessao,)) # envia as mensagens

    threadEntrada.start() # inicia a thread de entrada
    threadSaida.start() # inicia a thread de envio

    threadEntrada.join() # aguarda o encerramento da entrada
    threadSaida.join() # aguarda o encerramento do envio

finalizarAplicacao("Conversa finalizada.") # imprime mensagem de término

