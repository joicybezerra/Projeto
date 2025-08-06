import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import redes
import json
import socket

AZUL_CLARO = "#00a8e8"
AZUL_MEDIO = "#007ea7"
AZUL_ESCURO = "#003459"
QUASE_PRETO = "#00171f"
BRANCO = "#ffffff"

class CatChatGUI:
    def _init_(self, master):
        self.master = master
        self.master.title("🐱 CatChat - Projeto de Mensagens")
        self.master.geometry("520x550")
        self.master.configure(bg=QUASE_PRETO)

        self.role = tk.StringVar()
        self.sock = None
        self.sock_conectado = None
        self.rodando = False
        self.endereco = None
        self.protocolo = tk.StringVar(value="TCP")

        self.build_start_screen()

    def build_start_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Você deseja ser o:", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=20)

        tk.Button(self.master, text="🎧 Host (Servidor)", width=20, bg=AZUL_MEDIO, fg=BRANCO, command=self.build_host_ui).pack(pady=10)
        tk.Button(self.master, text="💬 Cliente", width=20, bg=AZUL_MEDIO, fg=BRANCO, command=self.build_client_ui).pack(pady=10)

    def build_host_ui(self):
        self.clear_window()
        tk.Label(self.master, text="CatChat - Host", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=10)

        frame = tk.Frame(self.master, bg=QUASE_PRETO)
        frame.pack(pady=5)

        tk.Label(frame, text="Porta:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=0)
        self.porta_entry = tk.Entry(frame, width=10, bg=BRANCO)
        self.porta_entry.insert(0, "5000")
        self.porta_entry.grid(row=0, column=1)

        tk.Label(frame, text="Protocolo:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=2, padx=10)
        tk.OptionMenu(frame, self.protocolo, "TCP", "UDP").grid(row=0, column=3)

        tk.Button(self.master, text="Iniciar Servidor", bg=AZUL_CLARO, fg=QUASE_PRETO, command=self.iniciar_servidor).pack(pady=10)
        self.build_chat_area()

    def build_client_ui(self):
        self.clear_window()
        tk.Label(self.master, text="CatChat - Cliente", font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=10)

        frame = tk.Frame(self.master, bg=QUASE_PRETO)
        frame.pack(pady=5)

        tk.Label(frame, text="IP:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=0)
        self.ip_entry = tk.Entry(frame, width=15, bg=BRANCO)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1)

        tk.Label(frame, text="Porta:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=2)
        self.porta_entry = tk.Entry(frame, width=10, bg=BRANCO)
        self.porta_entry.insert(0, "5000")
        self.porta_entry.grid(row=0, column=3)

        tk.Label(frame, text="Protocolo:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=4)
        tk.OptionMenu(frame, self.protocolo, "TCP", "UDP").grid(row=0, column=5)

        tk.Button(self.master, text="Conectar", bg=AZUL_CLARO, fg=QUASE_PRETO, command=self.conectar_cliente).pack(pady=10)
        self.build_chat_area()

    def build_chat_area(self):
        self.chat_box = scrolledtext.ScrolledText(self.master, width=60, height=20, state="disabled", bg=BRANCO)
        self.chat_box.pack(padx=10, pady=10)

        bottom = tk.Frame(self.master, bg=QUASE_PRETO)
        bottom.pack(pady=5)

        self.mensagem_entry = tk.Entry(bottom, width=40, bg=AZUL_ESCURO, fg=BRANCO, insertbackground=BRANCO)
        self.mensagem_entry.pack(side=tk.LEFT, padx=5)
        self.mensagem_entry.bind("<Return>", self.enviar_mensagem)

        self.enviar_btn = tk.Button(bottom, text="Enviar", bg=AZUL_MEDIO, fg=BRANCO, command=self.enviar_mensagem)
        self.enviar_btn.pack(side=tk.LEFT)

        self.master.protocol("WM_DELETE_WINDOW", self.fechar)

    def iniciar_servidor(self):
        porta = int(self.porta_entry.get())
        protocolo = self.protocolo.get()
        try:
            self.sock = rede.criar_socket_comunicacao(protocolo, '0.0.0.0', porta)
            self.sock.bind(('0.0.0.0', porta))
            self.sock.listen(1)
            self.log("Aguardando conexão do cliente...")
            threading.Thread(target=self.aguardar_conexao, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor: {e}")

    def aguardar_conexao(self):
        try:
            self.sock_conectado, addr = self.sock.accept()
            self.endereco = addr
            self.rodando = True
            self.log(f"Conectado com {addr}")
            threading.Thread(target=self.receber_mensagens, daemon=True).start()
        except Exception as e:
            self.log(f"Erro ao aceitar conexão: {e}")

    def conectar_cliente(self):
        host = self.ip_entry.get()
        porta = int(self.porta_entry.get())
        protocolo = self.protocolo.get()

        try:
            self.sock = rede.criar_socket_comunicacao(protocolo, host, porta)
            self.sock.connect((host, porta))
            self.sock_conectado = self.sock
            self.endereco = (host, porta)
            self.rodando = True
            self.log("Conectado ao servidor!")
            threading.Thread(target=self.receber_mensagens, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Erro: {e}")

    def enviar_mensagem(self, event=None):
        msg = self.mensagem_entry.get().strip()
        if msg and self.sock_conectado:
            dados = {"Comando": "", "Mensagem": msg}
            rede.enviar_dados(self.sock_conectado, dados, self.protocolo.get(), self.endereco)
            self.log(f"Você: {msg}")
            self.mensagem_entry.delete(0, tk.END)

    def receber_mensagens(self):
        while self.rodando:
            try:
                dados, _ = rede.enviar_dados(self.sock_conectado, {}, self.protocolo.get(), self.endereco)
                if dados:
                    if dados.get("Comando") == "desconectar":
                        self.log("O outro usuário se desconectou.")
                        self.rodando = False
                        break
                    self.log(f"Outro: {dados.get('Mensagem')}")
            except:
                break

    def log(self, mensagem):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, mensagem + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.yview(tk.END)

    def fechar(self):
        if self.sock_conectado:
            try:
                dados = {"Comando": "desconectar", "Mensagem": ""}
                rede.enviar_dados(self.sock_conectado, dados, self.protocolo.get(), self.endereco)
                self.sock_conectado.close()
            except:
                pass
        self.master.destroy()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()
import socket;
import threading;
import time;