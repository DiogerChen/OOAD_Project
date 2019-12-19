from Room import *
from User import *
import logging
import time


roominfoupdata = {"type": "roominfo", "room": None, "room_id": None, "name": "", "ready": ""}
initcarddata = {"type": "initcard", "room": None, "room_id": None, "content": ""}
carddata = {"type": "card", "room": None, "room_id": None, "player": None, "content": ""}
pairdata = {"type": "pair", "room": None, "room_id": None, "content": ""}
askdata = {"type": "askchoice", "room": None, "room_id": None, "content": None}
playdata = {"type": "play", "room": None, "room_id": None, "player": None, "card": None}
specialopedata = {"type": "specialope", "room": None, "room_id": None, "chi1": None,
                  "chi2": None, "chi3": None, "peng": None, "gang": None, "hu": "0"}
hurequest = {"type": "specialope", "socket_id": 0, "room": None, "room_id": None,
                                 "chi1": None, "chi2": None, "chi3": None,
                                 "peng": None, "gang": None, "hu": "1"}

def sendmsgtogether(userlist, server, data):
    for i in userlist:
        if i is not None:
            data["room_id"] = str(i.room_id)
            server.send(int(i.socket_id), data)


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
        # 需要一个服务器每次收到消息都执行ChangeToNextState()的方法
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
            sendmsgtogether(self.room.user_list, self.server, initcarddata)
            self.room.state = WaitSupervisorState(self.room, self.server)


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
            sendmsgtogether(self.room.user_list, self.server, pairdata)

            self.room.state = WaitScoreState(self.room, self.server)


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
            askdata["room"] = str(self.room.room_id)
            askdata["content"] = str(self.room.orders[0][0])
            sendmsgtogether(self.room.user_list, self.server, askdata)


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
                askdata["room"] = str(self.room.room_id)
                askdata["content"] = str(self.room.orders[0][0])
                sendmsgtogether(self.room.user_list, self.server, askdata)
            else:
                if self.room.selectround == 1:
                    self.room.selectround += 1
                    self.room.paircards = self.room.generateFourPairs()
                    pairdata["room"] = str(self.room.room_id)
                    pairdata["content"] = ""
                    for c in self.room.paircards:
                        pairdata["content"] += '{} {} '.format(c[0], c[1])
                    pairdata["content"] = pairdata["content"][:-1]
                    sendmsgtogether(self.room.user_list, self.server, pairdata)

                    self.room.state = WaitScoreState(self.room, self.server)
                else:
                    card = self.room.drawCard()
                    carddata["room"] = str(self.room.room_id)
                    carddata["player"] = "1"
                    carddata["content"] = str(card)
                    sendmsgtogether(self.room.user_list, self.server, carddata)
                    self.room.state = WaitCardState(self.room, self.server)


class WaitCardState(State):
    def __str__(self):
        return "----- Wait Card Play State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        self.room.playCard(int(reply["content"]))
        result = self.room.checkAll(int(reply["content"]))
        specialoperationflag = False
        specialopedata["room"] = str(self.room.room_id)

        for i in range(0, 4):
            if result[i][0] == 0:
                specialopedata["chi1"] = None
                specialopedata["chi2"] = None
                specialopedata["chi3"] = None
            else:
                if result[i][1][0] is None:
                    specialopedata["chi1"] = None
                else:
                    specialopedata["chi1"] = '{} {} {}'.format(result[i][1][0][0], result[i][1][0][1],
                                                               result[i][1][0][2])
                if result[i][1][1] is None:
                    specialopedata["chi2"] = None
                else:
                    specialopedata["chi2"] = '{} {} {}'.format(result[i][1][1][0], result[i][1][1][1],
                                                               result[i][1][1][2])
                if result[i][1][2] is None:
                    specialopedata["chi3"] = None
                else:
                    specialopedata["chi3"] = '{} {} {}'.format(result[i][1][2][0], result[i][1][2][1],
                                                               result[i][1][2][2])
            if result[i][2] == 1:
                specialopedata["peng"] = '{} {} {}'.format(result[i][3][0], result[i][3][1], result[i][3][2])
            if result[i][4] == 1:
                specialopedata["gang"] = '{} {} {} {}'.format(result[i][5][0], result[i][5][1], result[i][5][2],
                                                              result[i][5][3])
            if result[i][6] == 1:
                specialopedata["hu"] = "1"
            self.server.send(self.room.user_list[i].socket_id, specialopedata)

        if specialoperationflag:
            self.room.state = WaitSpecailReplyState(self.room, self.server)
        else:
            card = self.room.drawCard()
            carddata["room"] = str(self.room.room_id)
            carddata["player"] = str(self.room.getCurrentPlayer())
            carddata["content"] = str(card)
            sendmsgtogether(self.room.user_list, self.server, carddata)
            for i in range(1, 5):
                if self.room.checkHu(i):
                    hurequest["room"] = str(self.room.room_id)
                    hurequest["room_id"] = str(self.room.getCurrentPlayer())
                    self.server.send(self.room.user_list[i].socket_id, hurequest)
                    self.room.state = WaitZimoState(self.room, self.server)
                else:
                    self.room.state = WaitCardState(self.room, self.server)


class WaitSpecailReplyState(State):
    def __str__(self):
        return "----- Wait Special Operation Replies State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        self.room.replies.append(reply)
        if len(self.room.replies) == 4:
            for r in self.room.replies:

                pass

class WaitZimoState(State):
    def __str__(self):
        return "----- Wait Zimo Reply State -----"

    def __init__(self, room, server):
        super().__init__(room, server)

    def ChangeToNextState(self, reply):
        if reply["hu"] is None:
            card = self.room.drawCard()
            carddata["room"] = str(self.room.room_id)
            carddata["player"] = str(self.room.getCurrentPlayer())
            carddata["content"] = str(card)
            sendmsgtogether(self.room.user_list, self.server, carddata)
            self.room.state = WaitCardState(self.room, self.server)
        else:
            self.room.Hu(reply["room_id"])
            card = self.room.drawCard()
            carddata["room"] = str(self.room.room_id)
            carddata["player"] = reply["room_id"]
            carddata["content"] = str(card)
            sendmsgtogether(self.room.user_list, self.server, carddata)
            self.room.state = WaitCardState(self.room, self.server)
