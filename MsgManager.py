import json

class RcvMsg:
    def __init__(self, msg):
        self.msg = json.loads(msg.decode('utf-8'))
    
    def Analyse(self):
        
        
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
