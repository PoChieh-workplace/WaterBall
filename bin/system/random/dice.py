from random import randint
from discord import Client
from discord.ext import commands
from bin.embed import getembed
from config.color import GREEN

class MAX_SMALLER_THAN_MIN(commands.CommandError):
    """最大值不可小於最小值"""
class NUMBER_ERROR(commands.CommandError):
    """資料型態錯誤，必須為數字"""
class FLOAT_ERROR(commands.CommandError):
    """小數最多只能10位數"""


async def to_dice_a_number(client:Client,ctx,max:int,min:int,flo:int):
    if max<min:raise MAX_SMALLER_THAN_MIN("最大值不可小於最小值")
    elif flo>10:raise FLOAT_ERROR("小數最多只能10位數")
    t = 10**flo
    req = randint(min*t,max*t)/t
    await ctx.send(
        embed = getembed(
            f"🎲骰出 {min}~{max}",
            f"{req}",
            GREEN
        )
    )