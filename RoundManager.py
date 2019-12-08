from Server import server
from Logic import *
import time

changePlayerDic = {0:1, 1:2, 2:3, 3:0}

class BigRound():
    players = [] # players
    def __init__(self, game):
        self.game = game
        self.round = 0
        self.remaincard = 138   # 需要定义真正的牌数
        self.currentPlayer = 0
        self.ChangeToPlayStatus()

    def Licensing(self, player): # 发牌
        thiscard = game.popCard()
        player.recieveCard(thiscard)
        SendCardMsg(player)
        # 客户端要有对应的GetCard()方法来得到卡牌

    def EndGame(self, player):
        print(player.CalculateFan()) # 计算番数
        SendPlayAgainMsg()

    def RunTheGame(self):
        while True:
            specialope = False

            SendWaitMsg(self.currentPlayer)
            start_time = time.time() # 计时器
            disCard = None # 得到卡片

            for player in players:
                if player.checkChi(disCard) is True:
                    SendChiMsg(player)
                    if reply == True: # 
                        player.Chi(disCard)
                    self.currentPlayer = player
                    specialope = True    
                if player.checkPeng(disCard) is True:
                    SendPengMsg(player)
                    if reply == True: # 
                        player.Peng(disCard)
                    self.currentPlayer = player
                    specialope = True
                
                if player.checkGang(disCard) is True:
                    SendGangMsg(player)
                    if reply == True: # 
                        player.Gang(disCard)
                    self.currentPlayer = player
                    self.Licensing(player) # 杠上
                    specialope = True
                
                if player.checkHu(disCard) is True:
                    SendHuMsg(player)
                    if reply == True: #
                        player.Hu(disCard)
                    self.EndGame(player)
                    return

            if specialope == False:
                self.currentPlayer = changePlayerDic[self.currentPlayer]
                self.Licensing(player)
            
            SendWaitMsg(player)
            self.round += 1


def SendWaitMsg(operation_player_id):
    # 命令其他三个等待，剩下那个可以打牌，开始计时
    pass

def SendChiMsg(operation_player_id):
    # 如果有人可以吃，向他们发送打牌的指令，别人等待，开始计时
    pass
def SendPengMsg(operation_player_id):
    # 如果有人可以碰，向他们发送打牌的指令，别人等待，开始计时
    pass
def SendGangMsg(operation_player_id):
    # 如果有人可以杠，向他们发送打牌的指令，别人等待，开始计时
    pass

def SendHuMsg(operation_player_id):
    # 如果有人可以杠，向他们发送打牌的指令，别人等待，开始计时
    pass

def SendCardMsg(discard, operation_player_id):
    pass

def SendPlayAgainMsg():
    # 询问是否再玩，不玩的话退出游戏
    pass


if __name__ == '__main__':
    game = Game()
    round = BigRound()
    round.RunTheGame()
    # newServer = server.Echo()
