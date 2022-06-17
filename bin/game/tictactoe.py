import asyncio
import discord
from discord.ui import Button,View
from discord import Interaction
from bin.embed import getembed
from config.color import GREEN, PURPLE, RED

from config.emoji import BACK, ORANGE_BUTTERFLY, RED_BUTTERFLY, WHITE_STAR
from config.zh_tw import GAME_SETTING, NOW_PLAYERS_TURN, WAIT_FOR_PLAYER_TITLE, WIN_GAME


CIRCLE_EMOJI_GAME = "⭕"
FORK_EMOJI_GAME = "❌"

class turn:
    def __init__(self,turn:int,player:discord.User,emoji:str,button_color:discord.ButtonStyle,color) -> None:
        self.turn = turn
        self.player=player
        self.emoji=emoji
        self.button_color=button_color
        self.color=color


win_list = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [1,5,9],
    [3,5,7]
]




class TicTacToe:
    def __init__(self,player1:discord.User,msg:discord.Message,bot:discord.Client) -> None:
        self.game_end = False
        self.turn = 1
        self.player1 = turn(1,player1,CIRCLE_EMOJI_GAME,discord.ButtonStyle.green,GREEN)
        self.player2 = turn(2,None,FORK_EMOJI_GAME,discord.ButtonStyle.danger,RED)
        self.message = msg
        self.bot = bot
        self.view = board(self)

    def now_player_return(self):
        if self.turn ==1:return self.player1
        elif self.turn ==2:return self.player2
        else: return None

    def if_end(self):
        list1=[]
        for i in self.view.children:
            if i.label == self.now_player_return().emoji:list1.append(int(i.custom_id))
        for i in win_list:
            if (i[0] in list1) and (i[1] in list1) and (i[2] in list1):return self.now_player_return().player.name
            elif len(list1) >=5:return "平手"
        return False

    async def main(self):
        to_wait = wait_player(self)
        await self.message.edit(embed = getembed(
                WAIT_FOR_PLAYER_TITLE.format(self.player1.player.name),
                "\n".join([
                    f"正在等待遊戲開始",
                    f"對峙玩家：`有點空`"
                ]),
                PURPLE
            ),
            view = to_wait
        )
        while(to_wait.game_start==False):await asyncio.sleep(1)
        del to_wait
        await self.message.edit(embed = getembed(
                NOW_PLAYERS_TURN.format(self.now_player_return().emoji,self.now_player_return().player),
                "",
                self.now_player_return().color
            )
            ,view=self.view
        )        
        while(self.game_end==False):await asyncio.sleep(1)


class wait_player(View):
    def __init__(self,game:TicTacToe):
        self.game_start = False
        self.game = game
        super().__init__(timeout=0)
    async def update_embed(self,interaction:Interaction):
        if self.game.player2.player==None:msg = "有點空"
        else:msg = self.game.player2.player.name
        await interaction.response.edit_message(
            embed = getembed(
                WAIT_FOR_PLAYER_TITLE.format(self.game.player1.player.name),
                "\n".join([
                    f"正在等待遊戲開始",
                    f"對峙玩家：`{msg}`"
                ]),
                PURPLE
            )
        )
    @discord.ui.button(emoji=f"{RED_BUTTERFLY}",label="加入",row=1,custom_id="join",style = discord.ButtonStyle.green)
    async def callback_join(self,interaction:Interaction,button:Button):
        if self.game.player2.player == None:
            self.game.player2.player=interaction.user
            await self.update_embed(interaction)
        else:await interaction.response.send_message(embed = getembed(f"{BACK} | 裡面已經有人了","",RED),ephemeral=True)
    @discord.ui.button(emoji=f"{BACK}",label="剔除",row=1,custom_id="kick",style=discord.ButtonStyle.danger)
    async def callback_kick(self,interaction:Interaction,button:Button):
        if self.game.player2.player == None:await interaction.response.send_message(embed = getembed(f"{BACK} | 裡面沒有人耶","",RED),ephemeral=True)
        elif interaction.user==self.game.player1 or interaction.user== self.game.player2.player:
            self.game.player2.player=None
            await self.update_embed(interaction)
        else:await interaction.response.send_message(embed = getembed(f"{BACK} | 你沒有權限剔除人家","",RED),ephemeral=True)
    @discord.ui.button(emoji="🎮",label="開始",row=1,custom_id="start",style=discord.ButtonStyle.blurple)
    async def callback_start(self,interaction:Interaction,button:Button):
        if self.game.player2.player ==None:await interaction.response.send_message(embed = getembed(f"{BACK} | 跟空氣玩遊戲？","",RED),ephemeral=True)
        else:
            self.game_start=True
            await interaction.response.edit_message(embed=GAME_SETTING)










class board(View):
    def __init__(self,game:TicTacToe):
        self.game = game
        super().__init__(timeout=0)
    async def update(self,interaction:Interaction,button:Button):
        if interaction.user==self.game.now_player_return().player:
            button.style=self.game.now_player_return().button_color
            button.label=self.game.now_player_return().emoji
            button.disabled=True
            check_end = self.game.if_end()
            if isinstance(check_end,str):
                for i in self.children:
                    i.disabled = True
                await interaction.response.edit_message(embed = getembed(
                        WIN_GAME.format(ORANGE_BUTTERFLY,check_end),
                        "",
                        self.game.now_player_return().color
                    )
                    ,view=self
                )
                self.game.game_end=True
                return
                
            if self.game.turn==1:self.game.turn=2
            else :self.game.turn=1
            await interaction.response.edit_message(embed = getembed(
                    NOW_PLAYERS_TURN.format(self.game.now_player_return().emoji,self.game.now_player_return().player.name),
                    "",
                    self.game.now_player_return().color
                ),view=self)
        else:await interaction.response.send_message(embed = getembed(f"{BACK} | 還敢亂啊？","",RED),ephemeral=True)





    @discord.ui.button(label="⬜",row=1,custom_id="1")
    async def callback_1(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=1,custom_id="2")
    async def callback_2(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=1,custom_id="3")
    async def callback_3(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=2,custom_id="4")
    async def callback_4(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=2,custom_id="5")
    async def callback_5(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=2,custom_id="6")
    async def callback_6(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=3,custom_id="7")
    async def callback_7(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=3,custom_id="8")
    async def callback_8(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)
    @discord.ui.button(label="⬜",row=3,custom_id="9")
    async def callback_9(self,interaction:Interaction,button:Button):
        await self.update(interaction,button)