from core.Actions.Action import FreeAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.Weapons.Weapon import Weapon


class Claws(Weapon):
    id = 'claws'
    name = 'Стальные когти'
    description = 'Ближний бой, урон 1-3, точность высокая. Можно выдвинуть когти, повысив урон до 2-5, ' \
                  'но затрачивая 4 энергии за атаку.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0

        self.claws = False


@AttachedAction(Claws)
class SwitchClaws(FreeAction):
    id = 'switch_claws'

    @property
    def name(self):
        return 'Выдвинуть когти' if not self.weapon.claws else 'Задвинуть когти'

    def func(self, source, target):
        if not self.weapon.claws:
            self.weapon.cubes = 4
            self.weapon.dmgbonus = 1
            self.weapon.energycost = 3
            self.weapon.accuracybonus = 1
        else:
            self.weapon.cubes = 3
            self.weapon.dmgbonus = 0
            self.weapon.energycost = 2
        self.weapon.claws = not self.weapon.claws
        self.session.say(f"⚙️|{source.name} {'выдвигает' if not self.weapon.claws else 'задвигает'} когти!")
