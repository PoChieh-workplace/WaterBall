import discord,asyncio
from discord.ext import commands
from core.help import CustomHelpCommand
from config.zh_tw import *
import os


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PRE,intents=intents,help_command=CustomHelpCommand())



@bot.event
async def on_ready():
    print(BOT_ONLINE_INF)
    game = discord.Game(BOT_ONLINE_SET)
    await bot.change_presence(status=discord.Status.idle, activity=game)

async def to_extensions():
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')



async def main():
    async with bot:
        await to_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())