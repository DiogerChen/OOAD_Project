from Logic import *
from Room import *
from User import *
import json
import time
import random

# 状态模式
class State:
    def __str__(self):
        return "This is a Main State Class"

    def __init__(self, room, server):   ###
        self.room = room
        self.server = server
    
    def ChangeToNextState(self, reply):
        pass


class WaitReadyState(State):
    def __str__(self):
        return "Waiting for the ready reply"

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        # update according to the reply
        if reply["type"] == "joinroom":
            self.room.addUser(User(reply["socket_id"]))
        elif reply["type"] == "ready":
            self.game.user_list[reply["room_id"]].setReady()
        elif reply["type"] == "cancelready":
            self.game.user_list[reply["room_id"]].setUnready()
        elif reply["type"] == "quitroom":
            self.game.removeUser(reply["room_id"])
        # edit the json
        roominfoupdate = {"type":"roominfo", "room":room.room_id,"room_id":None, "name":"", "ready":None}
        for i in self.room.user_list:
            if i is None:
                roominfoupdate["name"] += '_ '
                roominfoupdate["ready"] += '0 '                
                continue
            else:
                roominfoupdate["name"] += i.name + ' '
                if i.isready == True:
                    roominfoupdate["ready"] += '1 '
                else:
                    roominfoupdate["ready"] += '0 '
        # send the roominfo Msg to every room players        
        for i in self.room.user_list:
            roominfoupdate["room_id"] = str(i.room_id)
            self.room.server.send(i.socket_id,json.dumps(roominfoupdate).encode('utf-8'))
        # go to the next state
        if self.room.checkready == True:
            self.college = self.room.createGame()
            self.room.assignInitCard()
            self.room.state = WaitSupervisorState(self.room, self.server)
        

class WaitSupervisorState(State):
    def __str__(self):
        return "Waiting for the choice of the supervisor"

    def __init__(self, room, server):
        self.room = room
        self.server = server


class WaitPairChoiceState(State):
    def __str__(self):
        return "Waiting for the choice of the card pairs"

    def __init__(self, room, server):
        self.room = room
        self.server = server
    
    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        self.room
        self.room.state = WaitCardState()


class WaitCardState(State):
    def __str__(self):
        return "Waiting for a card from player"

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        result = self.room.checkAll(reply["content"][0])
        specialoperationflag = False
        self.room.requestsend = 0     # 发送的请求数，对应的需要收到相应数目的回复
        for r in result:
            if r is not None:
                specialoperationflag = True
                self.room.requestsend += 1

                # Send Msg
        if specialoperationflag == True:
            self.room.replies = []
            self.room.state = WaitSpecailReplyState(self.room.requestsend)
        else:
            self.room.drawCard()
            if self.room.checkHu() == True:    #
                self.room.state = WaitZimoState()
                self.server.send(self.game.currentplayer, "")   #
            else:

                self.room.state = WaitCardState()
                
                #self.room.WaitSpecailReplyState = WaitSpecailReplyState()

     
class WaitSpecailReplyState(State):
    def __str__(self):
        return "Waiting for the reply/replies of specail operation"
    
    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        self.replies.append(reply)
        self.needtorecieve -= 1
        if self.needtorecieve == 0:
            #
            pass
        

class WaitZimoState(State):
    def __str__(self):
        return "Waiting for a reply of Zi Mo"

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
