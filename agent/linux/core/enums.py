from enum import StrEnum


class EventSource(StrEnum):
    SSH = "ssh"


class EventType(StrEnum):
    LOGIN_FAILED = "login_failed"
    LOGIN_SUCCESS = "login_success"
    INVALID_USER = "invalid_user"
    ROOT_LOGIN = "root_login"
    PUBLICKEY_LOGIN = "publickey_login"
    AUTHENTICATION_TIMEOUT ="authentication_timeout"

class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"

class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    CLOSED = "closed"