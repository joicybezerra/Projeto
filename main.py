import redes
#o programa precisa usar algumas funções que foram implementadas no arquivo redes, por isso foi importado 
import threading
#executar tarefas ao mesmo tempo (o pragrama necessita disso já que precisa-se enviar e receber mensagens)
import os
#utilizado para encerrar o programa (os._exit(1))

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
    







