from bin.embed import getembed
from bin.rpg.money.config import CHECK_IN_CHANNEL_ID, CHECK_IN_MONEY
from bin.rpg.rpgsql import get_money_info, limit,earn_money
from config.color import PURPLE
from config.emoji import MONEY_PAPER
from discord import Client, Message
from datetime import date


async def check_in(bot:Client,message:Message):
    if message.channel.id == CHECK_IN_CHANNEL_ID:
        id = message.author.id
        limit.check_data(id)
        data = limit.get_data_from_date(id,'check_in')
        if data != date.today():
            limit.set_date_to_now(id,'check_in')
            earn_money(id,CHECK_IN_MONEY)
            await message.add_reaction(bot.get_emoji(967781525737320579))
            await message.author.send(
                embed=getembed(
                    "💳 | 簽到成功",
                    f"成功領取 {CHECK_IN_MONEY} 元 | 目前存款：{get_money_info(id)}",
                    PURPLE
                )
            )    
    return