from Logic import *
from Room import *
from User import *
import json
import time
import random


def sendmsgtogether(userlist, server, data):
    for i in userlist:
        data["room_id"] = str(i.room_id)
        server.send(i.socket_id,json.dumps(data).encode('utf-8'))


'''状态模式'''
class State:
    def __str__(self):
        return "This is a Main State Class"

    def __init__(self, room, server):
        self.room = room
        self.server = server
    
    def ChangeToNextState(self, reply):
        # 需要一个服务器每次收到消息都执行ChangeToNextState()的方法
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
        roominfoupdate = {"type":"roominfo", "room":room.room_id, "room_id":None, "name":"", "ready":None}
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
        sendmsgtogether(self.room.user_list, self.server, roominfoupdate)

        # go to create a game
        if self.room.checkready == True:
            college = self.room.createGame()
            collegelostmsg = {"type":"college", "room":self.room.room_id, "room_id":None, "content":"{} {}".format(college[0], college[1])}
            sendmsgtogether(self.room.user_list, self.server, collegelostmsg)   # send college ID that will not appear in this game

            self.room.state = WaitSupervisorState(self.room, self.server)
        

class WaitSupervisorState(State):
    def __str__(self):
        return "Waiting for the choice of the supervisor"

    def __init__(self, room, server):
        self.room = room
        self.server = server
        self.room.replies = []  # need to use it store 4 replies

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        if reply["type"] == "supervisor":
            # 需要player对象里有存supervisor的变量
            pass
        if self.room.supervisorchoice == True:  # 需要有一个检测supervisor是否都选了的方法

            # init 9 cards for 4 players
            self.room.assignInitCard()
            carddata = {"type":"initcard", "room":room.room_id, "room_id":None, "content":""}
            for i in range(1, 5):
                for c in self.room.getHand(i):
                    carddata["content"] += str(c) + ' '
            sendmsgtogether(self.room.user_list, self.server, carddata)

            # get pairs of cards then go to next state
            pairdata = {"type":"pair", "room":room.room_id, "room_id":None, "content":""}
            for c in self.room.generateFourPairs():
                pairdata["content"] += '{} {} '.format(c[0], c[1])
            sendmsgtogether(self.room.user_list, self.server, pairdata)

            self.room.state = WaitScoreState(self.room, self.server)


class WaitScoreState(State):
    def __str__(self):
        return "Waiting for the choice of the scores"

    def __init__(self, room, server):
        self.room = room
        self.server = server
        self.room.replies = []  # need to use it store 4 replies

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        if reply["type"] == "supervisor":
            self.room.replies.append(reply)
            # 这里我还需要根据下面需要的的内容再改

        if len(self.room.replies) == 4:
            
            # 需要有一个根据积分排出先后顺序的方法，并且需要一个长度为8的数组(可以暂定为chooseorder)记录这个顺序(顺序是一个回文)
            self.room.state = WaitPairChoiceState(self.room, self.server)


class WaitPairChoiceState(State):
    def __str__(self):
        return "Waiting for the choice of the card pairs"

    def __init__(self, room, server):
        self.room = room
        self.server = server
        self.selectround = 0    # there are 8 rounds in choose pairs, this is a counter to record the round

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        if reply["type"] == "choice":
            # 仍需敲定细节
            self.selectround += 1
            # sendmsgtogether
        if self.selectround == 8:
            self.room.state = WaitCardState()


class WaitCardState(State):
    def __str__(self):
        return "Waiting for a card from player"

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        self.room.playCard(reply["content"][0])
        result = self.room.checkAll(reply["content"][0])
        specialoperationflag = False
        specialopedata = {"type":"specialope", "room":str(self.room.room_id), "room_id":None, "chi1":None, "chi2":None, "chi3":None, "peng":None,"gang":None, "hu":"0"}
        
        for i in range(0,4):
            if result[i][0] == 1:
                specialopedata["chi1"] = '{} {} {}'.format(result[i][1][0], result[i][1][1], result[i][1][2])
            elif result[i][0] == 2:
                specialopedata["chi1"] = '{} {} {}'.format(result[i][1][0], result[i][1][1], result[i][1][2])
                specialopedata["chi2"] = '{} {} {}'.format(result[i][1][3], result[i][1][4], result[i][1][5])
            elif result[i][0] == 3:
                specialopedata["chi1"] = '{} {} {}'.format(result[i][1][0], result[i][1][1], result[i][1][2])
                specialopedata["chi2"] = '{} {} {}'.format(result[i][1][3], result[i][1][4], result[i][1][5])
                specialopedata["chi3"] = '{} {} {}'.format(result[i][1][6], result[i][1][7], result[i][1][8])
            if result[i][2] == 1:
                specialopedata["peng"] = '{} {} {}'.format(result[i][3][0], result[i][1][1], result[i][1][2])
            if result[i][4] == 1:
                specialopedata["gang"] = '{} {} {} {}'.format(result[i][5][0], result[i][5][1], result[i][5][2], result[i][5][3])
            if result[i][6] == 1:
                specialopedata["hu"] = "1"
            self.server.send(self.room.user_list[i].socket_id, json.dumps(specialopedata).encode('utf-8'))
    
        if specialoperationflag == True:
            self.room.replies = []
            self.room.state = WaitSpecailReplyState(self.room, self.server)
        else:
            self.room.drawCard()
            for i in range(1,5):
                if self.room.checkHu(i) == True:
                    hurequest = {"type":"specialope", "socket_id":0,"room":str(self.room.room_id), "room_id":str(self.room.currentplayer), "chi1":None, "chi2":None, "chi3":None, "peng": None,"gang": None, "hu":"1"}
                    self.server.send(self.room.user_list[i].socket_id, json.dumps(hurequest).encode('utf-8'))
                    self.room.state = WaitZimoState(self.room, self.server)
                else:
                    self.room.state = WaitCardState(self.room, self.server)

     
class WaitSpecailReplyState(State):
    def __str__(self):
        return "Waiting for the reply/replies of specail operation"
    
    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))
        self.room.replies.append(reply)
        if len(self.room.replies) == 4:
            highestchoice = 0   # 需要一个方法根据操作的优先级和编号来决定操作由谁做
            for r in self.room.replies:
                pass
        

class WaitZimoState(State):
    def __str__(self):
        return "Waiting for a reply of Zi Mo"

    def __init__(self, room, server):
        self.room = room
        self.server = server

    def ChangeToNextState(self, reply):
        reply = json.loads(reply.decode('utf-8'))

        if reply["hu"] is None:
            self.room.nextPlayer()
            self.room.drawCard()
            self.room.state = WaitCardState(self.room, self.server)
        else:
            self.room.Hu(reply["room_id"])
            self.room.drawCard()
            self.room.state = WaitCardState(self.room, self.server)

