from bin.FacebookRequest import getFbPost
from bin.json import open_json_FBpost,write_json_FBpost
from bin.system.WHSHannounce import openAnnounce, writeAnnounce
from bin.embed import getembed
from bin.time import RewriteTime, TimeZoneChange

from cmds.Permission import HavePermission
from config.TimeConfig import WHSH_FUCK_TIME, WHSH_FUCK_TO_TIME
from config.color import RED
from config.zh_tw import *
from core.classes import Cog_Extension

from discord.ext.commands import command,Context



class FBrequest(Cog_Extension,name='貼文訂閱'):
    @command(name = 'fbpost',aliases=[])
    async def sendfacebookpost(self,ctx:Context,msg):
        if not HavePermission(ctx.author.id,ctx.guild.id,4):
            await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
            return
        try:
            data = getFbPost(msg)
        except KeyError:
            await ctx.channel.send(embed=getembed("",WHSH_POST_GET_ERROR.format(msg),RED))
            return
        usedata = data['posts']['data'][0]
        message = usedata['message']
        Title = message.split("\n",1)
        time = RewriteTime(TimeZoneChange(usedata['created_time'],WHSH_FUCK_TIME),WHSH_FUCK_TO_TIME)
        embed = getembed(
            WHSHembed.title.format(Title[0]),
            WHSHembed.description.format(
                Title[1],
                time,
                Title[0][1:],
                usedata["id"]
            ),
            WHSHembed.color
        )
        await ctx.channel.send(embed=embed)
    @command(name='post',aliases=[])
    async def _ConnectPost(self,ctx:Context,modify:str,data:str):
        if not HavePermission(ctx.author.id,ctx.guild.id,3):
            await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
            return
        jdata = open_json_FBpost
        if modify in ADD_LIST:
            try:
                if ctx.channel.id in jdata["sendchannel"][data]:
                    await ctx.channel.send(embed=getembed("",POST_HAVE_CONNECT.format(data),RED))
                else:
                    jdata["sendchannel"][data].append(ctx.channel.id)
                    write_json_FBpost(jdata)
                    await ctx.channel.send(embed=getembed("",POST_CONNECT_SUCCESS.format(data,ctx.channel.name,PRE,"post",data),GREEN))
                return
            except KeyError:
                await ctx.channel.send(embed=getembed("",POST_CONNECT_KEY_ERROR.format(data,PRE),RED))
                return
        elif modify in DELETE_LIST:
            try:
                jdata["sendchannel"][data].remove(ctx.channel.id)
                write_json_FBpost(jdata)
                await ctx.channel.send(embed=getembed("",POST_DISCONNECT_SUCCESS.format(ctx.channel.name,data),GREEN))
            except ValueError:
                await ctx.channel.send(embed=getembed("",POST_REMOVE_KEY_ERROR.format(ctx.channel.name,data),RED))
                return
            except KeyError:
                await ctx.channel.send(embed=getembed("",POST_CONNECT_KEY_ERROR.format(data,PRE),RED))
                return
    @command(name='announce',aliases=[])
    async def _ConnectAnnounce(self,ctx:Context,modify:str,data:str):
        if not HavePermission(ctx.author.id,ctx.guild.id,3):
            await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
            return
        jdata = openAnnounce()
        if modify in ["add","set"]:
            try:
                if ctx.channel.id in jdata[data]:
                    await ctx.channel.send(embed=getembed("",POST_HAVE_CONNECT.format(data),RED))
                else:
                    jdata[data].append(ctx.channel.id)
                    writeAnnounce(jdata)
                    await ctx.channel.send(embed=getembed("",POST_CONNECT_SUCCESS.format(data,ctx.channel.name,PRE,"announce",data),GREEN))
                return
            except KeyError:
                await ctx.channel.send(embed=getembed("",POST_CONNECT_KEY_ERROR.format(data,PRE),RED))
                return
        elif modify in ["remove","delete"]:
            try:
                jdata[data].remove(ctx.channel.id)
                writeAnnounce(jdata)
                await ctx.channel.send(embed=getembed("",POST_DISCONNECT_SUCCESS.format(ctx.channel.name,data),GREEN))
            except ValueError:
                return await ctx.channel.send(embed=getembed("",POST_REMOVE_KEY_ERROR.format(ctx.channel.name,data),RED))
            except KeyError:
                return await ctx.channel.send(embed=getembed("",POST_CONNECT_KEY_ERROR.format(data,PRE),RED))
                

async def setup(bot):
    await bot.add_cog(FBrequest(bot))