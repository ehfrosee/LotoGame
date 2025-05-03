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

    def __init__(self, player_name="Игрок"):
        self.player_name = player_name
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

    def __str__(self):
        # def print_card(self, player_name="Игрок"):
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

        title = f'\nКарточка игрока: {self.player_name}'
        line_1 = f'{title:^{total_length}}'
        line_2 = '-' * (total_length + 2)
        lines = ['| ' + ' '.join([num_str(num) for num in card_line]) + ' |' for card_line in self.card]
        lines.insert(0, line_2)
        lines.insert(0, line_1)
        lines.append(line_2)
        card_string = '\n'.join(lines)
        return card_string
        # for line in lines:
        #     print(line)

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

    def __len__(self):
        nums = {num for row in self.card for num in row} - {0, -1}
        return len(nums)

    def __eq__(self, other):
        if isinstance(other, LottoCard):
            return len(self) == len(other)
        return False

    def __gt__(self, other):
        if isinstance(other, LottoCard):
            return len(self) < len(other)
        return False

    def __lt__(self, other):
        if isinstance(other, LottoCard):
            return len(self) > len(other)
        return False


class Kegs:
    """
    Класс бочонки
    """

    def __init__(self, max_number=90):
        self.kegs = list(range(1, max_number + 1))
        random.shuffle(self.kegs)
        self._keg = 0

    def __str__(self):
        keg = self._keg if self._keg > 0 else "нет"
        return f'\nНовый бочонок: {keg} (осталось {len(self.kegs)})'

    def __eq__(self, other):
        return set(self.kegs) == set(other.kegs)

    @property
    def keg(self):
        try:
            random.shuffle(self.kegs)
            keg = self.kegs.pop()
            self._keg = keg
        except:
            keg = 0
            self._keg = keg
        print(self)
        return keg


class Player:
    """
    Класс игрок
    """

    def __init__(self, name='Игрок'):
        self.card = LottoCard(name)
        self.player_name = name

    def __str__(self):
        return self.player_name

    def __eq__(self, other):
        return str(self) == str(other)

    def step(self, number):
        print(self.card)
        # self.card.print_card(self.player_name)
        return self.card.chek_number(number)


class PlayerComputer(Player):
    __count = 1

    def __init__(self):
        super().__init__(name=f'Компьютер №{PlayerComputer.__count}')
        PlayerComputer.__count += 1

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

    def __str__(self):
        if self.player_1.card > self.player_2.card:
            report = f"\nИгрок {self.player_1} ведёт\n"
        if self.player_1.card < self.player_2.card:
            report = f"\nИгрок {self.player_2} ведёт\n"
        if self.player_1.card == self.player_2.card:
            report = f"\nИгроки идут ровно\n"
        return report

    def play_round(self):
        keg = self.kegs.keg
        score_1 = self.player_1.step(keg)
        score_2 = self.player_2.step(keg)
        if score_1 == 0 and score_2 == 0:
            print(self)
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
