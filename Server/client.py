import socket
import threading


class client:
    serverName = '127.0.0.1'
    serverPort = 5555
    server = None

    def open(self):
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsock.connect((self.serverName, self.serverPort))
        self.server = clientsock
        print("connect server successfully")
        new_thread = threading.Thread(target=self.receive, args=())
        new_thread.start()  # 开启线程


    def receive(self):
        while True:
            data = self.server.recv(2048)
            if data and data != b'quit':
                print(data.decode())
            else:
                self.server.close()
                print('connection closed')


if __name__ == '__main__':
    c = client()
    c.open()
