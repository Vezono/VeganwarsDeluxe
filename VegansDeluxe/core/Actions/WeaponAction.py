import math
import random

from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.Actions.Action import Action
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Events.DamageEvents import PostAttackGameEvent, AttackGameEvent
from VegansDeluxe.core.Sessions import Session
from VegansDeluxe.core.TargetType import Enemies, Distance
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons import Weapon


class WeaponAction[T: Weapon](Action):
    def __init__(self, session: Session, source: Entity, weapon: T):
        super().__init__(session, source)
        self.weapon: T = weapon


class FreeWeaponAction(WeaponAction):
    @property
    def cost(self):
        return False


class DecisiveWeaponAction(WeaponAction):
    @property
    def cost(self):
        return True


class Attack(DecisiveWeaponAction):
    id = 'attack'
    name = ls("base_attack_name")
    target_type = Enemies()
    priority = 0
    
    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.ATTACK, ActionTag.HARMFUL]

    def func(self, source, target):
        return self.attack(source, target)

    def calculate_damage(self, source: Entity, target: Entity) -> int:
        """
        Calculate the damage based on weapon's damage bonus and accuracy
        """
        if source.energy <= 0:
            return 0
        total_accuracy = source.energy + self.weapon.accuracy_bonus \
                         + target.inbound_accuracy_bonus + source.outbound_accuracy_bonus
        damage = sum(1 for _ in range(self.weapon.cubes) if random.randint(1, 10) <= total_accuracy)
        if total_accuracy > 10:
            damage = int(math.floor(damage * total_accuracy / 10))
        return damage + self.weapon.damage_bonus if damage else 0

    def attack(self, source, target, pay_energy=True):
        """
        Actually performs attack on target, dealing damage.
        """
        damage = self.calculate_damage(source, target)
        if pay_energy:
            source.energy = max(source.energy - self.weapon.energy_cost, 0)

        damage = self.publish_attack_event(source, target, damage)
        self.send_attack_message(source, target, damage)
        damage = self.publish_post_attack_event(source, target, damage)

        target.inbound_dmg.add(source, damage, self.session.turn)
        source.outbound_dmg.add(target, damage, self.session.turn)
        return damage

    def publish_attack_event(self, source, target, damage):
        message = AttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        self.event_manager.publish(message)  # 7.1 Pre-Attack stage
        return message.damage

    def publish_post_attack_event(self, source, target, damage):
        message = PostAttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        self.event_manager.publish(message)  # 7.2 Post-Attack stage
        return message.damage

    def send_attack_message(self, source, target, damage):
        attack_text = ls("base_attack_text_ranged") if self.weapon.ranged else ls("base_attack_text_melee")
        attack_emoji = ls("base_attack_emoji_ranged") if self.weapon.ranged else ls("base_attack_emoji_melee")
        target_name = ls("base_self_target_name") if source == target else target.name
        if damage:
            message = ls("base_attack_message").format(attack_emoji=attack_emoji, source_name=source.name,
                                                 attack_text=attack_text,
                                                 target_name=target_name, weapon_name=self.weapon.name, damage=damage)
        else:
            message = ls("base_miss_message").format(source_name=source.name, attack_text=attack_text,
                                               target_name=target_name,
                                               weapon_name=self.weapon.name)
        self.session.say(message)


class MeleeAttack(Attack):
    target_type = Enemies(distance=Distance.NEARBY_ONLY)


class RangedAttack(MeleeAttack):
    target_type = Enemies(distance=Distance.ANY)
