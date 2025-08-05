import socket;

modo = input("Deseja hostear (h) ou conectar-se (c) a uma sala? h/c: ")
# Pergunta ao usuário se deseja hostear ou conectar-se a uma sala
while modo not in ["h", "c"]:
#Enquanto o usuário não digitar uma opção válida, continua perguntando
    print("Opção inválida. Tente novamente.")
    modo = input("Deseja hostear (h) ou conectar-se (c) a uma sala? h/c: ")
    

