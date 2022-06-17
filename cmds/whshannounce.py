import asyncio,discord
from bin.FacebookRequest import *
from bin.system.WHSHannounce import announce, openAnnounce
from bin.time import getTempNowTime
from core.classes import Cog_Extension

class Announce(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        async def time_task():
            now_time = getTempNowTime("%d")
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if now_time != getTempNowTime("%d"):
                    #文華日報
                    data = openAnnounce()
                    embed = announce()
                    if len(data["WHSHannounce"])!=0:
                        for i in data["WHSHannounce"]:
                            channel = self.bot.get_channel(i)
                            await channel.send(embed=embed)
                    now_time = getTempNowTime("%d")
                await asyncio.sleep(1000)
        self.bg_task = self.bot.loop.create_task(time_task())
async def setup(bot):
    await bot.add_cog(Announce(bot))