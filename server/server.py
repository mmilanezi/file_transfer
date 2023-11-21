import threading
import socket

# lista de clientes
clients = []

# Dados do servidor para conexão
IP = 'localhost'
PORT = 8000

def main():
    # Inicia o socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET é ipv4 e SOCK_STREAM é TCP
    
    print('Server online, aguardando novas conexões!')

    try:
        server.bind((IP, PORT))
        server.listen() # Listen sem parametros, sem limite de clientes.
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        # Laço principal de conexão. Aceita novas conexões
        client, addr = server.accept()
        clients.append(client)
        print(f'\nNovo cliente: {client} IP: {addr}')
        print(f'\nLista de clientes online: {clients}')

        # Coloca cada cliente em uma nova thread
        thread = threading.Thread(target=recebeMensagens, args=[client])
        thread.start()

def recebeMensagens(client):
    # Método para receber mensagens de clientes e verifica se o cliente ainda está conectado.
    # Caso não esteja, deleta o registro do cliente.
    while True:
        try:
            msg = client.recv(2048) # Buffer de 2048 bytes
            enviaMensagem(msg, client)
        except:
            deletarCliente(client)
            break


def enviaMensagem(msg, client):
    # Envia para todos os clientes a mensagem que recebeu.
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deletarCliente(clientItem)


def deletarCliente(client):
    # remove registros de clientes inativos
    clients.remove(client)
    print(f'\nCliente desconectado{client}')

main()