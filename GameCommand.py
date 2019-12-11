from Logic import *


class GameCommand:
    def __init__(self, game):
        self.game = game
        self.id_to_sock = {}

    def bindSock(self, player_id, sock):
        self.id_to_sock[player_id] = sock

    def getSock(self, player_id):
        return self.id_to_sock[player_id]

    def nextPlayer(self):
        index = self.game.remaining_player_list.index(self.game.current_player)
        if index == len(self.game.remaining_player_list) - 1:
            self.game.current_player = self.game.remaining_player_list[0]
            return self.game.remaining_player_list[0].player_id
        else:
            self.game.current_player = self.game.remaining_player_list[index + 1]
            return self.game.remaining_player_list[index + 1].player_id

    def assignInitCard(self):
        for i in range(9):
            self.game.player1.hand.append(self.game.popCard())
            self.game.player2.hand.append(self.game.popCard())
            self.game.player3.hand.append(self.game.popCard())
            self.game.player4.hand.append(self.game.popCard())

    def getHand(self, player_id):
        player = self.game.id_to_player[player_id]
        result = []
        for card in player.hand:
            result.append(card.card_id)
        return result

    def drawCard(self):
        # current_player抽一张卡。每回合结束时，应当先调用nextPlayer()，再drawCard()
        card = self.game.popCard()
        self.game.current_player.recieveCard(card)

    def playCard(self, card_id):
        card = self.game.id_to_card[card_id]
        self.game.current_player.playCard(card)

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
        # 杠与胡都需要暂时把current_player设成上家，以便nextPlayer()可以返还正确的next player
        index = self.game.remaining_player_list.index(player)
        self.game.current_player = self.game.remaining_player_list[index - 1]

    def checkHu(self, player_id):
        player = self.game.id_to_player[player_id]
        return player.checkHu()

    def Hu(self, player_id):
        # calculate score
        player = self.game.id_to_player[player_id]
        if len(self.game.remaining_player_list) > 1:
            index = self.game.remaining_player_list.index(player)
            self.game.current_player = self.game.remaining_player_list[index - 1]
        self.game.remaining_player_list.remove(player)

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
