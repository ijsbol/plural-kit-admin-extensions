__all__: tuple[str, ...] = (
    "DISCORD_BOT_TOKEN",
    "DATABASE_NAME",
    "YOUR_DISCORD_USER_ID",
)


from os import getenv

from dotenv import load_dotenv


load_dotenv()


def _get_int(key: str) -> int:
    value = getenv(key)
    if value is None or value == "null":
        return 0
    return int(value)


def _get_str(key: str) -> str:
    value = getenv(key)
    assert value is not None
    return value


DISCORD_BOT_TOKEN: str = _get_str("DISCORD_BOT_TOKEN")
DATABASE_NAME: str = _get_str("DATABASE_NAME") + ".db"
YOUR_DISCORD_USER_ID: int = _get_int("YOUR_DISCORD_USER_ID")
