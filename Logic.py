import random

type_hash = {'wan': 0, 'tiao': 1, 'bin': 2, 'dong': 3, 'xi': 4, 'nan': 5, 'bei': 6, 'bai': 7, 'fa': 8, 'zhong': 9}


class Game:
    def __init__(self, room_id, player1_nickname, player2_nickname, player3_nickname, player4_nickname):
        self.room_id = room_id
        self.player1 = Player(player1_nickname, 1)
        self.player2 = Player(player2_nickname, 2)
        self.player3 = Player(player3_nickname, 3)
        self.player4 = Player(player4_nickname, 4)
        self.original_player_list = [self.player1, self.player2, self.player3, self.player4]
        self.remaining_player_list = [self.player1, self.player2, self.player3, self.player4]
        self.deck = None
        self.id_to_card = {}
        self.id_to_player = {1: self.player1, 2: self.player2, 3: self.player3, 4: self.player4}
        self.createNewDeck()
        self.current_player = self.player1

    def nextPlayer(self):
        index = self.remaining_player_list.index(self.current_player)
        if index == len(self.remaining_player_list) - 1:
            return self.remaining_player_list[0]
        else:
            return self.remaining_player_list[index + 1]

    def removePlayer(self, player):
        self.remaining_player_list.remove(player)

    def createNewDeck(self):
        self.deck = []
        shu_pai = ['wan', 'tiao', 'bin']
        zi_pai = ['dong', 'xi', 'nan', 'bei', 'bai', 'fa', 'zhong']
        id_counter = 0
        for t in shu_pai:
            for i in range(1, 10):
                for j in range(4):
                    card = Card(t, i, id_counter)
                    self.deck.append(card)
                    self.id_to_card[id_counter] = card
                    id_counter += 1
        for t in zi_pai:
            for i in range(4):
                card = Card(t, 0, id_counter)
                self.deck.append(card)
                self.id_to_card[id_counter] = card
                id_counter += 1

    def popCard(self):
        if len(self.deck) > 0:
            return self.deck.pop(random.randint(0, len(self.deck) - 1))
        else:
            return None

    def drawCard(self):
        card = self.popCard()
        self.current_player.recieveCard(card)

    def assignInitCard(self):
        for i in range(9):
            self.player1.hand.append(self.popCard())
            self.player2.hand.append(self.popCard())
            self.player3.hand.append(self.popCard())
            self.player4.hand.append(self.popCard())


class Card:
    def __init__(self, card_type, card_num, card_id):
        self.card_type = card_type
        self.card_num = card_num
        # 字牌的card_num均为0
        self.card_id = card_id

    def __lt__(self, other):
        if type_hash[self.card_type] != type_hash[other.card_type]:
            return type_hash[self.card_type] < type_hash[other.card_type]
        else:
            return self.card_num < other.card_num

    def __str__(self):
        return self.card_type + ' ' + str(self.card_num)


class Player:
    def __init__(self, nickname, player_id):
        self.nickname = nickname
        self.player_id = player_id
        self.hand = []
        self.expose_area = []
        self.discard_area = []
        self.score = 0

    def recieveCard(self, received_card):
        self.hand.append(received_card)

    def playCard(self, discard):
        self.hand.remove(discard)
        self.discard_area.append(discard)

    def discardRandomCard(self):
        discard = self.hand.pop(random.randint(0, len(self.hand) - 1))
        self.discard_area.append(discard)
        return discard

    def checkHu(self):
        result = False
        self.hand.sort()
        for c1 in self.hand:
            for c2 in self.hand:
                if c1 == c2:
                    continue
                elif c1.card_type == c2.card_type and c1.card_num == c2.card_num:
                    # print(c1, c2)
                    triple = []
                    result = True
                    for c in self.hand:
                        if c != c1 and c != c2:
                            triple.append(c)
                        if len(triple) == 3:
                            if triple[0].card_type == triple[1].card_type == triple[2].card_type and (
                                    triple[0].card_num == triple[1].card_num == triple[2].card_num
                                    or triple[0].card_num + 2 == triple[1].card_num + 1 == triple[2].card_num):
                                # print(triple[0], triple[1], triple[2], 'triple success')
                                triple = []
                            else:
                                # print(triple[0], triple[1], triple[2], 'triple failed')
                                result = False
                                break
                    if result:
                        return result
        return result

    def Hu(self):
        pass

    def checkChi(self, discard):
        exist_two_less = False
        two_less = None
        exist_one_less = False
        one_less = None
        exist_one_more = False
        one_more = None
        exist_two_more = False
        two_more = None
        chiable = False
        choices = [None, None, None]
        for card in self.hand:
            # print(card.card_num,discard.card_num,card.card_type,discard.card_type)
            if card.card_type == discard.card_type and card.card_num == (discard.card_num - 1):
                exist_one_less = True
                one_less = card
                break
        for card in self.hand:
            # print(card.card_num, discard.card_num, card.card_type, discard.card_type)
            if card.card_type == discard.card_type and card.card_num == (discard.card_num + 1):
                exist_one_more = True
                one_more = card
                break
        for card in self.hand:
            # print(card.card_num, discard.card_num, card.card_type, discard.card_type)
            if card.card_type == discard.card_type and card.card_num == (discard.card_num - 2):
                exist_two_less = True
                two_less = card
                break
        for card in self.hand:
            # print(card.card_num, discard.card_num, card.card_type, discard.card_type)
            if card.card_type == discard.card_type and card.card_num == (discard.card_num + 2):
                exist_two_more = True
                two_more = card
                break
        if exist_two_less and exist_one_less:
            choices[0] = [two_less, one_less, discard]
            chiable = True
        if exist_one_less and exist_one_more:
            choices[1] = [one_less, discard, one_more]
            chiable = True
        if exist_one_more and exist_two_more:
            choices[2] = [discard, one_more, two_more]
            chiable = True
        return chiable, choices

    def Chi(self, choice_num: int, discard):
        chiable, choices = self.checkChi(discard)
        if chiable and 0 <= choice_num <= 2:
            if choice_num == 0:
                self.hand.remove(choices[0][0])
                self.expose_area.append(choices[0][0])
                self.hand.remove(choices[0][1])
                self.expose_area.append(choices[0][1])
                self.expose_area.append(discard)
            elif choice_num == 1:
                self.hand.remove(choices[1][0])
                self.expose_area.append(choices[1][0])
                self.expose_area.append(discard)
                self.hand.remove(choices[1][2])
                self.expose_area.append(choices[1][2])
            elif choice_num == 2:
                self.expose_area.append(discard)
                self.hand.remove(choices[2][1])
                self.expose_area.append(choices[2][1])
                self.hand.remove(choices[2][2])
                self.expose_area.append(choices[2][2])
            return True
        else:
            return False

    def checkPeng(self, discard):
        penable = False
        same_num = 0
        first_two_same = [None, None]
        for card in self.hand:
            # print(card.card_num, discard.card_num, card.card_type, discard.card_type)
            if card.card_type == discard.card_type and card.card_num == discard.card_num:
                first_two_same[same_num] = card
                same_num += 1
            if same_num == 2:
                penable = True
                break
        return penable, first_two_same

    def Peng(self, discard):
        penable, first_two_same = self.checkPeng(discard)
        if penable:
            self.hand.remove(first_two_same[0])
            self.expose_area.append(first_two_same[0])
            self.hand.remove(first_two_same[1])
            self.expose_area.append(first_two_same[1])
            self.expose_area.append(discard)
            return True
        else:
            return False

    def checkGang(self, discard):
        gangable = False
        same_num = 0
        first_three_same = [None, None, None]
        for card in self.hand:
            if card.card_type == discard.card_type and card.card_num == discard.card_num:
                first_three_same[same_num] = card
                same_num += 1
            if same_num == 3:
                gangable = True
                break
        return gangable, first_three_same

    def Gang(self, discard):
        gangable, first_three_same = self.checkPeng(discard)
        if gangable:
            self.hand.remove(first_three_same[0])
            self.expose_area.append(first_three_same[0])
            self.hand.remove(first_three_same[1])
            self.expose_area.append(first_three_same[1])
            self.hand.remove(first_three_same[2])
            self.expose_area.append(first_three_same[2])
            self.expose_area.append(discard)
            return True
        else:
            return False
