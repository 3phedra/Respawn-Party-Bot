import discord
from discord.ext import commands
from discord.ext.commands import Context

# TODO: Der reminder hat noch keine remind funktion. Außerdem is der code echt hässlich.
# TODO: Validation bei der Eingabe von duration - entschlüsseln nach Sekunden, Minuten etc. und formatieren in sqlite

class Timers(commands.Cog, name="timers"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def remindme_list(self, context: Context) -> None:

        user = context.author

        reminders_list = await self.bot.database.get_reminders(user.id, context.guild.id)
        embed = discord.Embed(title=f"Reminders of {user}", color=0xBEBEFE)
        description = ""
        if len(reminders_list) == 0:
            description = "This user has no reminders."
        else:
            for reminder in reminders_list:
                (user_id, server_id, reason, termination_time, created_at, reminder_id) = reminder
                description += f"[{reminder_id}]: {reason} in {termination_time}\n"

        embed.description = description
        await context.send(embed=embed)

    async def remindme_del(self, context: Context, reminder_id) -> None:
        member = context.guild.get_member(context.author.id) or await context.guild.fetch_member(
            context.author.id
        )
        if reminder_id == 0:
            total = await self.bot.database.remove_all_reminders(context.author.id, context.guild.id)
            embed = discord.Embed(
                description=f"I've removed all reminders from **{member}**!\nTotal reminders for this user: {total}",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        else:
            total = await self.bot.database.remove_reminder(reminder_id, context.author.id, context.guild.id)
            embed = discord.Embed(
                description=f"I've removed reminder **#{reminder_id}** from **{member}**!\nTotal reminders for this user: {total}",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="remindme", description="Reminds you of something.", )
    # async def remindme(self, context: Context, reason: str = "Not specified", duration: str = "1h") -> None:
    async def remindme(self, context: Context, *, args: str = "Not specified 1h") -> None:

        if args.startswith("delete") and not args == "delete all":
            try:
                del_id = args.split(' ')[1]
                await self.remindme_del(context, int(del_id))
            except:
                embed = discord.Embed(
                    description="nö.",
                    color=0xBEBEFE,
                )
                await context.send(embed=embed)

        elif args == "delete all":
            await self.remindme_del(context, 0)

        else:
            duration = args.split(' ')[-1]
            reason = args[:-len(duration) - 1]

            if reason == "Not specified":
                await self.remindme_list(context)

            else:
                user = context.author
                # termination_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                termination_time = duration
                reminder_id = await self.bot.database.add_reminder(user.id, context.guild.id, reason, termination_time)
                embed = discord.Embed(
                    description=f"Reminder successfully added for {user.mention} with the ID {reminder_id}.",
                    color=0xBEBEFE,
                )
                await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Timers(bot))
