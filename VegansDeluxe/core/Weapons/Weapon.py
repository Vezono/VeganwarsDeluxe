import functools

from VegansDeluxe.core.Translator.LocalizedString import ls


class Weapon:
    id = 'None'
    name = ls("base_weapon_name")
    description = ls("base_weapon_description")
    ranged = False

    energy_cost = 2
    cubes = 2
    damage_bonus = 0
    accuracy_bonus = 0

    type = 'weapon'

    @classmethod
    @property
    @functools.cache
    def melee(cls):
        return not cls.ranged

    def __init__(self, session_id: str, entity_id: str):
        self.session_id = session_id
        self.entity_id = entity_id

    def reload_text(self, source):
        if self.ranged:
            tts = ls("base_weapon_reload_text_ranged").format(source.name, source.max_energy)
        else:
            tts = ls("base_weapon_reload_text_melee").format(source.name, source.max_energy)
        return tts

    def hit_chance(self, source) -> int:
        if source.energy <= 0:
            return 0
        total_accuracy = source.energy + self.accuracy_bonus + source.outbound_accuracy_bonus
        cubes = self.cubes
        return int(max((1 - ((1 - total_accuracy / 10) ** cubes)) * 100, 0))


class MeleeWeapon(Weapon):
    ranged = False


class RangedWeapon(Weapon):
    ranged = True
