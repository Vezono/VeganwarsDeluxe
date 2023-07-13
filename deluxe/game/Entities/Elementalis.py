import random

import rebuild
from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.TargetType import OwnOnly
from .Dummy import Dummy


class Elemental(Dummy):
    def __init__(self, session_id: str, name='Веган Елементаль|🌪'):
        super().__init__(session_id, name=name)

        self.hp = 9
        self.max_hp = 9
        self.energy = 7
        self.max_energy = 7

        self.items = [item() for item in rebuild.all_items]
        self.skills.extend([skill() for skill in rebuild.all_skills])

        self.team = 'elemental'

    def choose_act(self, session):
        super().choose_act(session)
        self.weapon = random.choice(rebuild.all_weapons)()
        action_manager.update_entity_actions(session, self)

        cost = False
        while not cost:
            if self.energy <= 0:
                action = action_manager.get_action(session, self, "reload")
            else:
                action = random.choice(action_manager.get_available_actions(session, self))
            action.target = random.choice(action.targets)
            action_manager.queue_action(session, self, action.id)
            cost = action.cost


@AttachedAction(Elemental)
class WarpReality(DecisiveAction):
    id = 'warp_reality'
    name = 'Искривить пространство'
    target_type = OwnOnly()

    def func(self, source, target):
        self.source.inbound_accuracy_bonus = -5
        self.session.say(f'🌌|{source.name} искривляет пространство.')


@AttachedAction(Elemental)
class Singularity(DecisiveAction):
    id = 'reload'
    name = 'Перезагрузить сингулярность'
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(f'⚫️|{source.name} перезагружает сингулярность. Енергия восстановлена ({source.max_energy})!')
        source.energy = source.max_energy
