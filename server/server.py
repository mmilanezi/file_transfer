import threading
import socket

clients = []
IP = '192.168.0.102'
PORT = 8000
def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print('Server online, aguardando!')

    try:
        server.bind((IP, PORT))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
        
        print(f'Clientes online: {clients}')

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()