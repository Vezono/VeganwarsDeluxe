from VegansDeluxe.core import Item, FreeItem, AttachedAction
from VegansDeluxe.core import RegisterItem
from VegansDeluxe.core import Allies


@RegisterItem
class Adrenaline(Item):
    id = 'adrenaline'
    name = 'Адреналин'


@AttachedAction(Adrenaline)
class AdrenalineAction(FreeItem):
    id = 'adrenaline'
    name = 'Адреналин'
    target_type = Allies()
    priority = -2

    def func(self, source, target):
        target.energy += 3
        self.session.say(f'💉|{self.source.name} использует адреналин на {target.name}! '
                         f'Его енергия увеличена на 3.')
