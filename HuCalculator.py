from Logic import *


class HuCalculator:
    def __init__(self, calculator):
        self.calculator = calculator
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def calculate(self):
        self.player.score += 10000
        self.player.hu_discription += '胡+10000'


class ZhiRenCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'zhiren':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'zhiren':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 致仁书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 致仁书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 致仁书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 致仁书院+1000'


class ShuRenCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'shuren':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'shuren':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 树仁书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 树仁书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 树仁书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 树仁书院+1000'


class ZhiChengCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'zhicheng':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'zhicheng':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 致诚书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 致诚书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 致诚书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 致诚书院+1000'


class ShuDeCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'shude':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'shude':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 树德书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 树德书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 树德书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 树德书院+1000'


class ZhiXinCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'zhixin':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'zhixin':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 致新书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 致新书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 致新书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 致新书院+1000'


class ShuLiCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'shuli':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'shuli':
                counter += 1
        if counter == 4:
            self.player.score += 8000
            self.player.hu_discription += ' 树礼书院+8000'
        elif counter == 3:
            self.player.score += 5000
            self.player.hu_discription += ' 树礼书院+5000'
        elif counter == 2:
            self.player.score += 2500
            self.player.hu_discription += ' 树礼书院+2500'
        elif counter == 1:
            self.player.score += 1000
            self.player.hu_discription += ' 树礼书院+1000'


class OJCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'zhong' or c.card_type == 'fa' or c.card_type == 'bai':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'zhong' or c.card_type == 'fa' or c.card_type == 'bai':
                counter += 1
        bonus = counter * 800
        self.player.score += bonus
        self.player.hu_discription += ' OJ刷题+'
        self.player.hu_discription += str(bonus)


class TongShiCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        counter = 0
        for c in self.player.expose_area:
            if c.card_type == 'tiao' or c.card_type == 'bin' or c.card_type == 'wan':
                counter += 1
        for c in self.player.hand:
            if c.card_type == 'tiao' or c.card_type == 'bin' or c.card_type == 'wan':
                counter += 1
        bonus = counter * 400
        self.player.score += bonus
        self.player.hu_discription += ' 通识教育+'
        self.player.hu_discription += str(bonus)


class QiPaiCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        bonus = len(self.player.discard_area) * 200
        self.player.score += bonus
        self.player.hu_discription += ' 更多经历+'
        self.player.hu_discription += str(bonus)


class CPGCalculator(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        bonus = len(self.player.expose_area) * 500
        self.player.score += bonus
        self.player.hu_discription += ' 特殊操作+'
        self.player.hu_discription += str(bonus)


class SpecialCaseCalcultor(HuCalculator):
    def __init__(self, calculator):
        super().__init__(calculator)
        self.player = calculator.player

    def calculate(self):
        self.calculator.calculate()
        checkMenQianQing(self.player)
        checkFlush(self.player)
        checkQueSe(self.player)
        checkDuanYao(self.player)
        checkDanDiao(self.player)


def checkMenQianQing(player):
    if len(player.expose_area) == 0:
        player.score += 3000
        player.hu_discription += ' 门前清+3000'


def checkFlush(player):
    exist_tiao = [False, False, False, False, False, False, False, False, False]
    exist_bin = [False, False, False, False, False, False, False, False, False]
    exist_wan = [False, False, False, False, False, False, False, False, False]
    for c in player.hand:
        if c.card_type == 'tiao':
            exist_tiao[c.card_num - 1] = True
        if c.card_type == 'bin':
            exist_bin[c.card_num - 1] = True
        if c.card_type == 'wan':
            exist_wan[c.card_num - 1] = True
    for c in player.expose_area:
        if c.card_type == 'tiao':
            exist_tiao[c.card_num - 1] = True
        if c.card_type == 'bin':
            exist_bin[c.card_num - 1] = True
        if c.card_type == 'wan':
            exist_wan[c.card_num - 1] = True
    tiao_result = True
    for i in exist_tiao:
        if i is False:
            tiao_result = False
            break
    bin_result = True
    for i in exist_bin:
        if i is False:
            bin_result = False
            break
    wan_result = True
    for i in exist_wan:
        if i is False:
            wan_result = False
            break
    if tiao_result or bin_result or wan_result:
        player.score += 5000
        player.hu_discription += ' 一条龙+5000'


def checkQueSe(player):
    tiao_counter = 0
    bin_counter = 0
    wan_counter = 0
    for c in player.hand:
        if c.card_type == 'tiao':
            tiao_counter += 1
        if c.card_type == 'bin':
            bin_counter += 1
        if c.card_type == 'wan':
            wan_counter += 1
    for c in player.expose_area:
        if c.card_type == 'tiao':
            tiao_counter += 1
        if c.card_type == 'bin':
            bin_counter += 1
        if c.card_type == 'wan':
            wan_counter += 1
    total = len(player.hand) + len(player.expose_area)
    if tiao_counter == total or bin_counter == total or wan_counter == total:
        player.score += 6000
        player.hu_discription += ' 清一色+6000'
    elif tiao_counter + bin_counter == total or tiao_counter + wan_counter == total or wan_counter + bin_counter == total:
        player.score += 3000
        player.hu_discription += ' 缺一色+3000'


def checkDuanYao(player):
    result = True
    for c in player.hand:
        if c.card_num == 1 or c.card_num == 9:
            result = False
            break
    for c in player.expose_area:
        if c.card_num == 1 or c.card_num == 9:
            result = False
            break
    if result:
        player.score += 1500
        player.hu_discription += ' 段幺九+1500'


def checkDanDiao(player):
    if len(player.hand) == 2:
        player.score += 1500
        player.hu_discription += ' 单钓+1500'
