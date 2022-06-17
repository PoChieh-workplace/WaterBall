from random import choice

from discord import Client
from bin.embed import getembed
from bin.image.rate import pick_img
from config.color import BLACK

from discord.ext.commands import Context


async def random_is_ok(bot:Client,ctx:Context,title:str):
    files,num = pick_img(title)
    if num >= 100 and num < 150:msg = "我覺得一定是了拉"
    elif num >= 150:msg = "我覺得一定不是喔"
    else:msg = choice([f"我覺得 {100-num}% 是",f"我覺得 {num}% 不行"])
    embed = getembed(
        f" 詢問",
        f"{ctx.author.mention}：**{title}**\n\n{bot.user.mention}：`{msg}`",
        BLACK
    )
    embed.set_image(url='attachment://image.png')
    await ctx.send(embed = embed,file = files)