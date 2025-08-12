import tkinter as tk
import threading
import time
from tkinter import scrolledtext, messagebox

import redes  # importa seu módulo de rede (funções de criar socket, enviar/receber)

# paleta de cores usadas na interface
AZUL_CLARO = "#00a8e8"
AZUL_MEDIO = "#007ea7"
AZUL_ESCURO = "#003459"
QUASE_PRETO = "#00171f"
BRANCO = "#ffffff"

class CatChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("🐱 CatChat - Chat de Mensagens")
        self.master.geometry("520x550")
        self.master.configure(bg=QUASE_PRETO)

        self.role = None
        self.nome = tk.StringVar()
        self.protocolo = tk.StringVar(value="TCP")
        self.ip_version = tk.StringVar(value="IPv4")
        self.ip = tk.StringVar(value="127.0.0.1")
        self.porta = tk.IntVar(value=5000)

        self.message_queue = []
        self.waiting_for_message = threading.Event()
        self.start_event = threading.Event()
        self.chat_box = None

        self.build_start_screen()

    def build_start_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Você deseja ser o:", font=("Arial", 14),
                 fg=BRANCO, bg=QUASE_PRETO).pack(pady=20)
        tk.Button(self.master, text="🎧 Host (Servidor)", width=20,
                  bg=AZUL_MEDIO, fg=BRANCO,
                  command=lambda: self.build_connection_ui("h")).pack(pady=10)
        tk.Button(self.master, text="💬 Cliente", width=20,
                  bg=AZUL_MEDIO, fg=BRANCO,
                  command=lambda: self.build_connection_ui("c")).pack(pady=10)

    def build_connection_ui(self, role):
        self.role = role
        self.clear_window()

        tk.Label(self.master, text=f"CatChat - {'Host' if role=='h' else 'Cliente'}",
                 font=("Arial", 14), fg=BRANCO, bg=QUASE_PRETO).pack(pady=10)

        frame = tk.Frame(self.master, bg=QUASE_PRETO)
        frame.pack(pady=5)

        if role == "c":
            tk.Label(frame, text="IP:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=0)
            tk.Entry(frame, textvariable=self.ip, width=15, bg=BRANCO).grid(row=0, column=1)

        tk.Label(frame, text="Porta:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=2)
        tk.Entry(frame, textvariable=self.porta, width=10, bg=BRANCO).grid(row=0, column=3)

        tk.Label(frame, text="Protocolo:", bg=QUASE_PRETO, fg=BRANCO).grid(row=0, column=4)
        tk.OptionMenu(frame, self.protocolo, "TCP", "UDP").grid(row=0, column=5)

        tk.Label(frame, text="Versão IP:", bg=QUASE_PRETO, fg=BRANCO).grid(row=1, column=0, pady=5)
        tk.OptionMenu(frame, self.ip_version, "IPv4", "IPv6").grid(row=1, column=1, pady=5)

        tk.Label(self.master, text="Seu nome/apelido:", bg=QUASE_PRETO, fg=BRANCO).pack(pady=(15, 0))
        tk.Entry(self.master, textvariable=self.nome, width=30, bg=BRANCO).pack(pady=5)

        tk.Button(self.master, text="Entrar no Chat", bg=AZUL_CLARO, fg=QUASE_PRETO,
                  command=self.start_chat).pack(pady=10)

    def start_chat(self):
        if not self.nome.get().strip():
            messagebox.showerror("Erro", "Digite seu nome/apelido!")
            return
        self.build_chat_area()
        self.start_event.set()

    def build_chat_area(self):
        self.clear_window()
        self.chat_box = scrolledtext.ScrolledText(self.master, width=60, height=20,
                                                  state="disabled", bg=BRANCO)
        self.chat_box.pack(padx=10, pady=10)

        bottom = tk.Frame(self.master, bg=QUASE_PRETO)
        bottom.pack(pady=5)

        self.mensagem_entry = tk.Entry(bottom, width=40, bg=AZUL_ESCURO, fg=BRANCO,
                                       insertbackground=BRANCO)
        self.mensagem_entry.pack(side=tk.LEFT, padx=5)
        self.mensagem_entry.bind("<Return>", self.enviar_mensagem)

        self.enviar_btn = tk.Button(bottom, text="Enviar", bg=AZUL_MEDIO, fg=BRANCO,
                                    command=self.enviar_mensagem)
        self.enviar_btn.pack(side=tk.LEFT)

        self.master.protocol("WM_DELETE_WINDOW", self.fechar)

    def enviar_mensagem(self, event=None):
        msg = self.mensagem_entry.get().strip()
        if msg:
            self.message_queue.append(msg)
            self.waiting_for_message.set()
            self.mensagem_entry.delete(0, tk.END)

    def get_initial_data(self):
        self.start_event.wait()
        return (
            self.role,
            self.protocolo.get().lower(),
            self.ip.get(),
            int(self.porta.get()),
            self.nome.get(),
            self.ip_version.get()
        )

    def get_next_message(self):
        self.waiting_for_message.wait()
        self.waiting_for_message.clear()
        return self.message_queue.pop(0)

    def log(self, mensagem):
        agora = time.strftime("%d/%m/%Y %H:%M")
        mensagem_formatada = f"[{agora}] {mensagem}"
        if self.chat_box:
            self.chat_box.config(state="normal")
            self.chat_box.insert(tk.END, mensagem_formatada + "\n")
            self.chat_box.config(state="disabled")
            self.chat_box.see(tk.END)

    def fechar(self):
        self.master.destroy()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()