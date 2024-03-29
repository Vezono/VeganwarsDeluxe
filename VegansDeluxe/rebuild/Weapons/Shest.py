from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Shest(MeleeWeapon):
    id = 'shest'
    name = 'Шест'
    description = 'Ближний бой, урон 1-3. Способность: вы пытаетесь сбить соперника с ног, получая ' \
                  'возможность атаковать даже тех, кто не находится с вами в ближнем бою.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Shest)
class ShestAttack(MeleeAttack):
    pass


@AttachedAction(Shest)
class KnockDown(MeleeAttack):
    id = 'knock_down'
    name = 'Сбить с ног'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Shest):
        super().__init__(session, source, weapon)
        self.weapon: Shest = weapon

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 6
        damage = self.attack(source, target)
        if not damage:
            self.session.say(f'🚷💨|{source.name} не удалось сбить {target.name} с ног!')
            return
        self.session.say(f'🚷|{source.name} сбивает {target.name} с ног! {target.name} теряет равновесие и падает!')
        state = target.get_state('knockdown')
        state.active = True
