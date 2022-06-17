from discord.ext.commands import Cog,errors,Context
from config.zh_tw import *
from core.classes import Cog_Extension

class error(Cog_Extension):
    @Cog.listener()
    async def on_command_error(self,ctx:Context,error):
        if hasattr(ctx.command,'on_error'):return
        if isinstance(error,errors.MissingRequiredArgument):return await ctx.send(embed = getembed(ERROR_KEY_NOT_FOUND.format(PRE),"",RED))
        elif isinstance(error,errors.CommandOnCooldown):return await ctx.send(embed = getembed(ERROR_TIME_TICK,"",RED))
        elif isinstance(error,errors.CommandNotFound):return
        else:return await ctx.send(embed = getembed(f"{BACK} 錯誤",error,RED))

async def setup(bot):
    await bot.add_cog(error(bot))