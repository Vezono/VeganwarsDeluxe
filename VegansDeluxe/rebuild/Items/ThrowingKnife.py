import random

from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import Item
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class ThrowingKnife(Item):
    id = 'throwing_knife'
    name = ls("item_throwing_knife_name")


@AttachedAction(ThrowingKnife)
class ThrowingKnifeAction(DecisiveItem):
    id = 'throwing_knife'
    target_type = Enemies()

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.HARMFUL]

    @property
    def name(self):
        return ls("item_throwing_knife_name_percentage").format(self.hit_chance)

    @property
    def hit_chance(self):
        return 40 + self.source.energy * 10

    def func(self, source, target):
        source.energy -= 1
        if random.randint(0, 100) > self.hit_chance:
            self.session.say(ls("item_throwing_knife_name_miss").format(source.name, target.name))
            return
        bleeding = target.get_state('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
        bleeding.active = True
        self.session.say(
            ls("item_throwing_knife_text").format(source.name, target.name)
        )
