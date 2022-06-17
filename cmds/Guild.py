from datetime import date
from bin.View.whsh import whsh_curriculum_button
from bin.embed import getembed
from bin.View.function_view import whsh_selection
from bin.rpg.money.CheckIn import check_in
from bin.rpg.rpgsql import earn_money, limit
from bin.sql import check_if_whsh, get_tmp_nickname, get_whsh_inf, set_tmp_nickname
from bin.system.guild.guild import search_guild_inf
from bin.system.guild.member import search_member_inf

from cmds.Permission import HavePermission
from config.zh_tw import *
from core.classes import Cog_Extension

from discord import Member, User, VoiceState,Message
from discord.ext.commands import command,Cog,Context
from discord.errors import Forbidden

class guild(Cog_Extension,name = '伺服器'):
    @command(
        name = "guild",
        aliases=["server"],
        brief = '查詢伺服器資訊',
        usage = f'{PRE}guild',
        description = (
            "顯示資訊\n"
        )
    )
    async def _guild_information(self,ctx:Context):
        return await search_guild_inf(ctx)

    @command(
        name = "member",
        aliases=["user"],
        brief = '查詢成員資訊',
        usage = f'{PRE}member <@人/人id>',
        description = (
            "顯示玩家資料\n"
            "範例\n"
            f"`{PRE}r @水球` 顯示水球資料\n\n"
            f"`{PRE}r 45623` 顯示id為45623的玩家資料\n\n"
        )
    )
    async def _member_information(self,ctx:Context,arg:User=None,ids:int = None):
        return await search_member_inf(ctx,arg,ids)



    @command(
        name = "function",
        aliases=['whsh','f'],
        brief = '伺服器功能快捷鍵',
        usage = f'{PRE}f',
        description = (
            "管理身分組、徵選管管、意見回饋、學號綁定"
        )
    )
    async def _whsh_control(self,ctx:Context):
        return await ctx.send(embed = WHSH_CONTROL_TEXT,view = whsh_selection())



    @command(
        name = "purge",
        aliases = ['clean'],
        brief = '清理訊息',
        usage = f'{PRE}purge <數量>',
        description = (
            "清理數則訊息"
        )
    )
    async def _clean_message(self,ctx:Context,count:int):
        if not HavePermission(ctx.author.id,ctx.guild.id,3):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        await ctx.channel.purge(limit=count)
        return await ctx.send(embed = getembed("",PURGE_SECCESS.format(count),GREEN))


    # 沒用的東西
    # @commands.command(name= "history",aliases = ['his','past'])
    # async def _check_histury(self,ctx,channel:discord.TextChannel=None):
    #     if channel==None:channel = ctx.channel
    #     for i in [message async for message in channel.history(limit=123)]:print(type(i))


    #以下為文華群專用功能

    @command(
        name = "curriculum",
        aliases = ['c','class'],
        brief = '查詢文華課表',
        usage = f'{PRE} <數量>',
        description = (
            "清理數則訊息"
        )
    )
    async def classc(self,ctx:Context,cls:str):
        if not check_if_whsh(ctx.author):return await ctx.send(embed = getembed(f"{BACK} | 尚未註冊，無法辨識","請使用 *f - 學號註冊 功能後再試一次",RED))
        c = whsh_curriculum_button(ctx.author,cls)
        msg = await ctx.channel.send(embed = GAME_SETTING,view = c)
        await c.start(msg)


    #文華群簽到
    @Cog.listener()
    async def on_message(self,message:Message):
        return await check_in(self.bot,message)


    # 阿傑教室自動改名
    @Cog.listener()
    async def on_voice_state_update(self,user:Member,bf:VoiceState,af:VoiceState):
        try:
            r = get_whsh_inf(user)
            i = self.bot.get_channel(976787068518809640)
            if r != None:
                if af.channel!=None:
                    if af.channel.category==i:
                        if bf.channel==None:set_tmp_nickname(user)
                        elif bf.channel.category!=i:set_tmp_nickname(user)
                        await user.edit(nick=f"{r[3]}{r[1]}")
                    elif bf.channel!=None:
                        if bf.channel.category==i and af.channel.category!=i:
                            await user.edit(nick=get_tmp_nickname(user))
                elif bf.channel.category==i:
                    await user.edit(nick=get_tmp_nickname(user))
        except Forbidden:pass
async def setup(bot):
    await bot.add_cog(guild(bot))