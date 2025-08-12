import PySimpleGUI as sg
import sys
import threading
import main

# Classe para capturar prints do main.py
class StdoutRedirector:
    def __init__(self, window, key):
        self.window = window
        self.key = key

    def write(self, text):
        if text.strip():
            self.window.write_event_value(self.key, text)

    def flush(self):
        pass


def tela_inicial():
    sg.theme("DarkBlue3")
    layout = [
        [sg.Text("Opção (h/c):"), sg.Input(key="opcao")],
        [sg.Text("Protocolo (TCP/UDP):"), sg.Input(key="protocolo")],
        [sg.Text("IP Host:"), sg.Input(key="ipHost")],
        [sg.Text("Porta da Sala:"), sg.Input(key="portaSala")],
        [sg.Text("Apelido:"), sg.Input(key="apelido")],
        [sg.Button("Entrar"), sg.Button("Cancelar")]
    ]
    window = sg.Window("Configuração de Conexão", layout)

    event, values = window.read()
    window.close()

    if event == "Entrar":
        return values
    return None


