import random

import modern
from core.Skills.Skill import Skill


class Stockpile(Skill):
    id = 'stockpile'
    name = 'Запасливый'
    description = 'В начале матча вы получаете два дополнительных предмета.'

    def register(self, session_id):
        given = []
        for _ in range(2):
            item = random.choice(modern.game_items_pool)(self.source)
            pool = list(filter(lambda i: i(self.source).id not in given, modern.game_items_pool))
            pool = list(filter(lambda i: i.id not in [playerItem.id for playerItem in self.source.items], pool))
            if pool:
                item = random.choice(pool)(self.source)
            else:
                random.choice(modern.game_items_pool)(self.source)
            given.append(item.id)
            self.source.items.append(item)