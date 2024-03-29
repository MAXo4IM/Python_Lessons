# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
# И БАЗОВЫЙ КЛАСС MAN(общие характеристики)
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в GTA,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.

class House:

    def __init__(self):
        self.dirty = 0
        self.food = 50
        self.money = 100
        self.cats_food = 30
        self.money_was_earned = 0
        self.food_was_eaten = 0
        self.coats_were_bought = 0

    def __str__(self):
        return 'В доме осталось еды {}, денег осталось {}, грязи в доме {}'.format(
            self.food, self.money, self.dirty)

class Man:
    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.hapiness = 100
        self.house = None

    def __str__(self):
        return 'Я - {}, сытность {}, счастья {}'.format(self.name, self.fullness, self.hapiness)

    def pet_the_cat(self):
        cprint('{} погладил(a) кота'.format(self.name))
        self.hapiness += 5

    def go_into_the_house(self):
        self.fullness -= 10
        cprint('{} заехал(a) в дом'.format(self.name), color='grey')

    def eat(self):
        if self.house.food >= 10:
            cprint('{} покушал(a)'.format(self.name), color='green')
            self.fullness += 10
            self.house.food -= 10
            self.house.food_was_eaten += 10
        else:
            cprint('В доме нет еды', color='grey')

class Husband(Man):

    def __init__(self, name):
        super().__init__(name=name)

    def go_into_the_house(self, house):
        self.house = house
        super().go_into_the_house()

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='magenta')
        self.fullness -= 10
        self.house.money += 150
        self.house.money_was_earned += 150

    def gaming(self):
        cprint('{} весь день играл в GTA'.format(self.name), color='blue')
        self.fullness -= 10
        if self.hapiness > 80:
            pass
        else:
            self.hapiness += 20


    def act(self):
        if self.fullness < 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        if self.house.dirty >= 90:
            self.hapiness -= 10
        else:
            pass
        dice = randint(1, 7)
        if self.fullness <= 10:
            self.eat()
        elif self.house.money <= 300:
            self.work()
        elif self.hapiness < 20:
            self.gaming()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.work()
        elif dice == 3:
            self.pet_the_cat()
        else:
            self.gaming()


class Wife(Man):

    def __init__(self, name):
        super().__init__(name=name)

    def go_into_the_house(self, house):
        self.house = house
        super().go_into_the_house()

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходил(a) в магазин за едой'.format(self.name), color='white')
            self.house.food += 50
            self.house.money -= 50
            self.fullness -= 10
        else:
            cprint('В доме нету денег для еды', color='red')

    def buy_fur_coat(self):
        if self.house.money > 350:
            cprint('{} сходил(a) в магазин за шубой'.format(self.name))
            self.house.money -= 350
            self.fullness -= 10
            self.house.coats_were_bought += 1
            if self.hapiness > 45:
                pass
            else:
                self.hapiness += 60
        else:
            cprint('В доме нету денег для шубы', color='red')
            self.hapiness -= 10

    def clean_house(self):
        cprint('{} сделала уборку в доме'.format(self.name))
        self.fullness -= 10
        self.house.dirty -= 100

    def shopping_for_cat(self):
        if self.house.money >= 25:
            cprint('{} сходил(a) в магазин за едой для кота'.format(self.name))
            self.house.money -= 50
            self.house.cats_food += 50
        else:
            cprint('В досе нету денег для кошачей еды', color='red')

    def talk_to_friends(self):
        cprint('{} разговаривал(a) с друзьями'.format(self.name), color='grey')
        self.fullness -= 10
        if self.hapiness > 90:
            pass
        else:
            self.hapiness += 20

    def act(self):
        if self.fullness < 0:
            cprint('{} умер(ла)...'.format(self.name), color='red')
            return
        if self.house.dirty >= 90:
            self.hapiness -= 10
        else:
            pass
        dice = randint(1, 7)
        if self.fullness <= 10:
            self.eat()
        elif self.house.food <= 30:
            self.shopping()
        elif self.house.cats_food <= 20:
            self.shopping_for_cat()
        elif self.house.dirty >= 100:
            self.clean_house()
        elif self.hapiness < 20:
            self.talk_to_friends()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.buy_fur_coat()
        elif dice == 3:
            self.pet_the_cat()
        else:
            self.talk_to_friends()

class Child(Man):

    def __init__(self, name):
        self.name = name
        self.hapiness = 100
        self.fullness = 30
        self.house = None

    def __str__(self):
        return super().__str__()

    def go_into_the_house(self, house):
        self.house = house
        super().go_into_the_house()

    def eat(self):
        cprint('{} покушал'.format(self.name), color='green')
        self.fullness += 10
        self.house.food_was_eaten += 10

    def sleep(self):
        cprint('{} спал целый день'.format(self.name), color='green')
        self.fullness -= 10

    def act(self):
        if self.fullness < 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness < 30:
            self.eat()
        elif dice == 1:
            self.eat()
        else:
            self.sleep()

class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.house = None

    def __str__(self):
        return 'У {}(a) сытность {}'.format(self.name, self.fullness)

    def go_into_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('Кот {} заехал в дом'.format(self.name), color='grey')

    def eat(self):
        if self.house.cats_food >= 20:
            cprint('Кот {} покушал'.format(self.name), color='green')
            self.fullness += 20
            self.house.cats_food -= 10
            self.house.food_was_eaten += 10
        else:
            cprint('В доме нету еды для кота {}(a)'.format(self.name))

    def sleep(self):
        cprint('Кот {} проспал целый день zzz...'.format(self.name), color='green')
        self.fullness -= 10

    def tear_walls(self):
        cprint('Кот {} драл обои целый день'.format(self.name), color='green')
        self.fullness -= 10
        self.house.dirty += 5

    def act(self):
        if self.fullness < 0:
            cprint('Кот {} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness <= 10:
            self.eat()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.tear_walls()
        else:
            self.sleep()


mark = Husband(name='Mark')
alisa = Wife(name='Alisa')
fred = Child(name='Fred')
felix = Cat(name='Felix')
marcus = Cat(name='Marcus')
grealish = Cat(name='Grealish')


citizens = [
    mark,
    alisa,
    fred,
    felix,
    marcus,
    grealish,
]

our_sweet_house = House()
for citizen in citizens:
    citizen.go_into_the_house(house=our_sweet_house)

for day in range(1, 366):
    cprint('================== День {} =================='.format(day), color='yellow')
    our_sweet_house.dirty += 5
    for citizen in citizens:
        citizen.act()
    for citizen in citizens:
        cprint(citizen, color='cyan')
cprint('За весь год было заработанно {} денег, сьеденно {} единиц еды и купленно {} шуб.'.format(
    our_sweet_house.money_was_earned, our_sweet_house.food_was_eaten, our_sweet_house.coats_were_bought), color='yellow')

# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


# ===== DONE(uper) =====


# TODO после реализации второй части - отдать на проверку учителем две ветки

######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда == 100 ;)


# ===== DONE(uper) =====


# TODO после реализации второй части - отдать на проверку учителем две ветки

######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')

# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

