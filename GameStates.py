# coding=utf-8

from Room import *
from User import *
import logging

roominfoupdata = {"type": "roominfo", "room": None, "room_id": None, "name": "", "ready": ""}
initcarddata = {"type": "initcard", "room": None, "room_id": None, "content": ""}
carddata = {"type": "card", "room": None, "room_id": None, "player": None, "content": ""}
pairdata = {"type": "pair", "room": None, "room_id": None, "content": ""}
askchoicedata = {"type": "askchoice", "room": None, "room_id": None, "content": None}
askcarddata = {"type": "askcard", "room": None, "room_id": None, "content": None}
playdata = {"type": "play", "room": None, "room_id": None, "player": None, "card": None}
hurequest = {"type": "specialope", "socket_id": 0, "room": None, "room_id": None,
             "chi1": None, "chi2": None, "chi3": None,
             "peng": None, "gang": None, "hu": "1"}
cpgdata = {"type":"cpg", "room": None, "room_id": None, "player": None, "card": None}

def sendmsgtogether(userlist, server, data):
    for i in userlist:
        if i is not None:
            data["room_id"] = str(i.room_id)
            server.send(int(i.socket_id), data)

def sendDrawCardData(userlist, server, room, player, card):
    carddata["room"] = str(room)
    carddata["player"] = str(player)
    carddata["content"] = str(card)
    sendmsgtogether(userlist, server, carddata)

def sendAskCardData(userlist, server, room, player_id):
    askcarddata["room"] = str(room)
    askcarddata["content"] = str(player_id)
    sendmsgtogether(userlist, server, askcarddata)

def sendPlayData(userlist, server, room, player, card):
    playdata["room"] = str(room)
    playdata["player"] = str(player)
    playdata["card"] = str(card)
    sendmsgtogether(userlist, server, playdata)


'''状态模式'''
class State:
    def __str__(self):
        return "----- Main State Class -----"

    def __init__(self, room, server):
        self.room = room
        self.server = server
        self.room.replies = []
        print(str(self))
        logging.debug(str(self))

    def ChangeToNextState(self, reply):
        pass


class WaitReadyState(State):
    def __str__(self):
        return "----- Wait Ready State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        # update according to the reply
        if reply["type"] == "joinroom":
            u = User(int(reply["socket_id"]))
            self.room.addUser(u)
            u.setName(reply["content"])
        elif reply["type"] == "ready":
            self.room.user_list[int(reply["room_id"]) - 1].setReady()
        elif reply["type"] == "cancelready":
            self.room.user_list[int(reply["room_id"]) - 1].setUnready()
        elif reply["type"] == "quitroom":
            self.room.removeUser(int(reply["room_id"]))

        # edit the json
        roominfoupdata["room"] = str(self.room.room_id)
        roominfoupdata["name"] = ""
        roominfoupdata["ready"] = ""
        for i in self.room.user_list:
            if i is None:
                roominfoupdata["name"] += '_ '
                roominfoupdata["ready"] += '0 '
                continue
            else:
                roominfoupdata["name"] += i.name + ' '
                if i.isready:
                    roominfoupdata["ready"] += '1 '
                else:
                    roominfoupdata["ready"] += '0 '
        roominfoupdata["name"] = roominfoupdata["name"][:-1]
        roominfoupdata["ready"] = roominfoupdata["ready"][:-1]
        sendmsgtogether(self.room.user_list, self.server, roominfoupdata)

        # go to create a game
        if self.room.checkReady():
            self.room.createGame()
            self.room.assignInitCard()
            initcarddata["room"] = str(self.room.room_id)
            initcarddata["content"] = ""
            for i in range(1, 5):
                for c in self.room.getHand(i):
                    initcarddata["content"] += str(c) + ' '
            initcarddata["content"] = initcarddata["content"][:-1]
            self.room.state = WaitSupervisorState(self.room, self.server)
            sendmsgtogether(self.room.user_list, self.server, initcarddata)


class WaitSupervisorState(State):
    def __str__(self):
        return "----- Wait Supervisor Choices State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        if reply["type"] == "supervisor":
            self.room.replies.append(reply)
        if len(self.room.replies) == 4:
            for c in self.room.replies:
                self.room.supervisorchoice[c["room_id"]] = int(c["content"])
            # get pairs of cards then go to next state
            self.room.paircards = self.room.generateFourPairs()
            pairdata["room"] = str(self.room.room_id)
            pairdata["content"] = ""
            for c in self.room.paircards:
                pairdata["content"] += '{} {} '.format(c[0], c[1])
            pairdata["content"] = pairdata["content"][:-1]

            self.room.state = WaitScoreState(self.room, self.server)
            sendmsgtogether(self.room.user_list, self.server, pairdata)


class WaitScoreState(State):
    def __str__(self):
        return "----- Wait Scores State -----"

    def __init__(self, room, server):
        super().__init__(room, server)
        self.room.replies = {}
        self.room.orders = []

    def ChangeToNextState(self, reply):
        if reply["type"] == "score":
            self.room.replies[reply["room_id"]] = int(reply["content"])
        if len(self.room.replies) == 4:
            self.room.orders = sorted(self.room.replies.items(), key=lambda e: e[1], reverse=True)
            self.room.state = WaitPairChoiceState(self.room, self.server)
            askchoicedata["room"] = str(self.room.room_id)
            askchoicedata["content"] = str(self.room.orders[0][0])
            sendmsgtogether(self.room.user_list, self.server, askchoicedata)


class WaitPairChoiceState(State):
    def __str__(self):
        return "----- Wait Pair Choices State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        carddata["room"] = str(self.room.room_id)
        if reply["type"] == "choice":
            carddata["player"] = reply["room_id"]
            pair = self.room.paircards[int(reply["content"]) - 1]
            carddata["content"] = "{} {}".format(pair[0], pair[1])
            self.room.assignPair(int(reply["room_id"]), pair)
            sendmsgtogether(self.room.user_list, self.server, carddata)

            if len(self.room.orders) > 1:
                self.room.orders = self.room.orders[1:]
                askchoicedata["room"] = str(self.room.room_id)
                askchoicedata["content"] = str(self.room.orders[0][0])
                sendmsgtogether(self.room.user_list, self.server, askchoicedata)
            else:
                if self.room.selectround == 1:
                    self.room.selectround += 1
                    self.room.paircards = self.room.generateFourPairs()
                    pairdata["room"] = str(self.room.room_id)
                    pairdata["content"] = ""
                    for c in self.room.paircards:
                        pairdata["content"] += '{} {} '.format(c[0], c[1])
                    pairdata["content"] = pairdata["content"][:-1]

                    self.room.state = WaitScoreState(self.room, self.server)
                    sendmsgtogether(self.room.user_list, self.server, pairdata)

                else:
                    card = self.room.drawCard()
                    sendDrawCardData(self.room.user_list, self.server, self.room.room_id, 1, card)

                    self.room.state = WaitCardState(self.room, self.server)
                    sendAskCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer())


class WaitCardState(State):
    def __str__(self):
        return "----- Wait Card Play State -----"

    def __init__(self, room, server):
        super().__init__(room, server)
        self.room.specialopelist = []
        self.room.cheackallresult = []

    def ChangeToNextState(self, reply):
        # Tell everyone what play
        if reply["type"] == "playcard":
            if int(reply["content"]) != -1:
                self.room.playCard(int(reply["content"]))
                sendPlayData(self.room.user_list, self.server, reply["room"], reply["room_id"], reply["content"])
                self.room.cheackallresult = self.room.checkAll(int(reply["content"]))
            else:
                randomcard = self.room.playRandomCard()
                sendPlayData(self.room.user_list, self.server, reply["room"], reply["room_id"], str(randomcard))
                self.room.cheackallresult = self.room.checkAll(randomcard)
            # Check if Chi Peng Gang Hu
            specialoperationflag = False
            for i in range(0, 4):
                specialopedata = {"type": "specialope", "room": str(self.room.room_id), "room_id": str(i + 1), "chi1": None,
                                  "chi2": None, "chi3": None, "peng": None, "gang": None, "hu": "0"}
                if self.room.cheackallresult[i][0] == 0:
                    specialopedata["chi1"] = None
                    specialopedata["chi2"] = None
                    specialopedata["chi3"] = None
                else:
                    specialoperationflag = True
                    if self.room.cheackallresult[i][1][0] is None:
                        specialopedata["chi1"] = None
                    else:
                        specialopedata["chi1"] = '{} {} {}'.format(self.room.cheackallresult[i][1][0][0], self.room.cheackallresult[i][1][0][1],
                                                                   self.room.cheackallresult[i][1][0][2])
                    if self.room.cheackallresult[i][1][1] is None:
                        specialopedata["chi2"] = None
                    else:
                        specialopedata["chi2"] = '{} {} {}'.format(self.room.cheackallresult[i][1][1][0], self.room.cheackallresult[i][1][1][1],
                                                                   self.room.cheackallresult[i][1][1][2])
                    if self.room.cheackallresult[i][1][2] is None:
                        specialopedata["chi3"] = None
                    else:
                        specialopedata["chi3"] = '{} {} {}'.format(self.room.cheackallresult[i][1][2][0], self.room.cheackallresult[i][1][2][1],
                                                                   self.room.cheackallresult[i][1][2][2])
                if self.room.cheackallresult[i][2] == 1:
                    specialoperationflag = True
                    specialopedata["peng"] = '{} {} {}'.format(self.room.cheackallresult[i][3][0], self.room.cheackallresult[i][3][1], self.room.lastcardid)
                if self.room.cheackallresult[i][4] == 1:
                    specialoperationflag = True
                    specialopedata["gang"] = '{} {} {} {}'.format(self.room.cheackallresult[i][5][0], self.room.cheackallresult[i][5][1], self.room.cheackallresult[i][5][2],
                                                                  self.room.lastcardid)
                if self.room.cheackallresult[i][6] == 1:
                    specialoperationflag = True
                    specialopedata["hu"] = "1"

                self.room.specialopelist.append(specialopedata)

            if specialoperationflag:
                self.room.state = WaitSpecailReplyState(self.room, self.server)
                for i in range(0, 4):
                    playerid = int(self.room.specialopelist[i]["room_id"])
                    if self.room.user_list[playerid-1] is not None:
                        self.server.send(int(self.room.user_list[playerid-1].socket_id), self.room.specialopelist[i])
            else:
                card = self.room.drawCard()
                sendDrawCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer(), card)
                # Need to ensure the Hu check Code
                if self.room.checkHu(self.room.getCurrentPlayer()):  # 发现可以自摸
                    self.room.state = WaitZimoState(self.room, self.server)
                    hurequest["room"] = str(self.room.room_id)
                    hurequest["room_id"] = str(self.room.getCurrentPlayer())
                    self.server.send(self.room.user_list[self.room.getCurrentPlayer()].socket_id, hurequest)
                else:
                    self.room.state = WaitCardState(self.room, self.server)
                    sendAskCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer())



class WaitSpecailReplyState(State):
    def __str__(self):
        return "----- Wait Special Operation Replies State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        self.room.replies.append(reply)
        if len(self.room.replies) == 4:
            maxchoiceplayer = 0
            maxchoice = 0
            # 操作优先级：胡>杠>碰>吃，同时出现多个玩家可以操作的时候，按这种顺序决定执行谁的操作
            for r in self.room.replies:
                if int(r["content"]) > maxchoice:
                    maxchoice = int(r["content"])
                    maxchoiceplayer = int(r["room_id"])
                # 暂不考虑两人同时胡的时候的比较判断
            print("maxchoiceplayer: "+ str(maxchoiceplayer) + " maxchoice: "+ str(maxchoice))
            if maxchoice == 0:
                card = self.room.drawCard()
                sendDrawCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer(), card)
                if self.room.checkHu(self.room.getCurrentPlayer()):     # 发现可以自摸
                    self.room.state = WaitZimoState(self.room, self.server)
                    hurequest["room"] = str(self.room.room_id)
                    hurequest["room_id"] = str(self.room.getCurrentPlayer())
                    self.server.send(self.room.user_list[self.room.getCurrentPlayer()].socket_id, hurequest)
                else:
                    self.room.state = WaitCardState(self.room, self.server)
                    sendAskCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer())
                return
            elif maxchoice == 1:
                self.room.Chi(maxchoiceplayer, self.room.lastcardid, 0)
                chicards = self.room.cheackallresult[maxchoiceplayer-1][1][0]
                cpgdata["card"] = "{} {} {}".format(chicards[0], chicards[1], chicards[2])
                cpgdata["room"] = str(self.room.room_id)
                cpgdata["player"] = str(maxchoiceplayer)
                sendmsgtogether(self.room.user_list, self.server, cpgdata)
            elif maxchoice == 2:
                self.room.Chi(maxchoiceplayer, self.room.lastcardid, 1)
                chicards = self.room.cheackallresult[maxchoiceplayer-1][1][1]
                cpgdata["card"] = "{} {} {}".format(chicards[0], chicards[1], chicards[2])
                cpgdata["room"] = str(self.room.room_id)
                cpgdata["player"] = str(maxchoiceplayer)
                sendmsgtogether(self.room.user_list, self.server, cpgdata)
            elif maxchoice == 3:
                self.room.Chi(maxchoiceplayer, self.room.lastcardid, 2)
                chicards = self.room.cheackallresult[maxchoiceplayer-1][1][2]
                cpgdata["card"] = "{} {} {}".format(chicards[0], chicards[1], chicards[2])
                cpgdata["room"] = str(self.room.room_id)
                cpgdata["player"] = str(maxchoiceplayer)
                sendmsgtogether(self.room.user_list, self.server, cpgdata)
            elif maxchoice == 4:
                self.room.Peng(maxchoiceplayer, self.room.lastcardid)
                pengcards = self.room.cheackallresult[maxchoiceplayer-1][3]
                cpgdata["card"] = "{} {} {}".format(pengcards[0], pengcards[1], self.room.lastcardid)
                cpgdata["room"] = str(self.room.room_id)
                cpgdata["player"] = str(maxchoiceplayer)
                sendmsgtogether(self.room.user_list, self.server, cpgdata)
            elif maxchoice == 5:
                self.room.Gang(maxchoiceplayer, self.room.lastcardid)
                gangcards = self.room.cheackallresult[maxchoiceplayer-1][5]
                cpgdata["card"] = "{} {} {} {}".format(gangcards[0], gangcards[1], gangcards[2], self.room.lastcardid)
                cpgdata["room"] = str(self.room.room_id)
                cpgdata["player"] = str(maxchoiceplayer)
                sendmsgtogether(self.room.user_list, self.server, cpgdata)

                card = self.room.drawCard()
                sendDrawCardData(self.room.user_list, self.server, self.room.room_id, maxchoiceplayer, card)
            elif maxchoice == 6:
                self.room.Hu(maxchoiceplayer)
                # send Hu description
                # if delete player?


            self.room.state = WaitCardState(self.room, self.server)
            sendAskCardData(self.room.user_list, self.server, self.room.room_id, maxchoiceplayer)


class WaitZimoState(State):
    def __str__(self):
        return "----- Wait Zimo Reply State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        if reply["hu"] is None:
            self.room.state = WaitCardState(self.room, self.server)
            sendAskCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer())
        else:
            self.room.state = WaitCardState(self.room, self.server)
            self.room.Hu(reply["room_id"])
            # delete player
            # 是否需要nextPlayer()?不需要的话可以直接结算然后结束游戏
            card = self.room.drawCard()
            sendDrawCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer(), card)
            sendAskCardData(self.room.user_list, self.server, self.room.room_id, self.room.getCurrentPlayer())


