from uuid import uuid4

from core.Events.EventManager import EventManager
from core.Events.Events import AttachStateEvent
from core.States import State
from core.Weapons.Weapon import Weapon
from core.Items.Item import Item
from core.DamageHolder import DamageHolder


class Entity:
    type = 'entity'

    def __init__(self,
                 session_id: str = '', name: str = '',
                 hp: int = 0, max_hp: int = 0,
                 energy: int = 0, max_energy: int = 0):

        self.session_id = session_id
        self.name: str = name
        self.id = str(uuid4())

        self.hp: int = hp
        self.max_hp: int = max_hp
        self.dead = False

        self.energy: int = energy
        self.max_energy: int = max_energy

        self.weapon: Weapon = Weapon(session_id, self.id)
        self.skills: list[State] = []
        self.items: list[Item] = []

        self.nearby_entities: list[Entity] = []

        self.team = None

        # Temporary
        self.inbound_dmg = DamageHolder()
        self.outbound_dmg = DamageHolder()

        self.outbound_accuracy_bonus = 0
        self.inbound_accuracy_bonus = 0

        self.notifications = ""

    @property
    def hearts(self):
        return '♥️' * self.hp if self.hp < 8 else f"♥️x{self.hp}"

    @property
    def energies(self):
        return '⚡️' * self.energy if self.energy < 8 else f"⚡️x{self.energy}"

    def get_item(self, item_id: str):
        items = list(filter(lambda i: i.id == item_id, self.items))
        if items:
            item = items[0]
            item.source = self
            return item

    def attach_state(self, state: State, event_manager: EventManager):
        self.skills.append(state)
        event_manager.publish(AttachStateEvent(self.session_id, self.id, state))

    def get_state(self, skill_id: str) -> State:
        result = list(filter(lambda s: s.id == skill_id, self.skills))
        if result:
            return result[0]

    def is_ally(self, target):
        if target == self:
            return True
        if target.team is None or self.team is None:
            return False
        return target.team == self.team

    def pre_move(self):
        self.outbound_dmg.clear()
        self.inbound_dmg.clear()

        self.outbound_accuracy_bonus = 0
        self.inbound_accuracy_bonus = 0

        self.notifications = ""

    def tick_turn(self):
        pass
