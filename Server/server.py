import socket
import threading

class server:
    serverName = '10.21.82.248'
    serverPort = 5555
    client = []
    rooms = {}

    def receive(self, clientsock):
        while True:
            data = clientsock.recv(2048)
            if data and data != b'quit':
                data = data.decode('utf-8')
                print(data)
            else:
                clientsock.close()
                print('connection closed')
                return

    def open(self):
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.bind((self.serverName, self.serverPort))
        serversock.listen(10)
        print("open server successfully")
        while True:
            clientsock, address = serversock.accept()
            self.client.append(clientsock)
            print(address)
            print("a client has been connected")
            new_thread = threading.Thread(target=self.receive, args=(clientsock,))
            new_thread.start()

    def send(self, who, data):
        self.client[who-1].send(data)


if __name__ == "__main__":
    s = server()
    s.open()
