from bin.embed import getembed
from bin.json import open_json_JoinAndLeave
from bin.select.part import part
from bin.View.Join_and_Leave_view import part_view_for_JL
from bin.system.guild.JoinandLeave import set_guild_join_message, set_guild_leave_message
from config.color import *
from config.zh_tw import *
from core.classes import Cog_Extension
from discord.ext.commands import command,Cog,Context

class JoinAndLeave(Cog_Extension,name = '歡迎與離開'):

    #指令

    @command(
        name = 'joinconnect',
        aliases=['jc'],
        brief = '設置歡迎加入訊息',
        usage = f'{PRE}jc <內容>',
        description = (
            "使用 {member} 可加入成員名稱，\n"
            "若用 {guild} 可加入伺服器名稱\n"
            "範例：\n"
            f"`{PRE}jc {'{member}'}來到了{'{guild}'}，快ban他`\n\n"
        )
    )
    async def joinconnect_(self,ctx:Context,*,msg):
        return await set_guild_join_message(self.bot,ctx,msg)


    @command(
        name = 'leaveconnect',
        aliases=['lc'],
        brief = '設置終於離開訊息',
        usage = f'{PRE}lc <內容>',
        description = (
            "使用 {member} 可加入成員名稱，\n"
            "若用 {guild} 可加入伺服器名稱\n"
            "範例：\n"
            f"`{PRE}js {'{member}'}離開了{'{guild}'}，真棒`\n\n"
        )
    )
    
    async def leaveconnect_(self,ctx:Context,*,msg):
        return await set_guild_leave_message(self.bot,ctx,msg)
    




    #玩家加入



    @Cog.listener()
    async def on_member_join(self,member):
        jwelcome = open_json_JoinAndLeave()
        if not '{}.join'.format(member.guild.id) in jwelcome:return
        guild = self.bot.get_guild(member.guild.id)
        channel = self.bot.get_channel(int(jwelcome['{}.join'.format(member.guild.id)]["channel"]))
        text = str(jwelcome['{}.join'.format(member.guild.id)]['txt'])
        if "{member}" in text:
            pos=text.find('{member}')
            tmp = text[(pos+8):]
            text = text[:(pos)] + f'{member}' + tmp
        if "{guild}" in text:
            pos=text.find('{guild}')
            tmp = text[(pos+7):]
            text = text[:(pos)] + f'{guild}' + tmp
        embed=getembed("",text,PURPLE)
        select = part(self.bot,member.guild,member)
        if len([v for v in guild.get_member(self.bot.application_id).roles if v.permissions.administrator==False and v.is_assignable()])==0:await channel.send(embed=embed)
        else:
            view = part_view_for_JL(self.bot,member.guild,member)
            msg = await channel.send(embed=embed,view=view)
            view.set_msg(msg)

    @Cog.listener()
    async def on_member_remove(self,member):
        jwelcome = open_json_JoinAndLeave()
        if not '{}.leave'.format(member.guild.id) in jwelcome:return
        guild = self.bot.get_guild(member.guild.id)
        channel = self.bot.get_channel(int(jwelcome['{}.leave'.format(member.guild.id)]["channel"]))
        text = str(jwelcome['{}.leave'.format(member.guild.id)]['txt'])
        if "{member}" in text:
            pos=text.find('{member}')
            tmp = text[(pos+8):]
            text = text[:(pos)] + f'{member}' + tmp
        if "{guild}" in text:
            pos=text.find('{guild}')
            tmp = text[(pos+7):]
            text = text[:(pos)] + f'{guild}' + tmp
        embed=getembed("",text,BLACK)
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JoinAndLeave(bot))