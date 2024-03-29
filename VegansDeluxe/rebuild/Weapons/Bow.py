from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon

@RegisterWeapon
class Bow(RangedWeapon):
    id = 'bow'
    name = 'Лук'
    description = 'Дальний бой, урон 1-3, точность средняя. Способность: поджигает стрелу, которая не ' \
                  'наносит урон, но накладывает на цель 2 эффекта горения.'

    cubes = 3
    accuracy_bonus = 1
    energy_cost = 3
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Bow)
class BowAttack(RangedAttack):
    pass


@AttachedAction(Bow)
class FireArrow(RangedAttack):
    id = 'fire_arrow'
    name = 'Огненная стрела'
    target_type = Enemies()

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energy_cost, 0)
        if not damage:
            self.session.say(f'💨|{source.name} поджигает стрелу и запускает ее в {target.name}, но не попадает.')
            return
        self.session.say(f'☄️|{source.name} поджигает стрелу и запускает ее в {target.name}!')
        aflame = target.get_state('aflame')
        aflame.add_flame(self.session, target, source, 2)
