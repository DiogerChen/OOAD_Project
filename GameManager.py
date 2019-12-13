from Server import server
from Logic import *
from GameCommand import *
from GameStates import *
import time

gamestatus = ["beforestart", "", "", ""]


class GameManager():
    def __init__(self):
        self.game = Game()
        self.gamecommand = GameCommand()
        self.state = WaitReadyState()

    def Update(self, state, commands):

        pass

    def Check(self, conditions, commands):
        if conditions == True:
            self.Update(commands)


    def RunTheGame(self):

            specialope = False

            # SendWaitMsg(self.currentPlayer)
            start_time = time.time() # 计时器
            disCard = None # 得到卡片

            '''for player in players:
                if player.checkHu(disCard) is True:
                    SendHuMsg(player)
                    if reply == True: #
                        player.Hu(disCard)
                    self.EndGame(player)
                    return
                
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
                    specialope = True'''
                

            if specialope == False:
                game.nextPlayer()
                game.(player)
            
            self.round += 1

