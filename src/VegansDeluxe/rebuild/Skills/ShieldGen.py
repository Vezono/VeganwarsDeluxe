from VegansDeluxe.core import Allies
from VegansDeluxe.core import At
from VegansDeluxe.core import AttachedAction, StateContext, RegisterState
from VegansDeluxe.core import Entity
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import PostDamageGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class ShieldGen(Skill):
    id = 'shield-gen'
    name = ls("rebuild.skill.shield_gen.name")
    description = ls("rebuild.skill.shield_gen.description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(ShieldGen)
async def register(root_context: StateContext[ShieldGen]):
    session: Session = root_context.session
    source = root_context.entity


@AttachedAction(ShieldGen)
class ShieldGenAction(DecisiveStateAction):
    id = 'shield-gen'
    name = ls("rebuild.skill.shield_gen.action.name")
    target_type = Allies()
    priority = -2

    def __init__(self, session: Session, source: Entity, skill: ShieldGen):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 5
        if target == source:
            self.session.say(ls("rebuild.skill.shield_gen.action.text").format(source.name))
        else:
            self.session.say(ls("rebuild.skill.shield_gen.action_targeted").format(source.name, target.name))

        @At(self.session.id, turn=self.session.turn, event=PostDamageGameEvent)
        async def shield_block(context: EventContext[PostDamageGameEvent]):
            if context.event.target != target:
                return
            if not context.event.damage:
                return
            context.event.damage = 0
