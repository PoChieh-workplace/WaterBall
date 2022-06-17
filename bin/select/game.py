from discord.ui import Select,View,select
from discord import Interaction,SelectOption
from bin.game.SituationPuzzle import SituationPuzzle
from bin.game.halfpastten import HalfPastTen
from bin.game.tictactoe import TicTacToe
from config.emoji import *
from config.zh_tw import *


options = [
    ["SMALL - 圈圈叉叉 Tic-tac-toe",        "TicTacToe",            "建議人數：2人，遊玩時間：1分鐘",            "⭕"],
    ["MIDDLE - 十點半 Half-past-ten",       "HalfPastTen",          "建議人數：2~8人，遊玩時間：5分鐘",          "🃏"],
    ["MIDDLE - 海龜湯 Situation-puzzle",    "SituationPuzzle",      "建議人數：2人以上，遊玩時間：20分鐘",       "🥣"]
]






class Game_select(View):
    def __init__(self) -> None:
        super().__init__(timeout=0)
    @select(
        placeholder="🎮請選擇遊戲",
        options=[
            SelectOption(label=c[0],value = c[1],description=c[2],emoji=c[3]) for c in options
        ]
    )
    async def callback(self, interaction: Interaction,select:Select):
        select.disabled = True
        await interaction.response.edit_message(view = self)
        msg = await interaction.channel.send(embed = GAME_SETTING)

        if select.values[0] == "TicTacToe":game = TicTacToe(interaction.user,msg,interaction.client)
        elif select.values[0] == "HalfPastTen":game = HalfPastTen(msg,interaction.client,interaction.user)
        elif select.values[0] == "SituationPuzzle":game = SituationPuzzle(msg,interaction.client,interaction.user)

        await game.main()
        del game