
from discord.ext import commands

from bin.embed import getembed
from config.color import WHITE
from config.emoji import BLUE_STAR, DC_BOT, PINK_STAR, WHITE_STAR
from config.zh_tw import PRE

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__()

        
    async def send_bot_help(self, mapping) -> None:
        await self.get_destination().send(
            embed=getembed(
                f"📖 指令清單",
                "\n\n".join(
                    [f"{BLUE_STAR} {cog.qualified_name}：\n {'、'.join([f'`{PRE}{command.name}`' for command in mapping[cog]])}"
                     for cog in mapping if cog!=None and len(mapping[cog])!=0]
                     +[f"{DC_BOT} 使用 `{PRE}help <群組名/指令>` 查詢更好的指令說明"]),
                WHITE
            )
        )
    
    async def send_cog_help(self, cog) -> None:
        await self.get_destination().send(
            embed=getembed(
                f"{cog.qualified_name} 的指令庫",
                "\n\n".join([f"{PINK_STAR} {PRE}{command.name}：{command.brief}" for command in cog.get_commands()]),
                WHITE
            )
        )
    async def send_group_help(self, group) -> None:
        await self.get_destination().send(
            embed=getembed(
                f"{group.name} 的指令庫",
                "\n\n".join([f"{PINK_STAR} {PRE}{command.name}：{command.brief}" for command in enumerate(group.commands)]),
                WHITE
            )
        )

    async def send_command_help(self, command:commands.Command) -> None:
        await self.get_destination().send(
            embed = getembed(
                f"🎀 {command.name} 指令使用說明",
                f"{WHITE_STAR} {command.brief}\n\n"
                f"{BLUE_STAR}別稱：{'、'.join([f'`{PRE}{i}`' for i in command.aliases])}\n"
                f"{PINK_STAR}用法： `{command.usage}`\n"
                f"{command.description}",
                WHITE
            )
        )