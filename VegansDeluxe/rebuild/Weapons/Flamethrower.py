from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Flamethrower(RangedWeapon):
    id = 'flamethrower'
    name = ls("weapon_flamethrower_name")
    description = ls("weapon_flamethrower_description")

    energy_cost = 3
    cubes = 2
    accuracy_bonus = 2


@AttachedAction(Flamethrower)
class FlamethrowerAttack(RangedAttack):
    def calculate_damage(self, source, target):
        damage = super().calculate_damage(source, target)
        if damage:
            return 1

    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        aflame = target.get_state('aflame')
        aflame.add_flame(self.session, target, source, 1)
        return damage
