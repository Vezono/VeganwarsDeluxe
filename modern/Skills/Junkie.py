import random

from core.Actions.ActionManager import action_manager
from core.Events.DamageEvents import AttackGameEvent
from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import AttachStateEvent, PreActionsGameEvent, PreDamagesGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.Items.Adrenaline import Adrenaline
from modern.Items.Hitin import Hitin
from modern.Items.Jet import Jet
from modern.Items.RageSerum import RageSerum
from modern.Items.Stimulator import Stimulator


class Junkie(Skill):
    id = 'junkie'
    name = 'Наркоман'
    description = 'Ваша точность понижена на 1. Каждый раз, когда вы применяете 💉медикамент, ' \
                  'ваша точность на этом ходу увеличивается на 2, а урон на 1.'


@RegisterState(Junkie)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    source.items.append(random.choice([Jet, Hitin, Adrenaline, Stimulator])())

    @event_manager.now(session.id, PreActionsGameEvent)
    def pre_actions(message: PreActionsGameEvent):
        accuracy_bonus = 0
        damage_bonus = 0
        for action in action_manager.get_queued_entity_actions(session, source):
            if action.id in [Jet.id, Hitin.id, Adrenaline.id, Stimulator.id, RageSerum.id]:
                accuracy_bonus += 2
                damage_bonus += 1

        source.outbound_accuracy_bonus += accuracy_bonus

        @event_manager.now(session.id, event=AttackGameEvent)
        def attack_handler(attack_message: AttackGameEvent):
            if attack_message.source != source:
                return
            if attack_message.damage:
                attack_message.damage += damage_bonus

        @event_manager.now(session.id, event=PreDamagesGameEvent)
        def post_actions(actions_message: PreDamagesGameEvent):
            session.say(f"🙃|{source.name} получает бонусную точность и урон!")