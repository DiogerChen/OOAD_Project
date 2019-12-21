# coding=utf-8

from Room import *
import socket
import threading
import json
import random
import datetime
import logging
import os
import time


class server:
    serverName = '10.21.41.131'
    serverPort = 5555
    client = []
    rooms = {}

    def receive(self, clientsock):
        while True:
            data = clientsock.recv(2048)
            if data:
                data = json.loads(data.decode('utf-8'))
                print("Client send: " + str(data))
                logging.debug("Client send: " + str(data))
                if 'code' in data:
                    clientsock.close()
                    print('connection closed')
                    return
                if data["type"] == "quitGame":
                    clientsock.close()
                    print('connection closed')
                    return
                if data["type"] == "create":
                    roomid = random.randint(1000,9999)
                    self.rooms[roomid] = Room(roomid, self)
                    self.rooms[roomid].addUser(User(data["socket_id"]))
                    self.rooms[roomid].user_list[0].setName(data["content"])
                    roominfodic = {"type":"roominfo", "room": str(roomid),"room_id": 1,
                                   "name":data["content"]+" _ _ _", "ready":"0 0 0 0"}
                    self.send(int(data["socket_id"]), roominfodic)
                else:
                    if int(data["room"]) in self.rooms.keys():
                        self.rooms[int(data["room"])].ChangeToNextState(data)
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
        print("Server send: " + str(data))
        logging.debug("Server send: " + str(data))
        self.client[int(who)-1].send(data.encode('utf-8'))
        time.sleep(0.05)    # Unity是逐帧更新，发包间隔过短很有可能会让前端收不到消息


if __name__ == "__main__":
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
        format="%(message)s",  # 定义输出log的格式
        filename=datetime.datetime.now().strftime('Logs/%Y-%m-%d_%H-%M-%S.txt'),
        filemode='w')

    s = server()
    s.open()
