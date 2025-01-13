__all__ = (
    "check_sqlite_connection",
)


from sys import exit as sys_exit
from sqlite3 import Connection, Error
from sqlite3 import connect as sync_connect

from utils.env import DATABASE_NAME


sqlite_connection: bool | Connection = False


def check_sqlite_connection() -> None:
    try:
        sqlite_connection = sync_connect(DATABASE_NAME)
        cursor = sqlite_connection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print(f"SQLite Database Version is: {record}")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `RoleLock` (
                guild_id                TEXT NOT NULL,
                role_id                 TEXT,
                alert_message           TEXT,
                delete_after            INTEGER,
                PRIMARY KEY (guild_id)
            );
        """)

        cursor.close()
    except Error as error:
        print(f"[SQLite Error] Error while connecting to SQLite {error}")
        sys_exit()
    except Exception as error:
        print(f"[Unknown Error] Error on DB loading: {error}")
        sys_exit()
