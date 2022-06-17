import discord
from discord.ext.commands import command,Context
from bin.embed import getembed
from config.color import ORANGE, Face
from config.zh_tw import PRE
from core.classes import Cog_Extension

class Info(Cog_Extension,name = "機器人資訊"):
    @command(
        name="bot",
        aliases=[],
        brief = '機器人自介',
        usage = f'{PRE}bot'
    )
    async def _information(self,ctx:Context):
        embed = getembed(
            "關 於 WaterBall 2.0",
            "\n".join([
                "我的生日是 `2021/8/4`{}，已改名數次".format(Face("happy")),
                "經過的風風雨雨堪比一位高中生💦",
                "最愛吃麻婆豆腐🍣，差點吃到中風",
                "在校喜歡唱歌🎵，總遠離 **男友** 以外的男生",
                "對主人 PoChieh 採絕對服從",

                "\n 想知道更多?來看[網頁](http://pochieh.ddns.net:6001/])吧~"
            ]),
            ORANGE
        )
        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))