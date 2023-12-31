from core.Actions.Action import DecisiveAction
from core.ContentManager import AttachedAction
from core.Actions.EntityActions import SkipActionGameEvent
from core.Entities.Entity import Entity

from core.TargetType import OwnOnly
from rebuild import all_states


class TelegramEntity(Entity):
    def __init__(self, session_id: str, user_name, user_id):
        super().__init__(session_id)
        self.init_states()

        self.id = str(user_id)
        self.name = user_name
        self.npc = False  # to differentiate humans and bots

        self.chose_weapon = False
        self.chose_skills = False
        self.skill_cycle = 0
        self.chose_items = False
        self.ready = False

    @property
    def user_id(self):
        return int(self.id)

    def choose_act(self, session):  # method for AI
        pass

    def init_states(self):
        for state in all_states:
            self.skills.append(state())

    def pre_move(self):
        super().pre_move()
        if not self.dead:
            self.ready = False


@AttachedAction(TelegramEntity)
class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'
    target_type = OwnOnly()

    @property
    def hidden(self) -> bool:
        return self.source.nearby_entities == list(filter(lambda t: t != self.source, self.session.entities))

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(f'👣|{source.name} подходит к противнику вплотную.')


@AttachedAction(TelegramEntity)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'
    target_type = OwnOnly()

    def func(self, source, target):
        source.energy = source.max_energy
        self.session.say(source.weapon.reload_text(source))


@AttachedAction(TelegramEntity)
class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'
    target_type = OwnOnly()
    priority = 2

    def func(self, source, target):
        message = event_manager.publish(SkipActionGameEvent(self.session.id, self.session.turn, source.id))
        if not message.no_text:
            self.session.say(f"⬇|{source.name} пропускает ход.")
