from Logic import *
from GameStates import *
import numpy as np

class Room:
    def __init__(self, room_id, server):
        self.room_id = room_id
        self.user_list = [None, None, None, None]
        self.game = None
        self.state = WaitReadyState(self, server)
        self.replies = []
        self.paircards = []
        self.supervisorchoice = {}
        self.orders = []
        self.selectround = 1

    def ChangeToNextState(self, reply):
        self.state.ChangeToNextState(reply)

    def addUser(self, user):
        for i in range(len(self.user_list)):
            if self.user_list[i] is None:
                self.user_list[i] = user
                user.room_id = i + 1
                break

    def removeUser(self, user_room_id):
        self.user_list[user_room_id - 1] = None

    def checkReady(self):
        for u in self.user_list:
            if u is not None and u.isready:
                pass
            else:
                return False
        return True

    def getSock(self, player_id):
        return self.user_list[player_id - 1].socket_id

    def createGame(self):
        colleges = np.random.choice([1, 2, 3, 4, 5, 6], 2, True)
        self.game = Game(colleges[0], colleges[1])
        return colleges

    def setCalculator(self, player_id, college_id, skill_id):
        player = self.game.id_to_player[player_id]
        huCalculator = HuCalculator(None)
        huCalculator.setPlayer(player)
        if college_id == 1:
            huCalculator = ZhiRenCalculator(huCalculator)
        elif college_id == 2:
            huCalculator = ShuRenCalculator(huCalculator)
        elif college_id == 3:
            huCalculator = ZhiChengCalculator(huCalculator)
        elif college_id == 4:
            huCalculator = ShuDeCalculator(huCalculator)
        elif college_id == 5:
            huCalculator = ZhiXinCalculator(huCalculator)
        elif college_id == 6:
            huCalculator = ShuLiCalculator(huCalculator)
        if skill_id == 1:
            huCalculator = OJCalculator(huCalculator)
        elif skill_id == 2:
            huCalculator = TongShiCalculator(huCalculator)
        elif skill_id == 3:
            huCalculator = QiPaiCalculator(huCalculator)
        elif skill_id == 4:
            huCalculator = CPGCalculator(huCalculator)
        huCalculator = SpecialCaseCalcultor(huCalculator)
        player.huCalculator = huCalculator

    def nextPlayer(self):
        print(self.game.current_player)
        print(self.game.remaining_player_list)
        index = self.game.remaining_player_list.index(self.game.current_player)
        if index == len(self.game.remaining_player_list) - 1:
            self.game.current_player = self.game.remaining_player_list[0]
            return self.game.remaining_player_list[0].player_id
        else:
            self.game.current_player = self.game.remaining_player_list[index + 1]
            return self.game.remaining_player_list[index + 1].player_id

    def assignInitCard(self):
        for i in range(9):
            self.game.player1.recieveCard(self.game.popCard())
            self.game.player2.recieveCard(self.game.popCard())
            self.game.player3.recieveCard(self.game.popCard())
            self.game.player4.recieveCard(self.game.popCard())

    def generateFourPairs(self):
        result = [[], [], [], []]
        for r in result:
            r.append(self.game.popCard().card_id)
            r.append(self.game.popCard().card_id)
        return result

    def assignPair(self, player_id, pair):
        player = self.game.id_to_player[player_id]
        card1 = self.game.id_to_card[pair[0]]
        card2 = self.game.id_to_card[pair[1]]
        player.recieveCard(card1)
        player.recieveCard(card2)

    def getHand(self, player_id):
        player = self.game.id_to_player[player_id]
        result = []
        for card in player.hand:
            result.append(card.card_id)
        return result

    def drawCard(self):
        card = self.game.popCard()
        self.game.current_player.recieveCard(card)
        return card

    def playCard(self, card_id):
        card = self.game.id_to_card[card_id]
        self.game.current_player.playCard(card)
        self.nextPlayer()

    def playRandomCard(self):
        return self.game.current_player.discardRandomCard().card_id

    def getRemainingPlayers(self):
        result = []
        for player in self.game.original_player_list:
            result.append(player.player_id)
        return result

    def getOriginalPlayers(self):
        result = []
        for player in self.game.original_player_list:
            result.append(player.player_id)
        return result

    def checkChi(self, player_id, card_id):
        player = self.game.id_to_player[player_id]
        card = self.game.id_to_card[card_id]
        chiable, choices = player.checkChi(card)
        result = []
        for choice in choices:
            if choice is not None:
                temp = []
                for card in choice:
                    temp.append(card.card_id)
                result.append(temp)
            else:
                result.append(None)
        return chiable, result

    def Chi(self, player_id, choice_num, discard_id):
        player = self.game.id_to_player[player_id]
        discard = self.game.id_to_card[discard_id]
        player.Chi(choice_num, discard)
        self.game.current_player = player

    def checkPeng(self, player_id, card_id):
        player = self.game.id_to_player[player_id]
        card = self.game.id_to_card[card_id]
        penable, first_two_same = player.checkPeng(card)
        result = []
        for card in first_two_same:
            if card is not None:
                result.append(card.card_id)
        return penable, result

    def Peng(self, player_id, discard_id):
        player = self.game.id_to_player[player_id]
        discard = self.game.id_to_card[discard_id]
        player.Peng(discard)
        self.game.current_player = player

    def checkGang(self, player_id, card_id):
        player = self.game.id_to_player[player_id]
        card = self.game.id_to_card[card_id]
        gangable, first_three_same = player.checkGang(card)
        result = []
        for card in first_three_same:
            if card is not None:
                result.append(card.card_id)
        return gangable, result

    def Gang(self, player_id, discard_id):
        player = self.game.id_to_player[player_id]
        discard = self.game.id_to_card[discard_id]
        player.Gang(discard)
        self.game.current_player = player

    def checkHu(self, player_id):
        player = self.game.id_to_player[player_id]
        huable = player.checkHu()
        return huable

    def earlyHu(self, player):
        if len(self.game.remaining_player_list) == 4:
            player.score += 5000
            player.hu_discription += ' 第一个胡+5000'
        elif len(self.game.remaining_player_list) == 3:
            player.score += 2000
            player.hu_discription += ' 第二个胡+2000'
        elif len(self.game.remaining_player_list) == 2:
            player.score += 1000
            player.hu_discription += ' 第三个胡+1000'
        else:
            player.hu_discription += ' 第四个胡+0'

    def checkWillHu(self, player_id, card_id):
        player = self.game.id_to_player[player_id]
        card = self.game.id_to_card[card_id]
        player.recieveCard(card)
        result = player.checkHu()
        player.hand.remove(card)
        return result

    def Hu(self, player_id):
        # calculate score
        player = self.game.id_to_player[player_id]
        player.huCalculator.calculate()
        self.earlyHu(player)
        if len(self.game.remaining_player_list) > 1:
            self.nextPlayer()
            self.game.remaining_player_list.remove(player)

    def getScore(self, player_id):
        player = self.game.id_to_player[player_id]
        return player.score

    def getHuDiscription(self, player_id):
        player = self.game.id_to_player[player_id]
        return player.hu_discription

    def checkAll(self, card_id):
        # result[0]中依次是player1的：chiable,choices,penable,first_two_same,gangable,first_three_same,huable
        # 如果该player2已经胡了，则result[1]为None
        result = [[], [], [], []]
        card = self.game.id_to_card[card_id]
        for i in range(1, 5):
            temp = []
            player = self.game.id_to_player(i)
            if player in self.game.remaining_player_list:
                chiable, choices = self.checkChi(i, card_id)
                temp.append(chiable)
                temp.append(choices)
                penable, first_two_same = self.checkPeng(i, card_id)
                temp.append(penable)
                temp.append(first_two_same)
                gangable, first_three_same = self.checkGang(i, card_id)
                temp.append(gangable)
                temp.append(first_three_same)
                player.recieveCard(card)
                temp.append(self.checkHu(i))
                player.hand.remove(card)
            else:
                temp = None
            result[i - 1].append(temp)
        return result
