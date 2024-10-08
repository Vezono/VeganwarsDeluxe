import random

from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon
from VegansDeluxe.rebuild import Aflame


@RegisterWeapon
class Torch(MeleeWeapon):
    id = 'torch'
    name = ls("rebuild.weapon.torch.name")
    description = ls("rebuild.weapon.torch.description")

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.accuracy_bonus = 2
        self.cubes = 3


@AttachedAction(Torch)
class TorchAttack(MeleeAttack):
    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        if not damage:
            return damage
        if random.randint(0, 100) > 50:
            aflame = target.get_state(Aflame)
            aflame.add_flame(self.session, target, source, 1)
        return damage
