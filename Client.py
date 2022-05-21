import socket
import errno
import sys
import threading

def send_message(client_socket, HEADER_LENGTH):
    while True:
        message = input('[---]>')

    
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

def recieve_message(client_socket, HEADER_LENGTH):
    while True:
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server: \n')
                    sys.exit()
                
                username_lenth = int(username_header.decode('utf-8').strip())

                username = client_socket.recv(username_lenth).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message  = client_socket.recv(message_length).decode('utf-8')

                print(f'{username} > {message}')
        except IOError as e:
            
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()       

if __name__ == '__main__':

    
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 1234
    my_username = input("Username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    write_thread = threading.Thread(target=send_message, args=(client_socket, HEADER_LENGTH,))
    write_thread.start()

    recieve_thread = threading.Thread(target=recieve_message, args=(client_socket, HEADER_LENGTH,))
    recieve_thread.start()


