import discord
from discord.ext.commands import command,Context
from config.color import *
from config.zh_tw import PRE
from core.classes import Cog_Extension


class Vote(Cog_Extension):
    @command(
        name = "vote",
        aliases = ['v'],
        brief = '開發中',
        usage = f'{PRE}vote <標題>',
        description = (
            "開發中"
        )
    )
    async def _create_vote(self,ctx:Context,*arg:str):
        pass


async def setup(bot):
    await bot.add_cog(Vote(bot))