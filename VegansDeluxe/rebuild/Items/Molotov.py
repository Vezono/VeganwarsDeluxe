from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
import random

from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies


@RegisterItem
class Molotov(Item):
    id = 'molotov'
    name = 'Коктейль Молотова'


@AttachedAction(Molotov)
class MolotovAction(DecisiveItem):
    id = 'molotov'
    name = 'Коктейль Молотова'
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source, item)
        self.range = 2

    def func(self, source, target):
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            aflame = target.get_state('aflame')
            aflame.add_flame(self.session, target, source, 1)
            targets.append(target)
        source.energy = max(source.energy - 2, 0)
        self.session.say(f'🍸|{source.name} кидает коктейль молотова! '
                         f'{",".join([t.name for t in targets])} в огне!')

    @property
    def blocked(self):
        return self.source.energy < 2

