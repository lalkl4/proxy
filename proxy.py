import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        data = client_socket.recv(4096)
        if len(data) == 0:
            break
        remote_socket.send(data)
        
        remote_response = remote_socket.recv(4096)
        client_socket.send(remote_response)

    client_socket.close()
    remote_socket.close()

def main():
    local_host = '127.0.0.1'  # Локальный адрес, на котором будет работать прокси
    local_port = 8080  # Локальный порт

    remote_host = 'www.example.com'  # Хост, к которому будет пересылать запросы
    remote_port = 80  # Порт удаленного хоста

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)

    print(f'Прокси слушает на {local_host}:{local_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Принято соединение с {addr[0]}:{addr[1]}')
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()

if __name__ == '__main__':
    main()