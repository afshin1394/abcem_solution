from app.domain.events.event import Event


class AuthenticatedEvent(Event):
        is_ip_valid : bool
        jwt_token: str
        refresh_token: str