import socket
import threading
import os
import json

# Variável de controle para evitar condição de corrida em clients
clients_lock = threading.Lock()
server_directory = os.path.dirname(os.path.realpath(__file__))

# Função para lidar com a conexão de cada cliente
def handle_client(client_socket, client_id):
    
    global clients
    
    print(f"Conexão estabelecida com o Cliente {client_id}")

    # Enviar boas-vindas e ID ao cliente
    client_socket.send(f"Bem-vindo, Cliente Seu ID: {client_id}!".encode())
    
    with clients_lock:  # Usar Lock ao acessar clients
       clients[client_id] = client_socket
    
    print(f"Todos os clientes {clients}")
    
    while True:
        try:
            # Receber a mensagem do cliente
            data_bruto = client_socket.recv(1024).decode() 
                       
            try:
                # Converter a mensagem JSON para um dicionário Python
                data = json.loads(data_bruto)
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON do Cliente {client_id}: {str(e)}")
                continue
            
            print(f'json: {data}')
            # operation = data.get("operation")
            
            # Verificar a existência da chave "operation" no dicionário
            if "operation" in data:
                # Extrair a operação do dicionário
                operation = data["operation"]
                           
                if operation == '1':
                    # Operação para enviar arquivo
                    dest_id = str(data.get("dest_id"))
                    
                    # Criar a pasta de armazenamento se não existir
                    client_storage_directory = os.path.join(server_directory, "storage", str(client_id))
                    print(f'Caminho ou nome do arquivo: {client_storage_directory}')
                    if not os.path.exists(client_storage_directory):
                        os.makedirs(client_storage_directory)
                    
                    # Receber o arquivo do cliente e armazenar no servidor
                    file_name = data.get("file_name")
                    # file_path = f"{client_storage_directory}\{file_name}"
                    file_path = os.path.join(client_storage_directory, file_name)
                    # Aviso para o cliente enviar o arquivo
                    client_socket.send("Dados recebidos, pronto para receber o arquivo".encode())
                    
                    with open(file_path, 'wb') as file:
                        while True:
                            file_data = client_socket.recv(1024)
                            print(f'Conteudo: {file_data}')
                            # if not file_data or file_data == b'ARQUIVO_FINALIZADO':
                            if not file_data:
                                break
                            file.write(file_data)
                            break
                                     
                    print(f"Arquivo recebido e armazenado em {file_path}")
                    client_socket.send(f"Arquivo recebido com sucesso, enviando ao destinatário ID:{dest_id} Nome: {file_name}".encode())

                    # Enviar aviso para o destinatário
                    dest_socket = clients[int(dest_id)]
                    send_file(dest_socket, client_id, dest_id, client_socket, file_path)
                    

                elif operation == '2':
                    # Operação para sair
                    print(f"Cliente {client_id} desconectado.")
                    with clients_lock:  # Usar Lock ao acessar clients
                        del clients[client_id]
                    break
                else:
                    print(f"Operação inválida recebida do Cliente {client_id}: {operation}")

        except Exception as e:
            print(f"Erro na conexão com o Cliente {client_id}: {str(e)}")
            with clients_lock:  # Usar Lock ao acessar clients
                del clients[client_id]
            break
    client_socket.close()

def send_file(dest_socket, client_id, dest_id, client_socket, file_path):
    
    # Aguardar resposta do destinatário
    dest_socket.send(f"O Cliente {client_id} deseja enviar um arquivo. Aceitar? (S/N)".encode())
    msg = dest_socket.recv(1024).decode()
    
    if "response" in msg:
        response = msg['response']
    
    print(f"responsta cliente: {response}")
    
    if response.upper() == 'S':

        # Receber a resposta do destinatário
        # Enviar confirmação para o remetente
        client_socket.send(f"O Cliente {dest_id} aceitou o arquivo. Iniciando transferência...".encode())
        
        with open(os.path.join("send", file_path), 'rb') as file:
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                dest_socket.send(file_data)
                dest_socket.send("ARQUIVO_FINALIZADO".encode())
        
        # Salve os dados recebidos no arquivo do destinatário
        with open(f"arquivo_{client_id}.txt", 'wb') as received_file:
            received_file.write(file_data)
            

        # Informar ao destinatário sobre a conclusão da transferência
        dest_socket.send("Transferência concluída!".encode())

    else:
        # Informar ao remetente que o destinatário recusou o arquivo
        client_socket.send(f"O Cliente {dest_id} recusou o arquivo.".encode())
        
                   
# Configurações do servidor
host = '127.0.0.1'
port = 5555

# Inicializar o socket do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Servidor ouvindo em {host}:{port}")
clients = {}
print(f"Todos os clientes {clients}")
# Loop principal para aceitar conexões e iniciar threads para cada cliente
client_id_counter = 1
while True:
    client_socket, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id_counter))
    client_handler.start()
    client_id_counter += 1
    print(f"Servidor ouvindo em {host}:{port}")
    