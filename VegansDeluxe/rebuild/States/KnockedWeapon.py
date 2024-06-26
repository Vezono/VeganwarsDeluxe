from VegansDeluxe.core import AttachedAction, OwnOnly
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core.Translator.LocalizedString import ls


class KnockedWeapon(State):
    id = 'knocked-weapon'

    def __init__(self):
        super().__init__()
        self.weapon = None


@AttachedAction(KnockedWeapon)
class PickUp(DecisiveStateAction):
    id = 'pick_up'
    name = ls("state_knocked_weapon_name")
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: KnockedWeapon):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.weapon

    def func(self, source, target):
        source.weapon = self.state.weapon
        self.session.say(ls("state_knocked_weapon_text").format(source.name))
        self.state.weapon = None
