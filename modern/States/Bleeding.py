from core.States.State import State


class Bleeding(State):
    def __init__(self):
        super().__init__(id='bleeding', name='Кровотечение', constant=True)
        self.bleeding = 3
        self.active = False

    def __call__(self, source):
        if source.session.stage != 'pre-damages':
            return
        if not self.active:
            return
        if self.bleeding <= 0:
            source.session.say(f'🩸|{source.name} теряет ХП от кровотечения! Осталось {source.hp-1} ХП.')
            source.hp -= 1
            self.active = False
            self.bleeding = 3
            return
        source.session.say(f'🩸|{source.name} истекает кровью! ({self.bleeding})')
        self.bleeding -= 1


