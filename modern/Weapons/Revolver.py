import random
from core.Weapons.Weapon import Weapon


class Revolver(Weapon):
    id = 6
    name = 'Револьвер'
    description = 'Дальний бой, урон 3-3, точность средняя.'

    def __init__(self, owner):
        super().__init__(owner)
        self.ranged = True
        self.cubes = 3
        self.dmgbonus = 0
        self.energycost = 3
        self.accuracybonus = 2

    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        return damage if not damage else 3