import importlib
import psutil,os
from discord.ext.commands import command,Context
from bin.embed import getembed
from cmds.Permission import HavePermission
from config.color import *
from config.emoji import GREEN_CHECK
from config.zh_tw import NO_PERMISSION, RAM_EMBED
from core.classes import Cog_Extension

class Ram(Cog_Extension,name = '機器人系統'):
    @command(name = "ram",aliases=[])
    async def send_now_Ram(self,ctx:Context):
        if not HavePermission(ctx.author.id,ctx.guild.id,4):
            await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
            return
        def my_ram():
            process = psutil.Process(os.getpid())
            return (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        memoryEmbed = getembed(RAM_EMBED.TITLE,RAM_EMBED.DESCRIPTION.format(my_ram()),RAM_EMBED.color)
        await ctx.send(embed=memoryEmbed)



    @command(name="load")
    async def load_pyfile(self,ctx:Context,extension):
        if not HavePermission(ctx.author.id,ctx.guild.id,4):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        await self.bot.load_extension(f'cmds.{extension}')
        await ctx.channel.send(f'Load cmds.{extension} Done')



    @command(name = "reload")
    async def reload_pyfile(self,ctx:Context,extension):
        if not HavePermission(ctx.author.id,ctx.guild.id,2):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        await self.bot.reload_extension(f'cmds.{extension}')
        await ctx.channel.send(f'reLoad {extension} Done')



    @command(name = "unload")
    async def unload_pyfile(self,ctx:Context,extension):
        if not HavePermission(ctx.author.id,ctx.guild.id,4):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        await self.bot.unload_extension(f'cmds.{extension}')
        await ctx.channel.send(f'unLoad cmds.{extension} Done')

    @command(name = "reimport")
    async def reload_pysys(self,ctx:Context,extension):
        if not HavePermission(ctx.author.id,ctx.guild.id,4):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        importlib.reload(extension)
        await ctx.channel.send(f'reimport {extension} Done')


    @command(name = "ping",aliases=[])
    async def _test_ping(self,ctx:Context):
        await ctx.channel.send(content = f"{GREEN_CHECK}")
async def setup(bot):
    await bot.add_cog(Ram(bot))
