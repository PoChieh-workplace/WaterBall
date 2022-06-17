import json
import discord
from discord.ext.commands import command,Context
from bin.embed import getembed
from bin.json import open_json_permission,write_json_permission
from config.zh_tw import *
from core.classes import Cog_Extension



def setlevel(level):
    if level == "4" or level == "devoloper":
        return 4
    elif level == "3" or level == "admin":
        return 3
    elif level == "2" or level == "high":
        return 2
    else:
        return "Err"
def getlevel(member:int,guild:int):
    k=0
    data = open_json_permission()
    if member in data["devoloper"]:
            return 4
    if str(guild) in data["admin"]:
        if member in data["admin"]["{}".format(guild)]:
            return 3
    else:
        k=1
    if str(guild) in data["high"]:
        if member in data["high"]["{}".format(guild)]:
            return 2
    else:
        if k==1:return 3
        else:return 1
    return 1
    
def givelevel(i):
    if i==4:return "devoloper"
    elif i==3:return "admin"
    elif i==2:return "high"
    else:return "normal"

def HavePermission(memberId:int,guild:int,level:int):
    if getlevel(memberId,guild)>=level:
        return True
    else:
        return False


class Permission(Cog_Extension,name = '權限'):
    @command(name="permission",aliases=[])
    async def _Permission(self,ctx:Context,modify:str,member:discord.User,level:str):
        data = open_json_permission()
        L = setlevel(level)
        if isinstance(L,str):
            embed = getembed("",PERMISSION_KEY_ERROR.format(PRE),RED)
            await ctx.channel.send(embed=embed)
        tag = member.id
        if L==4:
            embed = getembed("",PERMISSION_DEVOLOPER_ERROR,RED)
            await ctx.channel.send(embed=embed)
            return
        if (modify in ADD_LIST):
            if getlevel(ctx.author.id,ctx.guild.id)<L:
                embed = getembed("",PERMISSION_LOWER,RED)
                await ctx.channel.send(embed=embed)
                return
            elif getlevel(tag,ctx.guild.id)>L:
                embed = getembed("",PERMISSION_HAVE_HIGHER.format(member.name,level),RED)
                await ctx.channel.send(embed=embed)
            elif getlevel(tag,ctx.guild.id)==L:
                embed = getembed("",PERMISSION_HAVED.format(member.name,level),RED)
                await ctx.channel.send(embed=embed)
            else:
                try:
                    data["{}".format(level)]["{}".format(ctx.guild.id)].append(tag)
                    write_json_permission(data)
                except KeyError:
                    data["{}".format(level)]["{}".format(ctx.guild.id)] = [tag]
                    write_json_permission(data)
                embed = getembed("",PERMISSION_EDIT_SUCCESS.format("新增",member.name,level),GREEN)
                await ctx.channel.send(embed=embed)
        elif (modify in DELETE_LIST):pass
        else:
            embed = getembed("",PERMISSION_KEY_ERROR.format(PRE),RED)
            await ctx.channel.send(embed=embed)



    @command(name = "sendpermission", aliases=[])
    async def _send_permission(self,ctx:Context,member:discord.User):
        embed = getembed("",PERMISSION_GET.format(member.name,givelevel(getlevel(member.id,ctx.guild.id))),LIGHT_BLUE)
        await ctx.channel.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Permission(bot))