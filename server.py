from User import *
from Room import *
import socket
import threading
import json
import random


class server:
    serverName = '10.21.83.79'
    serverPort = 5555
    client = []
    rooms = {}

    def receive(self, clientsock):
        while True:
            data = clientsock.recv(2048)
            if data:
                data = json.loads(data.decode('utf-8'))
                print(data)
                if "code" in data:
                    clientsock.close()
                    print('connection closed')
                    return
                if data["type"] == "create":
                    roomid = random.randint(1000,9999)
                    self.rooms[roomid] = Room(roomid, self)
                    self.rooms[roomid].addUser(User(data["socket_id"]))
                    self.rooms[roomid].user_list[0].setName(data["content"])
                    roominfodic = {"type":"roominfo", "room": str(roomid),"room_id": 1,"name":data["content"]+" _ _ _", "ready":"0 0 0 0"}
                    self.send(int(data["socket_id"]), roominfodic)
                else:
                    if int(data["room"]) in self.rooms.keys():
                        self.rooms[int(data["room"])].state.changeToNextState(data)
                    else:
                        self.send(int(data["socket_id"]), {"type": "roomnotfound"})
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
            iddic = {"type": "id", "room":"-1","room_id":"-1","content":str(len(self.client))}
            self.send(len(self.client), iddic)
            print(address)
            print("a client has been connected")
            new_thread = threading.Thread(target=self.receive, args=(clientsock,))
            new_thread.start()

    def send(self, who, data):
        data = json.dumps(data)
        print(data)
        self.client[who-1].send(data.encode('utf-8'))


if __name__ == "__main__":
    s = server()
    s.open()

