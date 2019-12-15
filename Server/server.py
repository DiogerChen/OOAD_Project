import socket
import threading
import json
import random
import Room

class server:
    serverName = '127.0.0.1'
    serverPort = 5555
    client = []
    self.rooms = {}

    def receive(self, clientsock):
        while True:
            data = clientsock.recv(2048)
            if data and data != b'quit':
                data = json.loads(data.decode('utf-8'))
                print(data.decode())
                if data["type"] == "createroom":
                    roomid = random.randint(1000,9999)
                    self.rooms[roomid] = Room(roomid)
                    # send roominfo
                else:
                    self.rooms[data["room"]].state.changeToNextState(data)
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
            self.send(len(client), clientsock)
            print(address)
            print("a client has been connected")
            new_thread = threading.Thread(target=self.receive, args=(clientsock,))
            new_thread.start()

    def send(self, who, data):
        self.client[who-1].send(data)


if __name__ == "__main__":
    s = server()
    s.open()
