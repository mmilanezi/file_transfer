import threading
import socket
import PySimpleGUI as sg

IP = '192.168.0.102'
PORT = 8000

# Layout janela
layout_inicial = [
    [sg.Text("Nome de usuário: ")],
    [sg.Input()],
    [sg.Button('Ok'), sg.Button('Sair')]]

chat = [
    [],
    [sg.Text("Digite sua mensagem:")],
    [sg.InputText(key='-INPUT-', size=(40, 1)), sg.Button('Enviar')],
]
def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((IP, PORT))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    window = sg.Window('Chat de rede',layout_inicial)
    
    while True:
        event, values = window.read()
        username = values[0]   
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Ok':
            window.close()
            window = sg.Window('Chat de rede', chat)
            # event, values = window.read()
        if event == "Enviar":
            window = sg.Window('Chat de rede', chat)

    # username = input('Usuário> ')

    print(username)

    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client, window])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    
    thread1.start()
    thread2.start()


def receiveMessages(client, window):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
            window.write_event_value('-INCOMING-', msg)
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()