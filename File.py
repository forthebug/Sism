import socket
import threading

class ChatApp:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 55655

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        clients = []
        nicknames = []

        def broadcast(message):
            for client in clients:
                client.send(message)

        def handle(client):
            while True:
                try:
                    message = client.recv(1024)
                    broadcast(message)
                except:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    nicknames.remove(nickname)
                    broadcast(f'{nickname} left the chat!'.encode('ascii'))
                    break

        def receive():
            while True:
                client, address = server.accept()
                print(f"Connected with {str(address)}")

                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                nicknames.append(nickname)
                clients.append(client)

                print(f'Nickname of the client is {nickname}!')
                broadcast(f'{nickname} joined the chat!'.encode('ascii'))
                client.send('Connected to the server!'.encode('ascii'))

                thread = threading.Thread(target=handle, args=(client,))
                thread.start()

        print("Server Started!")
        receive()

    def start_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        nickname = input("Choose a nickname: ")
        client.send(nickname.encode('ascii'))

        def receive():
            while True:
                try:
                    message = client.recv(1024).decode('ascii')
                    if message == 'NICK':
                        client.send(nickname.encode('ascii'))
                    else:
                        print(message)
                except:
                    print("An error occurred!")
                    client.close()
                    break

        def write():
            while True:
                message = f'{nickname}: {input("")}'
                client.send(message.encode('ascii'))

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

def main():
    app = ChatApp()
    print(".")
    print("2.join the group")
    choice = input("Enter your choice: ")
    if choice == "132231":
        app.start_server()
    elif choice == "2":
        app.start_client()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
