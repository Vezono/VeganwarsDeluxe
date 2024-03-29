from typing import Union, Optional

from VegansDeluxe.core.Actions.Action import Action
from VegansDeluxe.core.Actions.ItemAction import ItemAction
from VegansDeluxe.core.Actions.StateAction import StateAction
from VegansDeluxe.core.Actions.WeaponAction import WeaponAction
from VegansDeluxe.core.Entities.Entity import Entity
from VegansDeluxe.core.Events.Events import PostUpdateActionsGameEvent, PreUpdateActionsGameEvent
from VegansDeluxe.core.Items.Item import Item
from VegansDeluxe.core.SessionManager import SessionManager
from VegansDeluxe.core.Sessions import Session
from VegansDeluxe.core.States import State
from VegansDeluxe.core.Weapons import Weapon

ActionOwnerType = Union[type[Entity], type[Weapon], type[State], type[Item]]


class ActionManager:
    def __init__(self, session_manager: SessionManager, action_map: dict[ActionOwnerType, list[type[Action]]]):
        self.session_manager = session_manager
        self.event_manager = session_manager.event_manager

        """
        self.action_queue: Queue of Actions from all active Sessions.
        self.actions: Map of Session & Entity pairs to Actions.
        """
        self.action_queue: list[Action] = []
        self.actions: dict[tuple[Session, Entity], list[Action]] = {}

        self.action_map = action_map

    def reset_removed_actions(self, session_id):
        session = self.session_manager.get_session(session_id)
        for entity in session.entities:
            entity_actions = self.actions[(session, entity)]
            for action in entity_actions:
                action.removed = False

    def attach_action(self, session: Session, entity: Entity, action_id: str):
        owner_type, action_type = self.get_action_from_all_actions(action_id)
        if owner_type.type == 'entity':
            action = action_type(session, entity)
        elif owner_type.type == 'weapon':
            action = action_type(session, entity, owner_type(session.id, entity.id))
        else:
            action = action_type(session, entity, owner_type())
        self.actions[(session, entity)].append(action)

    def update_entity_actions(self, session: Session, entity: Entity):
        self.event_manager.publish(PreUpdateActionsGameEvent(session.id, session.turn, entity.id))

        entity_actions = self.actions.get((session, entity))
        if not entity_actions:
            entity_actions = []
            self.actions[(session, entity)] = entity_actions
        entity_actions.clear()

        entity_type = type(entity)
        if entity_type in self.action_map:
            for action in self.action_map[entity_type]:
                action: type[Action]
                entity_actions.append(action(session, entity))

        weapon_type = type(entity.weapon)
        if weapon_type in self.action_map:
            for action in self.action_map[weapon_type]:
                action: type[WeaponAction]
                entity_actions.append(action(session, entity, entity.weapon))

        for state in entity.states:
            state_type = type(state)
            if state_type in self.action_map:
                for action in self.action_map[state_type]:
                    action: type[StateAction]
                    entity_actions.append(action(session, entity, state))

        for item in entity.items:
            item_type = type(item)
            if item_type in self.action_map:
                for action in self.action_map[item_type]:
                    action: type[ItemAction]
                    entity_actions.append(action(session, entity, item))

        self.event_manager.publish(PostUpdateActionsGameEvent(session.id, session.turn, entity.id))

    def update_actions(self, session: Session):
        for entity in session.entities:
            self.update_entity_actions(session, entity)

    def get_action(self, session: Session, entity: Entity, action_id: str) -> Action:
        actions = filter(lambda a: action_id == a.id, self.get_actions(session, entity))
        return next(actions, None)

    def get_actions(self, session: Session, entity: Entity):
        return self.actions.get((session, entity), [])

    def get_available_actions(self, session: Session, entity: Entity) -> list[Action]:
        actions = self.get_actions(session, entity)
        result = []
        for action in actions:
            if action.removed:
                continue
            if action.hidden:
                continue
            result.append(action)
        return result

    def is_action_available(self, session: Session, entity: Entity, action_id: str) -> bool:
        for action in self.get_available_actions(session, entity):
            if action.id == action_id:
                return True
        return False

    def get_queued_entity_actions(self, session: Session, entity: Entity) -> list[Action]:
        result = []
        for action in self.get_queued_session_actions(session):
            if action.source != entity:
                continue
            result.append(action)
        return result

    def get_queued_session_actions(self, session: Session) -> list[Action]:
        queue = [action for action in self.action_queue if action.session.id == session.id]
        return queue

    def remove_action(self, session: Session, entity: Entity, action_id: str):
        action = self.get_action(session, entity, action_id)
        if action:
            action.removed = True
        return action

    def queue_action(self, session: Session, entity: Entity, action_id: str) -> bool:
        action: Action = self.get_action(session, entity, action_id)
        action.queued = True
        return self.queue_action_instance(action)

    def queue_action_instance(self, action: Action) -> bool:
        self.action_queue.append(action)
        action.queued = True
        return not action.cost

    def get_action_from_all_actions(self, action_id: str) -> Optional[tuple[type[ActionOwnerType], type[Action]]]:
        for action_owner in self.action_map:
            for action in self.action_map[action_owner]:
                if action.id == action_id:
                    return action_owner, action


