"""Создайте собственную программу «Адресная книга», работающую из командной 
строки и позволяющую просматривать, добавлять, изменять, удалять или искать
контактные данные ваших знакомых. Кроме того, эта информация также должна
сохраняться
на диске для последующего доступа.
Создайте класс для хранения персональных данных. Объекты визитных карточек
храните
в словаре, в котором имена контактов будут служить ключами. Для длительного
хранения
этих объектов на жёстком диске воспользуйтесь модулем pickle. Для добавления,
изменения или удаления контактов применяйте встроенные методы словаря."""

import shelve


class AdressBook:
    """Класс для хранения персональных данных"""
    id = 1
    userid = f'id{id}'
    contacts = {}
    users = {}

    def __init__(self, name, age, number):
        """Добавляет новый контакт в адресную книгу"""
        self.name = name
        self.age = age
        self.number = number
        self.id = AdressBook.id

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_number(self, number):
        self.number = number

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_number(self):
        return self.number

    def get_id(self):
        return self.id

    @classmethod
    def all_cotacts(cls):
        count = 1
        for contact in cls.contacts:
            print(f'{count}. Имя контакта: {cls.contacts[contact].get_name()}, '
                  f'Возраст: {cls.contacts[contact].get_age()}, '
                  f'Номер: {cls.contacts[contact].get_number()}, '
                  f'ID: {cls.contacts[contact].get_id()}')
            count += 1

    @classmethod
    def add_contact(cls):
        name = input('Введите имя контакта: ')
        age = input('Введите возраст: ')
        number = input('Введите номер: ')
        print('Контакт создан и добавлен в адресную книгу \n')
        cls.contacts[f'id{cls.id}'] = AdressBook(name, age, number)
        cls.id += 1

    def change_contact(self):
        print('Что в контакте вы хотите изменить?\n')
        change = int(input('Изменить Имя контакта - 1\n'
                           'Изменить возраст контакта - 2\n'
                           'Изменить номер - 3\n'))
        if change == 1:
            new_name = input('Введите новое Имя контакта: ')
            self.set_name(new_name)
            print(f'Новое Имя контакта {new_name}\n')
            return AdressBook.control()
        elif change == 2:
            new_age = input("Введите возраст: ")
            self.set_age(new_age)
            print(f'Возраст контакта изменён на {new_age}\n')
            return AdressBook.control()
        elif change == 3:
            new_number = input('Введите новый номер: ')
            self.set_number(new_number)
            print(f'Номер контакта изменён {new_number}\n')
            return AdressBook.control()

    def __del__(self):
        pass

    @classmethod
    def control(cls):
        while True:
            print("Просмотреть всю информацию в адресной книге - 1")
            print("Добавить новый контакт - 2")
            print("Изменить контакт - 3")
            print("Удалить контакт - 4")
            print("Сохранить адресную книгу - 5")
            print("Завершить работу программы - 6\n")
            action = int(input("Что вы хотите сделать? "))
            if action == 1:
                cls.all_cotacts()

            elif action == 2:
                cls.add_contact()

            elif action == 3:
                value = str.lower(input('Какой контакт вы хотите изменить?'
                                        ' Введите ID контакта: '))
                if value in cls.contacts:
                    cls.contacts[value].change_contact()
                else:
                    print('Введен несуществующий ID')
                    return cls.control()

            elif action == 4:
                del_contact = str.lower(input('Какой контакт вы хотите удалить?'
                                              ' Введите ID контакта: '))
                if del_contact in cls.contacts:
                    del cls.contacts[del_contact]
                    print(f'Контакт {del_contact} удален.')
                else:
                    print('Введен несуществующий ID')
                    return cls.control()

            elif action == 5:
                AdressBook.save_adressbook()
            else:
                break

    @staticmethod
    def save_adressbook():
        with open('adressbookbase.json', 'w') as adressbook_file:
            json.dump(AdressBook.contacts, adressbook_file, indent=2)
        print('Сохранено')


if __name__ == "__main__":
    AdressBook.control()
