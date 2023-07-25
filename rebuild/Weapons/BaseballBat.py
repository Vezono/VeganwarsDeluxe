from core.Actions.ActionManager import action_manager
from core.Actions.WeaponAction import MeleeAttack
import random

from core.Weapons.Weapon import MeleeWeapon


class BaseballBat(MeleeWeapon):
    id = 'baseball_bat'
    name = 'Бита'
    description = 'Ближний бой, урон 1-3, точность высокая. Имеет шанс оглушить цель.'

    accuracy_bonus = 2
    cubes = 3


@action_manager.register_action(BaseballBat)
class BaseballBatAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 30:
            return
        stun = target.get_skill('stun')
        self.session.say(f'🌀|{target.name} оглушен!')
        stun.stun += 2
        return damage
