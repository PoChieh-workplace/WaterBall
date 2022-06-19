


from discord import User
from discord.ext.commands import Context,CommandError

from bin.embed import getembed
from config.emoji import BACK




async def fight(ctx:Context,user:User,user2:User=None):
    if user2==None:pass
    elif user==user2:return await ctx.send(embed = getembed(
        f"{BACK} | 原來你的老公是小三",f"{user2.mention}"
    ))