import random

from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


class Torch(MeleeWeapon):
    id = 'torch'
    name = 'Факел'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс поджечь цель.'

    def __init__(self):
        super().__init__()
        self.accuracy_bonus = 2
        self.cubes = 3


@AttachedAction(Torch)
class TorchAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 50:
            aflame = target.get_skill('aflame')
            aflame.add_flame(self.session, target, source, 1)
        return damage
