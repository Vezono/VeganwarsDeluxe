import random

from core.Items.Item import DecisiveItem
from core.TargetType import Enemies


class ThrowingKnife(DecisiveItem):
    id = 'throwingknife'

    @property
    def name(self):
        return f'Метательный нож ({self.hit_chance}%)'

    def __init__(self, source):
        super().__init__(source, target_type=Enemies())

    @property
    def hit_chance(self):
        return 40 + self.source.energy * 10

    @name.setter
    def name(self, value):
        pass

    def use(self):
        if random.randint(0, 100) > self.hit_chance:
            self.source.session.say(f"💨|{self.source.name} кидает метательный нож "
                                    f"в {self.target.name}, но не попадает.")
            return
        bleeding = self.target.get_skill('bleeding')
        bleeding.active = True
        self.target.session.say(f'🔪|{self.source.name} кидает метательный нож в {self.target.name}.'
                                f'\n❣️|{self.target.name} истекает кровью!')
