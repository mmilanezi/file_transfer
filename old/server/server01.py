import socket
import threading
import random
import os

class fileServer():

    def __init__(self, ip, port, buffer=1024):

        self.__ip = ip
        self.__port = port
        self.__buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None
        self.addr = None

        self.data_address = None
        self.datasock = None

        self.mode = 'I'
        
        self.user_ids = {}
        

    def gerar_id(self):
        novo_id = random.randint(1, 1000)
        while novo_id in self.ids_em_uso:
            novo_id = random.randint(1, 1000)
        self.ids_em_uso.append(novo_id)
        return novo_id
    
    def bind(self):
        '''
            Wait a client's connection.

            Return a connection and address.
        '''
        self.socket.bind((self.__ip, self.__port))
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()
        
        
    def receive(self):
        ''' Receive data from the socket.

            The return value is a string representing the data received.
        '''

        return self.conn.recv(self.__buffer)
    
    def port(self, data):
        
        cmd_addr = data.split(" ")
        cmd_ip_port = cmd_addr[1].split(",")

        ip = ".".join(str(x) for x in cmd_ip_port[0:4])
        port = cmd_ip_port[-2:]
        port =  int(port[0])*256 + int(port[1])
        
        server.data_address = (ip, port)

        send = '200  Port command successfull.\r\n'
        server.conn.send(send.encode())    

    def download(self,data):
        '''
            Send file in batches with the buffer size
        '''
        filename = data.split(" ")[1]
        
        print('Download file... ',filename)

        try:
            filesize = os.path.getsize(filename)
        except: 
            self.conn.send(("550 can't access file '{}'.\r\n").format(filename).encode())
            return

        
        
        
        self.datasock.close()
        

    def upload(self, data):
        '''
            Receive a file from client and save it in chunks
        '''

        # str_size = struct.unpack("i", self.conn.recv(4))[0]

        # filename = self.conn.recv(str_size)
        filename = data.split(" ")[1]
        
        print('Upload file... ',filename)

        self.conn.send('150 Opening data connection.\r\n'.encode())

        self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.datasock.connect(self.data_address)

        readmode = 'wb' if  self.mode == 'I' else 'w'

        try:
            with open(filename, readmode) as f:
                
                while True:
                    bytes_recieved = self.datasock.recv(self.__buffer)
                    
                    if not bytes_recieved: break

                    f.write(bytes_recieved)

            self.conn.send('226 Transfer complete.\r\n'.encode())        
        except:
            self.conn.send("550 can't access file .\r\n".encode())
        
        self.datasock.close()
    
        print('Upload Successful\n')
    

if __name__ == "__main__":
    # FTP SERVER SETUP
    
    IP = '127.0.0.1'
    PORT = 2330

    server = fileServer(IP, PORT)
    
    print('FTP Server - {}:{} \n'.format( IP, PORT))
    print('This FTP server only works in passive mode\n')
    print('Binding... \n')
    
    server.bind()
   
    server.welcome_message()
        
    while True:
      
        
        print("Waiting instructions \n")

        data = server.receive()
        
        if not data: break

        data = data.decode()
       
        print("Received instruction: {0}\n".format(data))

        data_arr = data.split('\r\n')[:-1]
        
        
        for i in range(0,len(data_arr)):
            
            data = data_arr[i]

            if  data == "PWD" :
                server.pwd()
            elif data == "LIST" : 
                server.list_files()
            elif "PORT" in data:
                server.port(data)
            elif "CWD" in data:
                server.chdir(data) 
            elif "USER" in data:
                server.user(data)
            elif "PASS" in data:
                server._pass(data) 
            elif  "TYPE" in data:
                server._type(data)
            elif  "RETR" in data:
                server.download(data)
            elif "STOR" in data:  
                server.upload(data)
            elif  "ABOR" in data:
                server.abor()        
            elif data == 'PASV':
                server.pasv()
           

            elif data == "QUIT":

                server.quit()
                break
            else: 
                send = '220 starting connection funcioned tunino.\r\n'
                server.conn.send(send.encode())

            data = None