import socket
import select

class Server:

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.HEADER_LENGTH = 10
        self.enc = 'utf-8'

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()

        self.sockets_list = [self.socket]
        self.clients = {}

        print('Server is up')

    def select_handle(self):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
        return (read_sockets, exception_sockets)
            
    def recieve_message(self, socket):
        
        try:
            message_header = socket.recv(self.HEADER_LENGTH)

            if not len(message_header):
                return False
            
            message_length = int(message_header.decode(self.enc).strip())

            return {'header':message_header, 'data':socket.recv(message_length)}

        except:
            return False
    
    def broadcast_message(self, notified_socket, message):

        user = self.clients[notified_socket]
        print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                
        for client_socket in self.clients:
            if client_socket != notified_socket:
                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    def handle_other_exception(self, exception_sockets):
        for notified_socket in exception_sockets:
            
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]



