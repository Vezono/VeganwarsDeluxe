from core.ContentManager import RegisterState, Every
from core.Context import StateContext, EventContext
from core.Events.Events import PreMoveGameEvent
from core.Skills.Skill import Skill
from rebuild.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = 'Алхимик'
    description = 'В начале игры и каждые 9 ходов дает вам сыворотку бешенства, применение ' \
                  'которой заставляет выбранную цель атаковать дополнительно к своему действию.'


@RegisterState(Alchemist)
def register(root_context: StateContext[Alchemist]):

    @Every(root_context.session.id, turns=9, event=PreMoveGameEvent)
    def func(context: EventContext[PreMoveGameEvent]):
        root_context.entity.items.append(RageSerum())
