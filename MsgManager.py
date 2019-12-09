class RcvMsg:
    def __init__(self, msg):
        self.msg = msg.decode('utf-8')
    
    def Analyse(self):
        contents = self.msg.spilt()
        if len(contents) == 2:
            if contents[1] == 'quitroom':
                pass
        elif len(contents) == 3:
            if contents[1] == 'name':
                pass
            elif contents[1] == 'create':
                pass
            elif contents[1] == 'joinroom':
                pass
            elif contents[1] == 'ready':
                pass
        
            elif contents[2] == 'yes':
                pass
            elif contents[2] == 'no':
                pass
        elif len(contents) == 4:
            if contents[2] == 'score':
                pass
            elif contents[2] == 'choose':
                pass
            elif contents[2] == 'playcard':
                pass
        
class SendMsg:
    def sendmsg(self, Msg, client_id):
        self.Msg.encode('utf-8')
        # server.send(Msg, client_id)
    
    def sendSendReadyMsg(self, ready_roomplayer_id):
        pass

    def sendChiMsg(self, room_id, roomplayer_id, chicard_id, client_id):
        msg = '{0} {1} chi {2} {3} {4}'.format(room_id, roomplayer_id, chicard_id[0], chicard_id[1], chicard_id[2])
        self.sendmsg(msg, client_id)
    
    def sendPengMsg(self, room_id, roomplayer_id, chicard_id, client_id):
        msg = '{0} {1} peng {2} {3} {4}'.format(room_id, roomplayer_id, chicard_id[0], chicard_id[1], chicard_id[2])
        self.sendmsg(msg, client_id)
    
    def sendGangMsg(self, room_id, roomplayer_id, chicard_id, client_id):
        msg = '{0} {1} gang {2} {3} {4}'.format(room_id, roomplayer_id, chicard_id[0], chicard_id[1], chicard_id[2])
        self.sendmsg(msg, client_id)
    
    def sendHuMsg(self, room_id, roomplayer_id, chicard_id, client_id):
        msg = '{0} {1} hu {2}'.format(room_id, roomplayer_id, chicard_id)
        self.sendmsg(msg, client_id)
