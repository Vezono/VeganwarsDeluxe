from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.core import RegisterState, Every
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = ls("rebuild.skill.alchemist.name")
    description = ls("rebuild.skill.alchemist.description")


@RegisterState(Alchemist)
async def register(root_context: StateContext[Alchemist]):

    @Every(root_context.session.id, turns=9, event=PreMoveGameEvent)
    async def func(context: EventContext[PreMoveGameEvent]):
        root_context.entity.items.append(RageSerum())
