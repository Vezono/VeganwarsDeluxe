from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import FreeWeaponAction, MeleeAttack
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Claws(MeleeWeapon):
    id = 'claws'
    name = 'Стальные когти'
    description = 'Ближний бой, урон 1-3, точность высокая. Можно выдвинуть когти, повысив урон до 2-5, ' \
                  'но затрачивая 4 энергии за атаку.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.claws = False


@AttachedAction(Claws)
class ClawsAttack(MeleeAttack):
    pass


@AttachedAction(Claws)
class SwitchClaws(FreeWeaponAction):
    id = 'switch_claws'
    target_type = OwnOnly()
    priority = -10

    @property
    def name(self):
        return 'Выдвинуть когти' if not self.weapon.claws else 'Задвинуть когти'

    def func(self, source, target):
        if not self.weapon.claws:
            self.weapon.cubes = 4
            self.weapon.damage_bonus = 1
            self.weapon.energy_cost = 3
            self.weapon.accuracy_bonus = 1
        else:
            self.weapon.cubes = 3
            self.weapon.damage_bonus = 0
            self.weapon.energy_cost = 2
            self.weapon.accuracy_bonus = 2
        self.weapon.claws = not self.weapon.claws
        self.session.say(f"⚙️|{source.name} {'выдвигает' if not self.weapon.claws else 'задвигает'} когти!")
