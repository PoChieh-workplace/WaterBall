import asyncio,discord
from bin.FacebookRequest import *
from bin.time import dateCalculate, getTempNowTime
from bin.json import open_json_date, write_json_date
from core.classes import Cog_Extension

class DateListener(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        async def time_task():
            now_time = getTempNowTime("%d")-1
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if now_time != getTempNowTime("%d"):
                    #倒數日
                    data = open_json_date()
                    for i in data:
                        c = data[i]
                        try:
                            channel = self.bot.get_channel(c["id"])
                        except:
                            del data[i]
                            write_json_date(data)
                            continue
                        date = dateCalculate(c["year"],c["month"],c["day"])
                        await channel.edit(name = c["name"].format(date))
                    now_time = getTempNowTime("%d")
                await asyncio.sleep(1000)
        self.bg_task = self.bot.loop.create_task(time_task())
async def setup(bot):
    await bot.add_cog(DateListener(bot))