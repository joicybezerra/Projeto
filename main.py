import redes
#o programa precisa usar algumas funções que foram implementadas no arquivo redes, por isso foi importado 
import threading
#executar tarefas ao mesmo tempo (o pragrama necessita disso já que precisa-se enviar e receber mensagens)
import os
#utilizado para encerrar o programa (os._exit(1))

opcao = input("Deseja hostear (h) ou conectar-se (c) a uma sala? h/c: ").strip().lower()


