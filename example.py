from Logic import *

# 初始化一个游戏并让一个人摸13张牌，并与一张新抽牌一起检验能否吃碰杠
game = Game('a123', 'A', 'B', 'C', 'D')
for i in range(13):
    game.player1.recieveCard(game.popCard())
current_card = game.popCard()
for c in game.player1.hand:
    print(c.card_num, c.card_type)
print()
print(current_card.card_num, current_card.card_type)
print(game.player1.checkPen(current_card)[0])
print(game.player1.checkGang(current_card)[0])
print(game.player1.checkChi(current_card)[0])
