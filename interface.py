import tkinter #módulo gráfico padrão
from tkinter import scrolledtext, messagebox #caixa de texto com rolagem e janelas com avisos como alertas ou erros
import threading #permite que o programa faça múltiplas tarefas ao mesmo tempo
import redes 
import json #estrutura das mensagens enviadas
import socket #módulo de comunicação por rede do Python; TCP/IP 
import time  #formata e exibe data e hora

#paleta de cores do catchat
AZUL_CLARO = "#00a8e8"
AZUL_MEDIO = "#007ea7"
AZUL_ESCURO = "#003459"
QUASE_PRETO = "#00171f"
BRANCO = "#ffffff"

class CatChatGUI:
    def __init__(self, master): #método construtor que é executado quando se abre uma nova janela; master é a janela principal
        self.master = master #referência da janela
        self.master.title("🐱 CatChat - Chat de Mensagens") #nome da janela
        self.master.geometry("520x550") #tamanho da janela
        self.master.configure(bg=QUASE_PRETO) #cor de fundo

        self.role = tk.StringVar() #se o usuário é cliente ou servidor
        self.nome = tk.StringVar() #nome/apelido do usuário
        self.sock = None #socket principal
        self.sock_conectado = None #socket para a troca de mensagens
        self.rodando = False #controla o loop
        self.endereco = None #IP ou porta conectada ao chat
        self.protocolo = tk.StringVar(value="TCP") #se o protocolo é TCP (padrão) ou UDP

        self.build_start_screen() #chama a tela inicial que serve para escolher entre cliente ou servidor

    def build_start_screen(self): #tela de início
        self.clear_window() #remove as interfaces anteriores e mostra dois botões
        tk.Label(self.master, text="Você deseja ser o:", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=20) #título

        tk.Button(self.master, text="🎧 Host (Servidor)", width=20, bg=AZUL_MEDIO, fg=BRANCO, command=self.build_host_ui).pack(pady=10)
        tk.Button(self.master, text="💬 Cliente", width=20, bg=AZUL_MEDIO, fg=BRANCO, command=self.build_client_ui).pack(pady=10)
        #configuração dos botões de "cliente" e "servidor"; se escolher cliente, irá chamar a tela do cliente; se escolher servidor, irá para a tela do servidor

    def build_host_ui(self): #área do host/servidor
        self.clear_window() #limpa a tela anterior
        tk.Label(self.master, text="CatChat - Host", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=10) #título da janela

        frame = tk.Frame(self.master, bg=QUASE_PRETO)
        frame.pack(pady=5) #criação dos campos de entrada de porta e protocolo

        tk.Label(frame, text="Porta:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=0) #criação da label porta
        self.porta_entry = tk.Entry(frame, width=10, bg=BRANCO) #campo de entrada
        self.porta_entry.insert(0, "5000") #porta padrão
        self.porta_entry.grid(row=0, column=1) 

        tk.Label(frame, text="Protocolo:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=2, padx=10)
        tk.OptionMenu(frame, self.protocolo, "TCP", "UDP").grid(row=0, column=3) #label e menu de seleção para o protocolo

        tk.Label(self.master, text="Seu nome/apelido:", bg=QUASE_PRETO, fg=BRANCO).pack(pady=(15, 0)) #label para o nome/apelido
        tk.Entry(self.master, textvariable=self.nome, width=30, bg=BRANCO).pack(pady=5) #campo para inserir o nome/apelido do usuário

        tk.Button(self.master, text="Iniciar Servidor", bg=AZUL_CLARO, fg=QUASE_PRETO, command=self.iniciar_servidor).pack(pady=10) #botão de iniciar o servidor
        self.build_chat_area()#chama a função build_chat_area
        

    def build_client_ui(self): #área do cliente
        self.clear_window() #limpa as telas anteriores
        tk.Label(self.master, text="CatChat - Cliente", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=10) #título da janela do cliente

        frame = tk.Frame(self.master, bg=QUASE_PRETO)
        frame.pack(pady=5) #organização dos campos IP, porta e protocolo

        tk.Label(frame, text="IP:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=0) 
        self.ip_entry = tk.Entry(frame, width=15, bg=BRANCO)
        self.ip_entry.insert(0, "127.0.0.1") #IP padrão
        self.ip_entry.grid(row=0, column=1) #campo para o IP

        tk.Label(frame, text="Porta:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=2)
        self.porta_entry = tk.Entry(frame, width=10, bg=BRANCO)
        self.porta_entry.insert(0, "5000") #porta padrão
        self.porta_entry.grid(row=0, column=3) #campo para a porta

        tk.Label(frame, text="Protocolo:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=4)
        tk.OptionMenu(frame, self.protocolo, "TCP", "UDP").grid(row=0, column=5) #menu para o protocolo

        tk.Label(self.master, text="Seu nome/apelido:", bg=QUASE_PRETO, fg=BRANCO).pack(pady=(15, 0))
        tk.Entry(self.master, textvariable=self.nome, width=30, bg=BRANCO).pack(pady=5) #entrada para nome/apelido

        tk.Button(self.master, text="Conectar", bg=AZUL_CLARO, fg=QUASE_PRETO, command=self.conectar_cliente).pack(pady=10) #botão que conecta ao servidor por meio da função conectar_cliente
        self.build_chat_area() #chama a função build_chat_area

    def build_chat_area(self): #área do chat
        self.chat_box = scrolledtext.ScrolledText(self.master, width=60, height=20, state="disabled", bg=BRANCO) #caixa de texto com rolagem
        self.chat_box.pack(padx=10, pady=10)

        bottom = tk.Frame(self.master, bg=QUASE_PRETO) #quadro para alinhar o campo da mensagem e o botão enviar
        bottom.pack(pady=5) 

        self.mensagem_entry = tk.Entry(bottom, width=40, bg=AZUL_ESCURO, fg=BRANCO, insertbackground=BRANCO) #campo que usuário insere a mensagem
        self.mensagem_entry.pack(side=tk.LEFT, padx=5)
        self.mensagem_entry.bind("<Return>", self.enviar_mensagem) #chama a função enviar_mensagem ao pressionar o botão Enter

        self.enviar_btn = tk.Button(bottom, text="Enviar", bg=AZUL_MEDIO, fg=BRANCO, command=self.enviar_mensagem)
        self.enviar_btn.pack(side=tk.LEFT) #botão para enviar a mensagem

        self.master.protocol("WM_DELETE_WINDOW", self.fechar) #fecha a tela do chat

    def iniciar_servidor(self): #função para iniciar o servidor
        porta = int(self.porta_entry.get()) #lê o valor da porta
        protocolo = self.protocolo.get() #lê o valor do protocolo

        if not self.nome.get().strip(): 
            messagebox.showwarning("Nome obrigatório", "Por favor, informe seu nome/apelido.")
            return
            #se o campo estiver vazio, irá exibir uma tela de mensagem de aviso e interrompe o processo até ser inserido algum valor

        try:
            self.sock = redes.criar_socket_comunicacao(protocolo, '0.0.0.0', porta) #cria um socket do módulo redes
            self.sock.bind(('0.0.0.0', porta)) #liga o socket a qualquer IP disponível na máquina e à porta
            self.sock.listen(1) #máximo de 1 conexão simultânea
            self.log("Aguardando conexão do cliente...") #exibe que o host está esperando o cliente
            threading.Thread(target=self.aguardar_conexao, daemon=True).start() #cria uma nova thread
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor: {e}") #se der erro, exibe uma caixa de erro

    def aguardar_conexao(self): #função para aguardar a conexão
        try:
            self.sock_conectado, addr = self.sock.accept() #espera/bloqueia até que o cliente se conecte
            self.endereco = addr #ip e porta do cliente, que são guardados como endereço
            self.rodando = True #conexão ativa
            self.log(f"Conectado com {addr}") #print que informa que alguém se conectou
            threading.Thread(target=self.receber_mensagens, daemon=True).start() #inicia uma thread paralela
        except Exception as e:
            self.log(f"Erro ao aceitar conexão: {e}") #exibe uma caixa de erro caso haja alguma falha na conexão

    def conectar_cliente(self): #função da conexão do cliente
        host = self.ip_entry.get() #lê o ip
        porta = int(self.porta_entry.get()) #lê a porta
        protocolo = self.protocolo.get() #lê o protocolo

        if not self.nome.get().strip():
            messagebox.showwarning("Nome obrigatório", "Por favor, informe seu nome/apelido.")
            return 
            #se o campo estiver vazio, irá exibir uma tela de mensagem de aviso e interrompe o processo até ser inserido algum valor
        try:
            self.sock = redes.criar_socket_comunicacao(protocolo, host, porta) #cria o socket
            self.sock.connect((host, porta))
            self.sock_conectado = self.sock
            self.endereco = (host, porta)
            self.rodando = True
            self.log("Conectado ao servidor!") #exibe que a conexão foi feita
            threading.Thread(target=self.receber_mensagens, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}") #se der erro, exibe a mensagem de erro

    def enviar_mensagem(self, event=None): #chamada ao pressionar a tecla Enter ou apertar no botão de envio
        msg = self.mensagem_entry.get().strip() 
        if msg and self.sock_conectado: #lê e limpa o texto digitado e continua se a mensagem não for vazia e se estiver conectado
            dados = {"Comando": "", "Mensagem": msg}
            redes.enviar_dados(self.sock_conectado, dados, self.protocolo.get(), self.endereco) #envia a mensagem usando redes.enviar_dados
            nome = self.nome.get() or "Você"
            self.log(f"{nome}: {msg}") #mostra a mensagem enviada junto do nome/apelido do usuário
            self.mensagem_entry.delete(0, tk.END) #limpa o campo de digitação

    def receber_mensagens(self):
        while self.rodando:
            try:
                dados, _ = redes.criar_socket_comunicacao(self.sock_conectado, {}, self.protocolo.get(), self.endereco)
                if dados:
                    if dados.get("Comando") == "desconectar": #verifica se o usuário mandou uma mensagem
                        self.log("O outro usuário se desconectou.") #encerra o loop quando se desconecta do chat
                        self.rodando = False
                        break
                    self.log(f"Outro: {dados.get('Mensagem')}") #envia a mensagem 
            except:
                break #em caso de erro ou falha na conexão, o loop é interrompido

    def log(self, mensagem):
        agora = time.strftime("%d/%m/%Y %H:%M") #formata a hora atual
        mensagem_formatada = f"[{agora}] {mensagem}" #formata a mensagem para mostrar no chat
        self.chat_box.config(state="normal") #habilita a caixa de texto
        self.chat_box.insert(tk.END, mensagem_formatada + "\n") #insere a mensagem
        self.chat_box.config(state="disabled") #desabilita a caixa de texto
        self.chat_box.yview(tk.END) #rolagem até o final automaticamente

    def fechar(self): #função para fechar o chat
        if self.sock_conectado: #continua se tiver alguma função ativa
            try:
                dados = {"Comando": "desconectar", "Mensagem": ""} #cria uma mensagem com esses comandos
                redes.enviar_dados(self.sock_conectado, dados, self.protocolo.get(), self.endereco) #envia a mensagem de desconexão para o outro usuário
                self.sock_conectado.close() #fecha a conexão entre o cliente e o servidor
            except:
                pass
        self.master.destroy() #fecha a janela do programa

    def clear_window(self): 
        for widget in self.master.winfo_children(): #retorna uma lista com todos os botões, entradas de texto e etc
            widget.destroy() #apaga todos os widgets da janela para trocar de tela. exemplo: trocar de menu para o chat

if _name_ == "_main_":
    root = tk.Tk() #cria a janela principal da interface
    app = CatChatGUI(root) #cria uma instância
    root.mainloop() #inicia o loop principal do tkinter, que mantém a janela aberta e responde a cliques, digitação e etc