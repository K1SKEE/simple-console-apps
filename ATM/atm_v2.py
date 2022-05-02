"""банкомат

депозит
снимать
баланс
пин-код
залогиниться

админка
количество доступной налички в банкомате
админ может пополнять банкомат наличкой
реализовать авторизованного пользователя в отдельном классе"""
import json
import random
import sys


class ATM:
    """ATM"""
    __ATM_BALANCE = 0

    def __init__(self):
        self._data = Data()
        self.menu_action = {
            '1': lambda: self.open_account(),
            '2': lambda: self.login(),
            '3': lambda: self.login_admin()
        }

    def menu(self):
        """Menu"""
        print('Рускій воєнний карабль\n'
              'ІДІ НАХУЙ')
        while True:
            print('1 - Открыть счет\n'
                  '2 - Вставить карту\n'
                  '3 - Войти как админ\n')
            operation = input()
            self.menu_action[operation]()

    def open_account(self):
        """Create account"""
        random_card = [str(random.randint(0, 9)) for num in range(12)]
        open_card = '4149' + ''.join(random_card)
        last_name = input('Введите свою Фамилию:\n')
        first_name = input('Введите своё Имя:\n')
        self._data.new_user(open_card, last_name, first_name)
        print(f'Добро пожаловать {last_name} {first_name}\n'
              f'Вы открыли счет {open_card}\n'
              f'Ваш Пин-Код "0000", не забудьте изменить его на свой\n')
        menu = input('Продолжить?\n'
                     'Y/N ')
        return sys.exit() if menu == 'N' else self.menu()

    def login(self):
        """Log in"""
        card = input('Вставьте карту: ')
        if card in self._data.get_base():
            pin = input('Введите пин-код: ')
            return LogInMenu(card) if pin == self._data.get_pin(card) \
                else print('Неверный пин-код')
        elif card not in self._data.get_base():
            return print('Невалидная карта')

    def login_admin(self):
        login = input('Введите логин: ')
        if login == self._data.admin_login:
            password = input('Введите код доступа к панели администратора: ')
            return AdminMenu() if password == self._data.admin_password \
                else print('Неверный код доступа')
        else:
            return print('Неверный логин или пароль')

    @property
    def atm_balance(self):
        return self.__ATM_BALANCE

    @atm_balance.setter
    def atm_balance(self, value):
        self.__ATM_BALANCE += value


class LogInMenu(ATM):

    def __init__(self, card):
        super().__init__()
        self.card = card
        self.menu_action = {
            '1': lambda: self.check_balance(),
            '2': lambda: self.deposit(),
            '3': lambda: self.withdraw(),
            '4': lambda: self.change_pin(),
            '5': lambda: atm.menu()
        }
        self.menu()

    def menu(self):
        """Log in menu"""
        print(f'Добро пожаловать {self._data.get_last_name(self.card)} '
              f'{self._data.get_first_name(self.card)}')
        while True:
            print('---------------------------------------------------------\n'
                  'Выберите действие\n'
                  '1 - Проверить баланс\n'
                  '2 - Пополнить баланс\n'
                  '3 - Снять деньги\n'
                  '4 - Изменить ПИН-код\n'
                  '5 - Выйти\n'
                  '---------------------------------------------------------\n')
            operation = input()
            self.menu_action[operation]()

    def check_balance(self):
        print(f'На вашем счету: {self._data.get_balance(self.card)}')

    def withdraw(self):
        available_banknotes = [100, 200, 500, 1000]
        value = int(input(f'Доступные купюры для снятия: '
                          f'{available_banknotes}\n'
                          'Введите сумму снятия: \n'))
        return self._data.set_balance(self.card, value, withdraw=True)

    def deposit(self):
        available_banknotes = [100, 200, 500, 1000]
        value = int(input(f'Банкомат принимает только купюры '
                          f'{available_banknotes}\n'
                          f'Укажите какую сумму хотите внести: '))
        self._data.set_balance(self.card, value)

    def change_pin(self):
        new_pin = input('Введите новый ПИН-код:\n')
        if len(new_pin) == 4:
            self._data.set_pin(self.card, new_pin)
            print(f'Ваш новый пин-код {self._data.get_pin(self.card)}')
        else:
            print('Введён неверный ПИН-код')


class AdminMenu(ATM):

    def __init__(self):
        super().__init__()
        self.menu_action = {
            '1': lambda: self.check_atm_balance(),
            '2': lambda: self.set_atm_balance(),
            '3': lambda: self.view_base(),
            '4': lambda: self.del_user(),
            '5': lambda: atm.menu()
        }
        self.menu()

    def menu(self):
        """Admin Menu"""
        print('Вы вошли как Администратор')
        while True:
            print('---------------------------------------------------------\n'
                  'Выберите действие\n'
                  '1 - Проверить баланс банкомата\n'
                  '2 - Пополнить баланс банкомата\n'
                  '3 - Посмотреть базу\n'
                  '4 - Закрыть счет пользователя\n'
                  '5 - Выйти\n'
                  '---------------------------------------------------------\n')
            operation = input()
            self.menu_action[operation]()

    def check_atm_balance(self):
        print(f'Доступной налички в банкомате: {self.atm_balance}')

    def set_atm_balance(self):
        value = int(input())
        self.atm_balance += value

    def view_base(self):
        count = 0
        for i in self._data.get_base():
            count += 1
            print(f'{count}. Card: {i}, {self._data.get_base(i)}')

    def del_user(self):
        card = input('Введите карту пользователя которого хотите удалить: ')
        if card in self._data.get_base():
            self._data.del_user(card)
            print(f'Счёт {card} удален')
        else:
            print(f'{card} счёт не удалось найти')


class Data:
    JSON_DATA = r'atm.json'
    __admin_login = 'root'
    __admin_password = 'pass'

    def __init__(self):
        with open(self.JSON_DATA) as base:
            self._data_base = json.load(base)
        # try:
        #     with open(self.JSON_DATA) as base:
        #         self._data_base = json.load(base)
        # except FileNotFoundError:
        #     pass

    def new_user(self, card, last_name, first_name):
        self._data_base[card] = {'pin': '0000',
                                 'balance': 0,
                                 'last_name': last_name,
                                 'first_name': first_name}
        self.update_data()

    def update_data(self):
        with open(self.JSON_DATA, 'w') as base:
            json.dump(self._data_base, base, indent=2)

    def get_base(self, card=None):
        if card:
            return self._data_base[card]
        return self._data_base

    def get_pin(self, card):
        return self._data_base[card].get('pin')

    def get_last_name(self, card):
        return self._data_base[card].get('last_name')

    def get_first_name(self, card):
        return self._data_base[card].get('first_name')

    def get_balance(self, card):
        return self._data_base[card].get('balance')

    def set_balance(self, card, value, withdraw=None):
        if withdraw:
            if self.get_balance(card) >= value:
                self._data_base[card]['balance'] -= value
            else:
                print('У вас недоступно столько денег')
        else:
            self._data_base[card]['balance'] += value
        return self.update_data()

    def set_pin(self, card, value):
        self._data_base[card]['pin'] = value
        return self.update_data()

    def del_user(self, card):
        del self._data_base[card]
        return self.update_data()

    @property
    def admin_login(self):
        return self.__admin_login

    @property
    def admin_password(self):
        return self.__admin_password

    @admin_password.setter
    def admin_password(self, value):
        __admin_password = value


if __name__ == '__main__':
    atm = ATM()
    atm.menu()
