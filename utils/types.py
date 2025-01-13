__all__ = (
    "RoleLock",
)


from typing import Optional, TypedDict


class RoleLock(TypedDict):
    guild_id: str
    role_id: Optional[str]
    alert_message: Optional[str]
    delete_after: Optional[int]
