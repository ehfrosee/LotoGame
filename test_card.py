import pytest
import mock
import random

from loto import LottoCard, Kegs, PlayerHuman, PlayerComputer, Game


@pytest.mark.parametrize('arg', range(5))
def test_create(arg):
    # Проверка корректности создания карточки
    new_card = LottoCard()
    eq = set()
    total_len = 0
    for item in new_card.card:
        eq |= set(item)
        total_len += len(item)
    new_card = eq - {0}
    assert len(new_card) == 15, 'Ошибка карточки. Номера'
    assert total_len == 27, 'Ошибка карточки. Размер'


@pytest.fixture
def fix1():
    new_card = LottoCard()
    new_card.card = [[1, 10, 20, 30, 40, 0, 0, 0, 0],
                     [2, 11, 21, 31, 41, 0, 0, 0, 0],
                     [3, 12, 22, 32, 42, 0, 0, 0, 0]]
    return new_card


def test_chek_number(fix1):
    chek_result_1 = fix1.chek_number(31)
    chek_result_2 = fix1.chek_number(51)
    deleted_number = fix1.card[1][3]
    assert chek_result_1 == True, "проверка наличия номера не работает"
    assert chek_result_2 == False, "проверка наличия номера не работает"
    assert deleted_number == -1, "удаление номера не работает"


@pytest.fixture
def fix2():
    new_card = LottoCard()
    new_card.card = [[1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                     [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                     [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]

    return new_card


@pytest.fixture
def fix3():
    new_card = LottoCard()
    new_card.card = [[-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                     [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                     [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]
    return new_card


def test_closed(fix2, fix3):
    is_closed_1 = fix2.closed()
    is_closed_2 = fix3.closed()
    assert is_closed_1 == False, "проверка пустой карточки не работает"
    assert is_closed_2 == True, "проверка пустой карточки не работает"


@pytest.mark.parametrize('keg_number', range(10, 91, 10))
def test_kegs(keg_number):
    kegs = Kegs(keg_number)
    kegs_test = []
    k = kegs.keg
    while k:
        kegs_test.append(k)
        k = kegs.keg
    assert set(kegs_test) == set(range(1, keg_number + 1))

def test_kegs_eq():
    kegs1 = Kegs()
    kegs2 = Kegs()
    assert kegs1 == kegs2
    k = kegs1.keg
    assert kegs1 != kegs2


@pytest.fixture
def fix4():
    new_card = LottoCard()
    new_card.card = [[4, 14, 0, 0, 41, 0, 61, 73, 0],
                     [11, 0, 0, 0, 0, 55, 65, 74, 86],
                     [0, 0, 0, 36, 0, 59, 70, 76, 89]]
    return new_card


def test_comp_step(fix4):
    player = PlayerComputer()
    player.card = fix4
    assert player.step(11) is 0, 'Error step'
    assert player.step(51) is 0, 'OverTime'


def test_comp_step_last(fix2):
    player = PlayerComputer()
    player.card = fix2
    assert player.step(1) is 1, 'Error step'


@pytest.mark.parametrize('num, name, y, result', (
        [41, 'Человек', 'д', 0], [41, 'Человек', 'н', -1], [51, 'Человек', 'д', -1], [51, 'Человек', 'н', 0]))
def test_human_step(fix4, num, name, y, result):
    with mock.patch('builtins.input', lambda x: name):
        player = PlayerHuman()
        player.card = fix4
    with mock.patch('builtins.input', lambda x: y):
        assert player.step(num) is result, 'Error'


@pytest.mark.parametrize('num, name, y, result', ([1, 'Человек', 'д', 1], [1, 'Человек', 'н', -1]))
def test_human_step_last(fix2, num, name, y, result):
    with mock.patch('builtins.input', lambda x: name):
        player = PlayerHuman()
    player.card = fix2
    with mock.patch('builtins.input', lambda x: y):
        assert player.step(num) is result, 'Error'


@pytest.fixture
def fix5():
    with mock.patch('builtins.input', lambda x: "name"):
        game = Game()

    card_1 = LottoCard()
    card_1.card = [[-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                   [-1, -1, 21, -1, -1, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]
    game.player_1.card = card_1

    card_2 = LottoCard()
    card_2.card = [[-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, 41, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]
    game.player_2.card = card_2
    return game


@pytest.mark.parametrize('num, y, result', ([21, 'н', 1], [41, 'н', 1], [41, 'д', 2]))
def test_game(fix5, num, y, result):
    fix5.kegs.kegs = [num]
    with mock.patch('builtins.input', lambda x: y):
        assert fix5.play_round() is result, 'Error'


@pytest.fixture
def fix6():
    with mock.patch('builtins.input', lambda x: "name"):
        game = Game()

    card_1 = LottoCard()
    card_1.card = [[-1, -1, -1, -1, 41, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]
    game.player_1.card = card_1

    card_2 = LottoCard()
    card_2.card = [[-1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, 41, 0, 0, 0, 0, 0],
                   [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0]]
    game.player_2.card = card_2
    return game


@pytest.mark.parametrize('num, y, result', ([21, 'н', 0], [41, 'н', 1], [41, 'д', 3]))
def test_game_draw(fix6, num, y, result):
    fix6.kegs.kegs = [num]
    with mock.patch('builtins.input', lambda x: y):
        assert fix6.play_round() is result, 'Error'


@pytest.fixture
def fix7():
    new_card = LottoCard()
    new_card.card = [[4, 14, 0, 0, 41, 0, 61, 73, 0],
                     [11, 0, 0, 0, 0, 55, 65, 74, 86],
                     [0, 0, 0, 36, 0, 59, 70, 76, 89]]
    return new_card


@pytest.fixture
def fix8():
    new_card = LottoCard()
    new_card.card = [[4, 14, 0, 0, 41, 0, 61, 73, 0],
                     [11, 0, 0, 0, 0, 55, 65, 74, 86],
                     [0, 0, 0, 36, 0, 59, 70, 76, 89]]
    return new_card


def test_len(fix2):
    assert len(fix2) == 1, 'Ошибка длины'


def test_card_eq(fix7, fix8):
    assert fix7 == fix8, 'Ошибка сравнения'


def test_card_eq2(fix2, fix8):
    assert fix2 != fix8, 'Ошибка сравнения'

def test_card_gt(fix2, fix8):
    assert fix2 > fix8, 'Ошибка сравнения'

def test_card_lt(fix2, fix8):
    assert fix8 < fix2, 'Ошибка сравнения'
