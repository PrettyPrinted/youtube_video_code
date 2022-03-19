from abc import ABC, abstractmethod

class Enemy(ABC):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def get_health(self):
        pass

class Monster(Enemy):
    def attack(self):
        print('Attacking...')

    def get_health(self):
        print('Health: 100')

monster = Monster()