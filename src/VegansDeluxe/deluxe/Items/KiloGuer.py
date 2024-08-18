from VegansDeluxe.core import Item, FreeItem, AttachedAction, ActionTag, Entity, Everyone
from VegansDeluxe.core import RegisterItem
from VegansDeluxe.core import Allies
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class KiloGuer(Item):
    id = 'kilo-guer'
    name = "Guer"


@AttachedAction(KiloGuer)
class KiloGuerAction(FreeItem):
    id = 'kilo-guer'
    name = "Kilo-Guer"
    target_type = Everyone()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    def func(self, source: Entity, target: Entity):
        target.hp += 1000
        self.session.say(f"💉{target.name} {self.name}!")