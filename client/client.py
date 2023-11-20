import socket
import json
import os
import time
# Configurações do cliente
host = '127.0.0.1'
port = 5555

# Inicializar o socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Receber a mensagem de boas-vindas e ID do servidor
welcome_msg = client.recv(1024).decode()
print(welcome_msg)

def check_pending_files(client):
    # Enviar solicitação ao servidor para verificar arquivos pendentes
    msg_data = {
        "operation": "2",  # Operação para verificar arquivos pendentes
    }
    json_msg = json.dumps(msg_data)
    client.send(json_msg.encode())
    # Continuar daqui --------------------------------------------------------------------------------------------------------------
    # Aguardar resposta do servidor por alguns segundos
    try:
        file_status = client.recv(1024).decode()
        if file_status:
            # Exibir mensagem sobre o arquivo pendente
            print("Você tem um arquivo pendente para receber.")
            print(f'Mensagem do servidor: {file_status}')
            response = input("Deseja aceitar o arquivo? (S/N): ")

            if response.upper() == 'S':
                confirm_msg = {
                "response": 'S',  # Operação para confirmar o recebimento do arquivo
                }
                client.send(json.dumps(confirm_msg).encode())

                # Aguardar mensagem do servidor com informações sobre o arquivo
                file_info = json.loads(client.recv(1024).decode())
                file_name = file_info.get("file_name")
                file_data = client.recv(1024)

                # Criar pasta se não existir
                client_storage_directory = os.path.join(os.getcwd(), "received_files")
                if not os.path.exists(client_storage_directory):
                    os.makedirs(client_storage_directory)

                # Salvar o arquivo na pasta
                file_path = os.path.join(client_storage_directory, file_name)
                with open(file_path, 'wb') as received_file:
                    received_file.write(file_data)

                print(f"Arquivo recebido e salvo em {file_path}")
                print("Retornando ao menu principal.")
            else:
                print("Arquivo recusado. Retornando ao menu principal.")
        else:
            print("Não há arquivos pendentes para receber.")
    except:
        print("Não foi possível verificar os arquivos pendentes. Tente novamente mais tarde.")

while True:
    # Exibir menu de opções
    print("\nMenu de Opções:")
    print("1. Enviar arquivo")
    print("2. Verificar se há arquivo recebido")
    print("3. Sair")

    # Receber a escolha do usuário
    op = input("Escolha uma opção: ")

    if op == '1':
        
        # Solicitar ID do destinatário e caminho do arquivo
        dest_id = input("Digite o ID do destinatário: ")
        file_path = input("Digite o caminho do arquivo: ")
        file_path = file_path.replace('\\', '/')
        # Ler o arquivo e enviar para o servidor
        try:
            with open(os.path.join("send", file_path), 'rb') as file:

                # Criar um dicionário com as informações e converter para JSON
                msg_data = {
                    "operation": "1",
                    "dest_id": dest_id,
                    "file_name": os.path.basename(file_path)
                }
                json_msg = json.dumps(msg_data)
                # Enviar a mensagem JSON para o servidor
                client.send(json_msg.encode())
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')
                
                # Enviar o arquivo em partes
                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    client.send(file_data)
                    client.send("ARQUIVO_FINALIZADO".encode())
                    
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')
                
            
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')
                m_server = client.recv(1024).decode()
                print(f'Mensagem do servidor: {m_server}')

                
                

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file_path}")
    
    elif op == '2':
        # Solicitar se há algum arquivo recebido
        check_pending_files(client)
      
    elif op == '3':
        # Encerrar a conexão e sair
        client.send('2'.encode())
        client.close()
        break
    

    else:
        print("Opção inválida. Tente novamente.")



# Fechar a conexão
client.close()