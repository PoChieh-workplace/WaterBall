from discord.ext.commands import command,Context

from config.color import *
from config.zh_tw import PRE
from core.classes import Cog_Extension
from bin.select.game import Game_select


class Game(Cog_Extension,name = '遊戲廳'):
    @command(
        name="game",
        aliases=['g'],
        brief = '是遊戲！！可以玩嗎？',
        usage = f'{PRE}game',
        description = (
            "允許虛擬賭博，但別搞到家庭分裂呦！\n"
        )
    )
    async def _play_game(self,ctx:Context):
        await ctx.send(view = Game_select())

async def setup(bot):
    await bot.add_cog(Game(bot))