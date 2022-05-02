# ЗАДАЧКА ЛАБИРИНТ
"""Задача 3 (сложная, можно с ООП)

Помогаем Шарику найти косточку.
Вам нужно написать код, который будет проверять правильно ли Шарик идет по
лабиринту.
То есть, вам нужно придумать реализацию системы управления и проверки решений.
Управление: Вверх, вниз, влево, вправо через инпут или при нажатии клавиши, как
хотите.
Условия:
Если игрок выбрал оптимальное направление - выводим в консоль, что Шарик нашел
правильный пути и даем следующий ход.
Если Шарик пошел в сторону стены - пишем, что шарик ударился о стену, игра
закончена.
Если Шарик вернулся туда откуда пришел на предыдущем ходу - выводим шарик
струсил и убежал, игра закончена.
Если Шарик выбрал не оптимальный проход - выводим шарик заблудился, тоже
заканчиваем игру.
Если Шарик прошел через все оптимальные ходы - поздравляем с победой, завершаем
игру.
Использовать ООП или нет - по вашему усмотрению.
Задание с плюсиком:
Реализовать систему сохранений в JSON. При проигрыше предлагаем сохраниться,
прогресс шарика сохраняется на той позиции с которой он сделал неправильный ход.
При запуске новой игры происходит проверка на наличие сохранения. Если есть
сохранение - предлагаем игроку загрузить его. При отказе удаляем сохранение и
начинаем новую игру с нуля."""

import json
import os.path


class Labyrinth:
    victorious_path = ['r', 'd', 'l', 'd', 'r', 'r', 'r', 'd', 'd', 'r', 'r',
                       'd', 'l', 'd', 'd', 'l', 'd', 'r', 'd', 'r']
    player_path = []

    @classmethod
    def new_step(cls, step):
        cls.player_path.append(step)

    @classmethod
    def load_progress(cls, load_file):
        cls.player_path = load_file


class Player:
    def __init__(self):
        self.last_direction = None
        self.reverse_way = None

    def reverse_move(self):
        if self.last_direction == 'r':
            self.reverse_way = 'l'
        elif self.last_direction == 'l':
            self.reverse_way = 'r'
        elif self.last_direction == 'u':
            self.reverse_way = 'd'
        else:
            self.reverse_way = 'u'

    def move(self, way):
        self.reverse_move()
        if self.reverse_way == way:
            print('Шарик струсил и убежал')
        self.last_direction = way
        Labyrinth.new_step(way)


class Game:
    print('Помоги Шарику найти косточку')
    progress = 'homework.json'
    n = None
    step = None

    @classmethod
    def play(cls):
        cls.set_n()
        cls.step = input('Сделайте ход (up, down, left, right): ')
        sharik.move(cls.step)
        for i in Labyrinth.victorious_path[cls.n:-1]:
            if i == cls.step:
                cls.step = input('Сделайте следующий ход (up, down, left, '
                                 'right): ')
                sharik.move(cls.step)
            elif cls.step == sharik.reverse_way:
                cls.save_progress()
                break
            else:
                print('Шарик ударился в стену.')
                cls.save_progress()
                break
        else:
            if cls.step == 'r':
                print('Поздравляю с победой')
            else:
                print('Проигрыш')

    @classmethod
    def set_n(cls):
        cls.n = len(Labyrinth.player_path)

    @classmethod
    def save_progress(cls):
        save = input('Хотите сохраниться? Y - да, N - нет ')
        if save == 'Y':
            with open(cls.progress, 'w') as f:
                json.dump(Labyrinth.player_path[:-1], f, indent=2)
        else:
            print('Прогресс не был сохранен')

    @classmethod
    def load_progress(cls):
        if os.path.exists(cls.progress) is True:
            load = input('У вас есть сохранение. Хотите его загрузить? Y - да, '
                         'N - нет ')
            if load == 'Y':
                with open(cls.progress) as f:
                    load_file = json.load(f)
                    Labyrinth.load_progress(load_file)
                    cls.play()
            else:
                try:
                    os.remove(cls.progress)
                    cls.play()
                except:
                    cls.play()
        else:
            cls.play()


if __name__ == "__main__":
    sharik = Player()
    Game.load_progress()
