# 状态模式

class State:
    def __str__(self):
        return "This is a Main State Class"

    def __init__(self):
        pass

    def ChangeToNextState(self, game, reply):
        pass

class WaitChoiceState(State):
    pass



class WaitCardState(State):
    def __str__(self):
        return "Waiting for a card from player" + str('''玩家ID''')

    def __init__(self):
        pass

    def ChangeToNextState(self, game, reply):
        # reply = {"type":"playcard", "socket_id":22, "room":8, "room_id":1, "content":[66]}
        result = game.gamecommand.checkAll(reply["content"][0])
        specialoperationflag = False
        requestsend = 0
        for r in result:
            if r is not None:
                specialoperationflag = True
                requestsend += 1
                # Send Msg
        if specialoperationflag == True:
            game.state = WaitSpecailReplyState(requestsend)
        else:
            game.gamecommand.drawCard()
            if game.checkZimo() == True:
                game.state = WaitZimoState()
            else:
                game.state = WaitCardState()

class WaitSpecailReplyState(State):
    def __str__(self):
        return "Waiting for the reply/replies of specail operation"
    
    def __init__(self, send):
        self.needtorecieve = send
        self.replies = []

    def ChangeToNextState(self, game, reply):
        if self.needtorecieve > 1:
            self.replies.append(reply)
            self.needtorecieve
            pass
        else:


class WaitZimoState(State):
    def __str__(self):
        return "Waiting for a reply of Zi Mo"

    def ChangeToNextState(self, game, repliy):
        pass

class WaitReadyState(State):
    def __str__(self):
        return "Waiting for the ready reply"

    def __init__(self):
        self.ready = 0

    def ChangeToNextState(self, game, reply):
        if reply["type"] == "joinroom":
            
        if game.
