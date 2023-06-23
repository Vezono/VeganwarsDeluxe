from core.States.State import State
from core.Action import DecisiveAction
from core.TargetType import TargetType, OwnOnly


class Knockdown(State):
    id = 'knockdown'

    def __init__(self, source):
        super().__init__(source, constant=True)
        self.active = False

    def __call__(self):
        source = self.source
        if not self.active:
            return
        if source.session.event.moment == 'post-update':
            source.remove_action('attack')
            source.remove_action('dodge')

    def stand_up(self, source, target):
        self.active = False
        source.session.say(f'⬆️|{source.name} поднимается с земли.')

    @property
    def actions(self):
        if not self.active:
            return []
        return [
            DecisiveAction(self.stand_up, self.source, target_type=OwnOnly(), name='Поднятся с земли', id='stand_up')
        ]


