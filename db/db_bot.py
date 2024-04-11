import aiosqlite

import db.submodules.timers.db_timer as db_timer
import db.submodules.moderation.db_warn as db_warn
import db.submodules.lists.db_lists as db_lists


class DatabaseManager(db_timer.Mixin,
                      db_warn.Mixin,
                      db_lists.Mixin
                      ):
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

