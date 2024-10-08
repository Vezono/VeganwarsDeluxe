from VegansDeluxe.core.Events.EventManager import EventManager
from VegansDeluxe.core.Events.Events import AttachSessionEvent
from VegansDeluxe.core.Session import Session


class SessionManager:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

        self.sessions: dict[str, Session] = dict()

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    async def attach_session(self, session: Session):
        self.sessions.update({session.id: session})
        await self.event_manager.publish(AttachSessionEvent(session.id))
        return session

    def delete_session(self, session_id):
        self.sessions.pop(session_id, None)
