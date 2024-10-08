from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.Items.Stimulator import Stimulator


class Medic(Skill):
    id = 'medic'
    name = ls("rebuild.skill.medic.name")
    description = ls("rebuild.skill.medic.description")


@RegisterState(Medic)
async def register(root_context: StateContext[Medic]):
    session: Session = root_context.session
    source = root_context.entity

    source.items.append(Stimulator())
