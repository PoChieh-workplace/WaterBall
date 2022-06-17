from bin.embed import getembed
from bin.time import dateCalculate
from bin.json import openDate,writeDate
from cmds.Permission import HavePermission
from config.color import GREEN, RED
from config.zh_tw import ADD_LIST, DATE_CHANNEL_DELETE_SUCCESS, DATE_CHANNEL_EDIT_SUCCESS, DATE_CHANNEL_NOT_FOUND, DATE_KEY_ERROR, DELETE_LIST, NO_PERMISSION, PRE

async def date_channel_setting(ctx,modify,type):

    if not HavePermission(ctx.author.id,ctx.guild.id,3):return await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))   
    if modify in ADD_LIST:
        if len(type)!=4:return await ctx.channel.send(embed = getembed("",DATE_KEY_ERROR.format(PRE),RED))
        else:
            await ctx.channel.edit(name = type[3].format(dateCalculate(int(type[0]),int(type[1]),int(type[2]))))
            data = openDate()
            data["{}".format(ctx.channel.id)] = {"id":ctx.channel.id,"year":int(type[0]),"month":int(type[1]),"day":int(type[2]),"name":type[3]}
            writeDate(data)
            return await ctx.channel.send(embed = getembed("",DATE_CHANNEL_EDIT_SUCCESS.format(ctx.channel.name),GREEN))
    elif modify in DELETE_LIST:
        data = openDate()
        if not str(ctx.channel.id) in data:
            await ctx.channel.send(embed = getembed("",DATE_CHANNEL_NOT_FOUND,RED))
        else:
            del data["{}".format(ctx.channel.id)]
            writeDate(data)
            return await ctx.channel.send(embed = getembed("",DATE_CHANNEL_DELETE_SUCCESS.format(ctx.channel.name),GREEN)) 
    else:return await ctx.channel.send(embed = getembed("",DATE_KEY_ERROR.format(PRE),RED))