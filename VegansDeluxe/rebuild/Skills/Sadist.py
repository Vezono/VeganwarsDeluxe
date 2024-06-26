from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import HPLossGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Sadist(Skill):
    id = 'sadist'
    name = ls("skill_sadist_name")
    description = ls("skill_sadist_description")


@RegisterState(Sadist)
def register(root_context: StateContext[Sadist]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    def func(context: EventContext[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy = min(source.energy + context.event.hp_loss, source.max_energy)
            session.say(ls("skill_sadist_effect").format(source.name, context.event.hp_loss))
