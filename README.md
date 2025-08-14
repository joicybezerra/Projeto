# Repositório:
- [https://github.com/joicybezerra/Projeto.git](https://github.com/joicybezerra/Projeto.git)

# Descrição:
- Projeto de implementação de redes por meio de um sistema de comunicação/chat em tempo real entre cliente e servidor utilizando protocolo TCP ou UDP para a disciplina de Arquitetura de redes de computadores e Tecnologia de Implementação de redes.

# Discentes:
- Abda Queila Silva de Melo (20231054010003) 

- Ana Karoline da Costa Freire (20231054010030)

- Joicy da Silva Bezerra (20231054010029)

- Maria Eduarda de Araújo Ferino (20231054010009)

# Como utilizar:

1. De início, o programa pede para que o usuário insira "h" se ele quiser ser o host (servidor) (que irá criar o bate-papo) ou "c" se ele quiser ser o cliente para se conectar a uma sala existente. 
2. Se o usuário escolher ser o host, ele irá escolher o protocolo (TCP ou UDP) da sala que a ser criada. Se o usuário escolher ser cliente e já houver uma sala existente, o sistema irá pedir para que ele insira o protocolo da sala. 
3. Na tela do host, o usuário irá inserir se vai utilizar o IPv4 ou o IPv6 para acontecer a comunicação. Para o cliente, o sistema irá pedir o IP do host (obs: para que ocorra a comunicação, o cliente e o servidor precisam estar com o mesmo tipo de endereço IP).
4. Após, o host irá inserir a porta para a sala ser acessada, enquanto o sistema pergunta ao cliente qual a porta da sala que o cliente quer ter acesso.
4.1 Caso ocorra do usuário inserir um valor que não é válido em algum dos processos (ex: inserir um "j" ao invés de "h" para host e "c" para cliente), o sistema retoma o processo até que o valor válido seja inserido.
5. Para identificar o usuário (seja host ou cliente), o sistema pede para que seja inserido um apelido/nickname.
6. Após todo o processo de inserção dos dados, o programa estabelece um limite de 3 minutos para que outro usuário possa se conectar ao chat. Se não houver conexão, o processo é encerrado. 
7. Para se desconectar do chat, basta inserir o comando "/sair".

# Protocolo de camada de aplicação: 
- O CatChat utiliza a comunicação sobre os protocolos TCP ou UDP com suporte as camadas de redes IPv4 e IPv6. No momento da execução do programa, o usuário escolhe qual protocolo e qual transporte será utilizado para a comunicação, podendo ser host ou cliente.
- As mensagens são transmitidas em formato JSON convertido para UTF-8, tendo as chaves "apelido" (armazena o apelido do usuário no chat), "comando" armazena um comando especial de controle (ex: " desconectar" para encerrar a sessão) e "mensagem" (armazena o conteúdo da mensagem enviada).
- Na conexão TCP, o host cria um socket, faz bind no IP/porta inserida e aguarda a conexão do cliente. O cliente se conecta e, dessa forma, tanto o host quanto o cliente podem enviar e receber mensagens sem precisar se reconectar.
- Na conexão UDP, a comunicação ocorre por envio de pacotes independentes diretamente para o endereço e porta do destino, não tendo uma conexão persistente. Nesse protocolo, o host apenas espera receber dados vindos de qualquer IP/porta, mostrando que o protocolo UDP não traz garantia da chegada e da ordem da mensagem.

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

