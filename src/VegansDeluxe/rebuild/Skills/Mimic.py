import random

from VegansDeluxe.core import AttachedAction, Next
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Everyone, Own
from VegansDeluxe.core import PostUpdateActionsGameEvent, DeliveryRequestEvent, DeliveryPackageEvent
from VegansDeluxe.core import RegisterEvent, RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Mimic(Skill):
    id = 'mimic'
    name = ls("rebuild.skill.mimic.name")
    description = ls("rebuild.skill.mimic.description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0
        self.memorized_action = None


@RegisterState(Mimic)
async def register(root_context: StateContext[Mimic]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=PostUpdateActionsGameEvent)
    async def post_update_actions(update_context: EventContext[PostUpdateActionsGameEvent]):
        if update_context.event.entity_id != source.id:
            return
        if root_context.state.memorized_action:
            update_context.action_manager.attach_action(session, source, root_context.state.memorized_action)


@AttachedAction(Mimic)
class CopyAction(DecisiveStateAction):  # TODO: Fix Mimic
    id = 'copyAction'
    name = ls("rebuild.skill.mimic.action.name")
    priority = -2
    target_type = Everyone(own=Own.SELF_EXCLUDED)

    def __init__(self, session: Session, source: Entity, skill: Mimic):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source, target):
        @Next(self.session.id, event=DeliveryPackageEvent)
        async def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager

            action_pool = []
            for action in action_manager.action_queue:
                if action.type == 'item':
                    continue
                if action.source != target:
                    continue
                action_pool.append(action)

            if not action_pool:
                self.session.say(ls("rebuild.skill.mimic.action_miss").format(source.name, target.name))
                return

            self.session.say(ls("rebuild.skill.mimic.action.text").format(source.name, target.name))

            action = random.choice(action_pool)
            self.state.memorized_action = action.id

        await self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))

        self.state.cooldown_turn = self.session.turn + 6


