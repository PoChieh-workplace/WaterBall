from bin.system.datechannel import date_channel_setting
from config.zh_tw import PRE
from core.classes import Cog_Extension
from discord.ext.commands import command,Context



class DateCalculate(Cog_Extension,name = "倒數日系統"):
    @command(
        name = "datechannel",
        aliases = ['date'],
        brief = '設定倒數日頻道',
        usage = f'{PRE}datechannel <add/remove> [年] [月] [日] [名稱]',
        description = (
            "使用`{}` 將顯示日期，注意！discord頻道名稱不可有空白\n"
            "範例：\n"
            f"`{PRE}date add 2024 1 1 跨年倒數{'{}'}天` -> 跨年倒數***天\n\n"
            f"`{PRE}dice remove` 取消倒數\n\n"
        )
    )
    async def _Set_Date_Channel(self,ctx:Context,modify,*type):
        return await date_channel_setting(ctx,modify,type)
async def setup(bot):
    await bot.add_cog(DateCalculate(bot))