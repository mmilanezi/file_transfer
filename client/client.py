import threading
import socket

# Configuração de acesso ao cliente
print('\nAPLICAÇÃO DE CHAT')
print('\nDigite o ip do servidor: padrão é localhost')
ip = input('\nIp do servidor de chat: ')
port = int(input('\nDigite a porta do servidor:'))


def main():
    # inicia a conexão socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET é ipv4 e SOCK_STREAM é TCP

    try:
        client.connect((ip, port))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
    
    # Tela de escolha de username
    print(f'Conectado em {ip}:{port}')
    username = input('Seu nome de usuário: ')
    print(f'Você escolheu o nome: {username}')

    # Inicia threads para envio e recebimento de mensagens
    thread1 = threading.Thread(target=recebeMensagens, args=[client])
    thread2 = threading.Thread(target=enviaMensagens, args=[client, username])
   
    thread1.start()
    thread2.start()


def recebeMensagens(client):
    # Envia mensagem pora o servidor
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione enter para sair!')
            client.close()
            break
            

def enviaMensagens(client, username):
    # Recebe mensagem do servidor
    while True:
        try:
            msg = input('\n')
            client.send(f'{username} diz: {msg}'.encode('utf-8'))
        except:
            return


main()