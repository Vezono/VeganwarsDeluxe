from core.Weapons.Weapon import Weapon


class Pistol(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 1
        self.ranged = True
        self.cubes = 3
        self.accuracybonus = 3
        self.energycost = 3

        self.name = 'Пистолет'
        self.description = 'Дальний бой, урон 1-3, точность наивысшая.'
