import logging

from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Sessions import Session
from VegansDeluxe.core.TargetType import TargetType, Own, Aliveness, Team, Distance
from VegansDeluxe.core.Translator.LocalizedString import ls


class Action:
    id = 'action'
    name = ls("base_action_name")
    priority = 0
    target_type = TargetType(0, 0, 0, 0)

    type = 'action'

    def __init__(self, session: Session, source: Entity, *args):
        self.tags = []

        self.session: Session = session
        self.event_manager = self.session.event_manager

        self.source: Entity = source
        self.target: Entity = source

        self.canceled = False
        self.type = 'action'
        self.removed = False
        self.queued = False

        logging.debug(f"__init__() in Action[{self.id}] | session: {self.session.id}")

    def func(self, source, target):
        pass

    def __call__(self):  # Abstract "Run" method for overriding
        if self.canceled:
            return
        return self.func(self.source, self.target)

    @property
    def hidden(self) -> bool:
        return False

    @property
    def targets(self):
        return self.get_targets(self.source, self.target_type)

    def get_targets(self, source, target_type: TargetType):
        logging.debug(f"get_targets() in Action[{self.id}] | session: {self.session.id}")

        target_pool = self.session.entities
        targets = []

        for target in target_pool:
            conditions = [
                not (target_type.own == Own.SELF_ONLY and target != source),
                not (target_type.own == Own.SELF_EXCLUDED and target == source),

                not (target_type.aliveness == Aliveness.ALIVE_ONLY and target.dead),
                not (target_type.aliveness == Aliveness.DEAD_ONLY and not target.dead),

                not (target_type.team == Team.ALLIES_ONLY and not source.is_ally(target)),
                not (target_type.team == Team.ENEMIES_ONLY and source.is_ally(target)),

                not (target_type.distance == Distance.NEARBY_ONLY and target not in source.nearby_entities),
                not (target_type.distance == Distance.DISTANT_ONLY and target in source.nearby_entities)
            ]

            if all(conditions):
                targets.append(target)

        return targets

    @property
    def blocked(self):
        return False

    @property
    def cost(self):
        return None


class DecisiveAction(Action):
    @property
    def cost(self):
        return True


class FreeAction(Action):
    @property
    def cost(self):
        return False
