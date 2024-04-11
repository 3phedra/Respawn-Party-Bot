class Mixin:
    async def add_reminder(self, user_id: int, server_id: int, reason: str, termination_time: str) -> int:
        """
        This function will add a reminder to the database.

        :param user_id: The ID of the user that should be reminded.
        :param termination_time: The termination date and time of the reminder.
        :param reason: The description of the reminder.
        """
        rows = await self.connection.execute(
            "SELECT id FROM reminders WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            reminder_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO reminders(id, user_id, server_id, reason, termination_time) VALUES (?, ?, ?, ?, ?)",
                (
                    reminder_id,
                    user_id,
                    server_id,
                    reason,
                    termination_time
                ),
            )
            await self.connection.commit()
            return reminder_id

    async def remove_reminder(self, reminder_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a reminder from the database.

        :param reminder_id: The ID of the reminder.
        :param user_id: The ID of the user that was reminded.
        :param server_id: The ID of the server where the user has been reminded
        """
        await self.connection.execute(
            "DELETE FROM reminders WHERE id=? AND user_id=? AND server_id=?",
            (
                reminder_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM reminders WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def remove_all_reminders(self, user_id: int, server_id: int) -> int:
        """
        This function will remove all reminders from the database.

        :param user_id: The ID of the user that was reminded.
        :param server_id: The ID of the server where the user has been reminded
        """
        await self.connection.execute(
            "DELETE FROM reminders WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM reminders WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_reminders(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the reminders of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the reminders of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, reason, termination_time, strftime('%s', created_at), id FROM reminders WHERE "
            "user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
