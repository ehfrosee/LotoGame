'''
Игра Лото.
Игроки: Человек - Компьютер, Человек - Человек, Компьютер - Компьютер
'''
import random


class LottoCard:
    """
    Класс карточки лото
    """
    __rows = 3
    __cols = 9
    __num_per_row = 5
    __min_number = 1
    __max_number = 90
    __emptynum = 0
    __crossednum = -1

    def __init__(self):
        self.card = [[None for i in range(self.__cols)] for i in range(self.__rows)]
        self.new_card()

    def new_card(self):
        # Создание новой карточки
        numbers = sorted(random.sample(range(self.__min_number, self.__max_number), self.__rows * self.__cols))
        cards = [numbers[i::self.__rows] for i in range(self.__rows)]
        emptys = [sorted(random.sample(range(self.__cols), self.__cols - self.__num_per_row)) for i in
                  range(self.__rows)]
        for i in range(self.__rows):
            for j in range(self.__cols):
                self.card[i][j] = self.__emptynum if j in emptys[i] else cards[i][j]

    def print_card(self, player_name="Игрок"):
        # Вывод содержимого карточки на экран
        item_length = 4
        total_length = item_length * self.__cols + 1

        def num_str(num):
            if num > self.__emptynum:
                number_string = f"{num:>{2}} "
            elif num == self.__crossednum:
                number_string = "-- "
            else:
                number_string = ' ' * (item_length - 1)
            return number_string

        title = f'Карточка игрока: {player_name}'
        line_1 = f'{title:^{total_length}}'
        line_2 = '-' * (total_length + 2)
        lines = ['| ' + ' '.join([num_str(num) for num in card_line]) + ' |' for card_line in self.card]
        lines.insert(0, line_2)
        lines.insert(0, line_1)
        lines.append(line_2)
        for line in lines:
            print(line)

    def chek_number(self, number):
        # Проверка числа в карточке, вычёркивание его
        for i, row in enumerate(self.card):
            if number in row:
                j = row.index(number)
                self.card[i][j] = self.__crossednum
                return True
        return False


    def closed(self):
        return {set(ci) == {-1, 0} for ci in self.card} == {True}

class Kegs:
    """
    Класс бочонки
    """

    def __init__(self, max_number=90):
        self.__kegs = list(range(1, max_number + 1))
        random.shuffle(self.__kegs)

    def get_keg(self):
        try:
            random.shuffle(self.__kegs)
            keg = self.__kegs.pop()
        except:
            keg = 0
        print(f'\nНовый бочонок: {keg} (осталось {len(self.__kegs)})')
        return keg


class Player:
    """
    Класс игрок
    """

    def __init__(self, name='Игрок'):
        self.card = LottoCard()
        self.player_name = name

    def step(self, number):
        self.card.print_card(self.player_name)
        return self.card.chek_number(number)

class PlayerComputer(Player):

    def __init__(self):
        super().__init__('Компьютер')

    def step(self, number):
        if super().step(number):
            print('Номер есть')
            if self.card.closed():
                return 1
            else:
                return 0
        else:
            print('Номера нет в карточке')
            return 0

class PlayerHuman(Player):

    def __init__(self):
        name = input("Введите имя игрока: ")
        super().__init__(name)

    def step(self, number):
        check = super().step(number)
        ans = input('Зачеркнуть цифру (Д/Н)? ')
        while ans not in 'ДдНн':
            ans = input('Некорректный ввод. Зачеркнуть цифру (Д/Н)? ')

        if check and ans in 'Дд':
            print('Номер есть')
            if self.card.closed():
                return 1
            else:
                return 0
        elif not check and ans in 'Нн':
            print('Номера нет в карточке')
            return 0
        else:
            print('ОШИБКА!')
            return -1


class Game:
    """
    Класс Игра.
    """

    def __init__(self):
        self.kegs = Kegs()
        self.player_1 = PlayerComputer()
        #self.player_2 = PlayerComputer()
        self.player_2 = PlayerHuman()

    def play_round(self):
        keg = self.kegs.get_keg()
        score_1 = self.player_1.step(keg)
        score_2 = self.player_2.step(keg)
        if score_1 == 0 and score_2 == 0:
            return 0
        elif (score_1 == 1 and score_2 == 0) or score_2 == -1:
            return 1
        elif (score_1 == 0 and score_2 == 1) or score_1 == -1:
            return 2
        elif score_1 == 1 and score_2 == 1:
            return 3
        else:
            return -1

if __name__ == '__main__':
    game = Game()
    while True:
        score = game.play_round()
        if score == 1:
            print('Player 1 win')
            break
        elif score == 2:
            print('Player 2 win')
            break
        elif score == 3:
            print('Draw')
            break
        elif score == -1:
            print('The end')
            break

    # card = LottoCard()
    # card.print_card()
    # card.new_card()
    # card.print_card()
    #
    # keg = Kegs()
    # print(keg.get_keg())
