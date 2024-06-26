from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
import random

from VegansDeluxe.core import Session
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Molotov(Item):
    id = 'molotov'
    name = ls("item_molotov_name")


@AttachedAction(Molotov)
class MolotovAction(DecisiveItem):
    id = 'molotov'
    name = ls("item_molotov_name")
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, item: Item):
        super().__init__(session, source, item)
        self.tags += [ActionTag.HARMFUL]

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
        self.session.say(
            ls("item_molotov_text").format(source.name, ",".join([t.name for t in targets]))
        )

    @property
    def blocked(self):
        return self.source.energy < 2

