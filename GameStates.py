from Logic import *
from GameCommand import *
import time

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
        if reply["type"] == "joinroom":
            self.game.ready += 1
            self.room.players.append(Player())
            for i in self.room.players:

                self.room.server.send()
            # send the roominfo Msg to every room players
        if self.room.ready == 4:
            self.room.gamecommand.assignInitCard()
            self.room.state = WaitChoiceState(self.room, self.server)


class WaitChoiceState(State):
    def __str__(self):
        return "Waiting for the choice of the players"

    def __init__(self, room, server):
        self.room = room
        self.server = server
    
    def ChangeToNextState(self, reply):
        
        self.room
        self.room.state = WaitCardState()


class WaitCardState(State):
    def __str__(self):
        return "Waiting for a card from player" + str(self.game.currentplayer) # ??

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        # reply = {"type":"playcard", "socket_id":22, "room":8, "room_id":1, "content":[66]}
        result = self.room.gamecommand.checkAll(reply["content"][0])
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
            self.room.gamecommand.drawCard()
            if self.room.checkZimo() == True:    #
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
        pass


# self.room.state.ChangeToNextState(__self__,reply)