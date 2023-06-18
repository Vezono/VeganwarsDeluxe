from core.Skills.Skill import Skill
from core.Action import DecisiveAction
from core.TargetType import TargetType, Enemies


class Thief(Skill):
    def __init__(self, source):
        super().__init__(source, id='thief', name='Вор', constant=True)

    def __call__(self):
        pass

    def steal(self, source, target):
        success = False
        source.say(f'{target} юзает: {", ".join([item.name for item in target.item_queue])}')
        for item in target.item_queue:
            source.session.say(f'😏|{target.name} хотел использовать {item.name}, но вор {source.name} его украл!')
            success = True
            source.items.append(item)
            item.source = source
            item.canceled = True
        if not success:
            source.session.say(f'😒|Вору {source.name} не удается ничего украсть у {target.name}!')

    @property
    def actions(self):
        return [
            DecisiveAction(self.steal, self.source, target_type=Enemies(),
                           name='Украсть предмет', id='steal', priority=-1)
        ]


