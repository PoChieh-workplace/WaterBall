from discord import User
from bin.rpg.money.search import search_money, search_stock
from config.zh_tw import PRE
from core.classes import Cog_Extension
from discord.ext.commands import command,Context
from random import randint



class RPG(Cog_Extension,name = '生活系統'):
    @command(
        name="money",
        aliases=['cash','self'],
        brief = '目前生活狀況',
        usage = f'{PRE}money [@人]',
        description = (
            "錢錢就是力量"
        )
    )
    async def _search_money(self,ctx:Context,user:User=None):
        return await search_money(ctx,user)


    @command(
        name="stock",
        aliases=[],
        brief = '查詢股票資訊',
        usage = f'{PRE}stock <關鍵字>',
        description = (
            ""
        )
    )
    async def _search_stock(self,ctx:Context,name:str):
        return await search_stock(ctx,name)
    
    # @commands.Cog.listener()
    # async def on_message(self,msg):
    #     if randint(1,5)==1:earn_money(msg.author.id,randint(1000,10000))

async def setup(bot):
    await bot.add_cog(RPG(bot))