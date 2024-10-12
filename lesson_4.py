from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__max_health = health
        self.__damage = damage

    @property
    def max_health(self):
        return self.__max_health


    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.stunned = False

    def choose_defence(self, heroes_list):
        random_hero = choice(heroes_list)
        self.__defence = random_hero.ability

    def attack(self, heroes_list):
        if not self.stunned:
            for hero in heroes_list:
                if hero.health > 0:
                    if type(hero) == Berserk and self.__defence != hero.ability:
                        hero.blocked_damage = choice([5, 10])
                        hero.health -= (self.damage - hero.blocked_damage)
                    else:
                        hero.health -= self.damage
        else:
            print(f"Босс оглушен и пропускает ход.")
            self.stunned = False

    @property
    def defence(self):
        return self.__defence

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def apply_super_power(self, boss, heroes_list):
        pass

    def attack(self, boss):
        boss.health -= self.damage


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes_list):
        coeff = randint(25, 40,)
        boss.health -= coeff * self.damage
        print(f'Warrior {self.name} hits critically {coeff * self.damage}.')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')
        # self.__buff_amount = 20

    def apply_super_power(self, boss, heroes_list):
        plus_damage = randint(0, 15)
        for hero in heroes_list:
            if hero.health > 0 and type(hero) != Witcher:
                hero.damage += plus_damage
        print(f"Маг {self.name} усиленные герои атакуют {plus_damage}.")


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE')
        self.__blocked_damage = 0

    def apply_super_power(self, boss, heroes_list):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} damages to boss.')

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes_list):
        for hero in heroes_list:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points

class Witcher(Hero):
    def __init__(self, name, health):
       super().__init__(name, health, 0, 'REVIVE')

    def apply_super_power(self, boss, heroes_list):
        for hero in heroes_list:
            if hero.health == 0 and self.health > 0:
                hero.health = self.health
                self.health = 0
                print(f'{self.name} воскресил  {hero.name} отдав ему собственную жизнь ({hero.health}hp).')

class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STEAL_HEALTH')

    def apply_super_power(self, boss, heroes_list):
        if round_number % 2 == 1:
            hp_amount = randint(1, 1000)
            chosen_hero = choice(heroes_list)
            boss.health -= hp_amount
            chosen_hero.health += hp_amount
            print(f'{self.name} украл {hp_amount}хп у Босса и отдал {chosen_hero.name}')

class Reaper(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REAPER')

    def apply_super_power(self, boss, heroes):
        if self.health < self.max_health // 100 * 30:
            self.damage = self.damage * 2
            print(f'урон увеличен')
        if self.health < self.max_health // 100 * 15:
            self.damage = self.damage * 3
            print(f'урон увеличен')

import random

class Thor(Hero):
    def __init__(self, name, health, damage,):
        super().__init__(name,health,damage,'Stuns')

    def apply_super_power(self, boss, heroes):
        if random.random() < 0.3:
            boss.stunned = True
            print(f"Тор оглушил босса!")

class Bomber(Hero):
    boom = True
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'EXPLOSIVE')

    def apply_super_power(self, boss, heroes):
        if self.health == 0:
            boss.health -= 1000000000
            print('BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM')
round_number = 0


def is_game_over(boss, heroes_list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes_list:
        if hero.health > 0:
            all_heroes_dead = False
            break

    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False



def show_statistics(boss, heroes_list):
    print(f' ------------- ROUND {round_number} -------------')
    print(boss)
    for hero in heroes_list:
        print(hero)


def play_round(boss, heroes_list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes_list)
    boss.attack(heroes_list)
    for hero in heroes_list:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes_list)
        elif (type(hero) == Bomber and hero.health == 0 and boss.health > 0 and
              hero.ability != boss.defence and Bomber.boom == True):
            Bomber.boom = False
            hero.apply_super_power(boss, heroes_list)
    show_statistics(boss, heroes_list)

    for hero in heroes_list:
        if isinstance(hero, Thor) and hero.health > 0:
            hero.attack(boss)


def start_game():
    boss = Boss(name='MAHORAGA', health=1000000, damage=300)
    warrior_1 = Warrior(name='Rengoku', health=2000, damage=270)
    warrior_2 = Warrior(name='Benimaru', health=1800, damage=230)
    magic = Magic(name='Gojo', health=2000, damage=300)
    berserk = Berserk(name='Guts', health=1300, damage=220)
    doc = Medic(name='Doc', health=1000, damage=40, heal_points=30)
    assistant = Medic(name='Locha', health=800, damage=35, heal_points=20)
    hac = Hacker(name='Silver Wolf', health=1200, damage=100)
    wit = Witcher(name='Julius', health=4000)
    thor =Thor(name='Tor', health=1000, damage=100)
    reaper = Reaper(name='Kill', health=1000, damage=100)
    bomber = Bomber(name='Deidara', health=1000, damage=100)

    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, hac,wit,thor,reaper,bomber]
    show_statistics(boss, heroes_list)

    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)
        magic.apply_super_power(boss, heroes_list)

start_game()