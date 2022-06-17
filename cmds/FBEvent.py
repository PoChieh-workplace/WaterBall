import datetime,json,asyncio
import discord
from bin.FacebookRequest import *
from bin.time import RewriteTime, TimeZoneChange
from config.TimeConfig import WHSH_FUCK_TIME, WHSH_FUCK_TO_TIME
from config.color import RED, Face
from config.emoji import KB_WHSH
from config.zh_tw import WHSHembed
from core.classes import Cog_Extension 
from bin.json import open_json_FBpost
import requests
import facebook
import urllib3




class FBpost(Cog_Extension):
    #a = datetime.datetime.now().strftime('%Y %m %d %H %M')
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        async def time_task():
            await self.bot.wait_until_ready()
            class FbError:
                WordTooLong = "字數過多導致無法顯示{}".format(Face("sad"))
                ErrorNotfound = "基於某些問題，無法顯示本篇消息{}"
                IdNotFound = "突然找不到舊有的 id 了 {}\n將為您更新重置到最新貼文"
            Id = "whsh"
            data = getFbPost(Id)
            while not self.bot.is_closed():
                await asyncio.sleep(50)
                now_time=0
                if (int(now_time)%15==0):
                    data = getFbPost(Id)
                    count = getCount(Id,data)
                    print(f"whsh:{count}")
                    def sendmessage(i):
                        usedata = data['posts']['data'][i]
                        message = usedata['message']
                        Title = message.split("\n",1)
                        time = RewriteTime(TimeZoneChange(usedata['created_time'],WHSH_FUCK_TIME),WHSH_FUCK_TO_TIME)
                        embed = discord.Embed(
                            title = WHSHembed.title.format(""+f"{KB_WHSH}"+Title[0]),
                            description = WHSHembed.description.format(
                                Title[1],
                                time,
                                Title[0][1:],
                                usedata["id"]
                            ),
                            color = WHSHembed.color
                        )
                        embed.set_footer(text="Code by Po-Chieh")
                        return embed

                    if count==-1:
                        for k in open_json_FBpost()["sendchannel"]["whsh"]:
                            channel = self.bot.get_channel(k)
                            embed = discord.Embed(title="神奇錯誤💦",description = FbError.IdNotFound.format(Face("sad")),color = RED)
                            embed.set_footer(text="Code by Po-Chieh")
                            await channel.send(embed=embed)
                    elif(count==0):
                        pass
                    else:
                        for i in range(count):
                            try:
                                embed = sendmessage(count-i-1)
                                for k in open_json_FBpost()["sendchannel"]["whsh"]:
                                    channel = self.bot.get_channel(k)
                                    await channel.send(embed=embed)
                            except:
                                for k in open_json_FBpost()["sendchannel"]["whsh"]:
                                    channel = self.bot.get_channel(k)
                                    embed = discord.Embed(title = "神奇錯誤💦",description = FbError.ErrorNotfound.format(Face("sad")),color = RED)
                                    embed.set_footer(text="Code by Po-Chieh")
                                    await channel.send(embed=embed)
                        await asyncio.sleep(100)
                    updateNowId(Id,data)
                now_time = datetime.datetime.now().strftime('%M')
        self.bg_task = self.bot.loop.create_task(time_task())
async def setup(bot):
    await bot.add_cog(FBpost(bot))