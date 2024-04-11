import discord
from discord.ext import commands
from discord.ext.commands import Context

import bot


# TODO: Lol. Alles.

class Lists(commands.Cog, name="lists"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def print_packliste(self, context: Context) -> None:
        embed = discord.Embed(
            description="Platzhalter",
            color=0xE02B2B,
        )
        await context.send(embed=embed)

    async def add_packliste(self, context: Context, data) -> None:
        embed = discord.Embed(
            description=f"Added **{data}** to packing list.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(name="packliste", description="Platzhalter.")
    async def packliste(self, context: Context) -> None:

        subparams = context.message.content[1:].replace(context.invoked_with, "")[1:]
        subparams_arg = subparams.split(" ")

        if context.message.content == bot.PREFIX + "packliste":
            await self.print_packliste(context)

        elif subparams_arg[0] == "add":
            await self.add_packliste(context, ' '.join(subparams_arg[1:]))


async def setup(bot) -> None:
    await bot.add_cog(Lists(bot))
