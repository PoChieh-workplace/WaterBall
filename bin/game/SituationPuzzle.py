


import asyncio
from datetime import datetime
from typing import List
from discord import Client, Embed, Message,ButtonStyle,Interaction, SelectOption, TextStyle,User
from discord.ui import View,Button,button,Modal,TextInput,select,Select
from bin.embed import getembed
from config.color import LIGHT_BLUE, RED

from config.emoji import BACK, BLUE_STAR, PINK_STAR, PURPLE_CHECK, WHITE_STAR


class SituationPuzzle:
    class option:
        def __init__(self,author:User,ask:str,answer = None) -> None:
            self.author = author
            self.ask = ask
            self.answer = answer

    def __init__(self,message:Message,client:Client,author:User) -> None:
        self.page = 1
        self.msg = message
        self.bot = client
        self.author = author
        self.description:str = "\u200b"
        self.asks:List[self.option] = []
        self.answers:List[self.option] = []
    async def main(self):
        await self.msg.edit(embed = self.to_embed(),view = game_setting(self))

    def to_embed(self) -> Embed:
        t = datetime.now().strftime("%H:%M:%S")
        if self.asks!=[]:asks = f"{BLUE_STAR} **{self.asks[0].ask}** - 由 {self.asks[0].author.mention} 提問\n\n"
        else:asks = ""
        asks += "\n\n".join([f"{PINK_STAR} **{u.ask}** - 由 {u.author.mention} 提問" for u in self.asks[1:] if isinstance(u,self.option)])
        answers = "\n\n".join([f"{WHITE_STAR} **{u.ask}** | {u.answer}" for u in self.answers[(self.page-1)*8:(self.page*8)] if isinstance(u,self.option)])
        if asks=="":asks = "空"
        if answers=="":answers = "空"
        embed = getembed("🥣 | 海龜湯系統 SituationPuzzle",f"由 {self.author.mention} 發起,\n時間：{t}，頁數：{self.page}/{int((len(self.answers)-1)/8)+1}",LIGHT_BLUE)
        embed.add_field(name="🍡說明", value=f"{self.description}", inline=False)
        embed.add_field(name="目前提問", value=asks, inline=False)
        embed.add_field(name="已有線索", value=answers, inline=False)
        return embed


class game_setting(View):
    def __init__(self,main:SituationPuzzle):
        super().__init__(timeout=0)
        self.main = main
    @button(emoji="🔧",label="設定說明",row=1,custom_id="set_description",style=ButtonStyle.blurple)
    async def set_des_callback(self,interaction:Interaction,button:Button):
        if interaction.user != self.main.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是遊戲發起者","",RED))
        return await interaction.response.send_modal(game_modal(self.main,self))
    @button(emoji=f"{PURPLE_CHECK}",label="確認",row=1,custom_id="done",style=ButtonStyle.green,disabled=True)
    async def callback_done(self,interaction:Interaction,button:Button):
        if interaction.user != self.main.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是遊戲發起者","",RED))
        return await interaction.response.edit_message(embed=self.main.to_embed(),view = main_respond_and_answer(self.main))

#設定遊戲說明

class game_modal(Modal):
    def __init__(self,main:SituationPuzzle,setting:game_setting) -> None:
        super().__init__(title="🍡設定題目說明",timeout=0)
        self.setting = setting
        self.main = main
    description = TextInput(label="填入說明",style=TextStyle.paragraph,placeholder="一天...水球疲憊的躺在文華裡",max_length=300,min_length=10,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.description = self.description.value
        [u for u in self.setting.children if isinstance(u,Button) and u.custom_id=="done"][0].disabled = False
        await interaction.response.edit_message(embed = self.main.to_embed(),view = self.setting)

#主回覆

class main_respond_and_answer(View):


    def __init__(self,main:SituationPuzzle):
        super().__init__(timeout=0)
        self.main = main


    async def respond_ask(self,interaction:Interaction,emoji):
        if interaction.user != self.main.author:
            return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是遊戲發起者","",RED))
        elif len(self.main.asks)==0:
            return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 似乎還沒有人提出問題","",RED))
        else:
            self.main.asks[0].answer = emoji
            self.main.answers.append(self.main.asks[0])
            del self.main.asks[0]
            return await interaction.response.edit_message(embed = self.main.to_embed())


    @button(emoji="👍🏻",label="是",row=1,custom_id="yes",style=ButtonStyle.green)
    async def yes_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)


    @button(emoji="👎🏻",label="否",row=1,custom_id="no",style=ButtonStyle.red)
    async def no_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)

    @button(emoji="❔",label="無關",row=1,custom_id="nothing",style=ButtonStyle.gray)
    async def nothing_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)

    @button(emoji="◀",label="上一頁",row=2,custom_id="last",style=ButtonStyle.blurple)
    async def last_callback(self, interaction: Interaction,button:Button):
        if self.main.page + 1 > int((len(self.main.answers)-1)/8)+1:self.main.page = 1
        else:self.main.page+=1
        return await interaction.response.edit_message(embed=self.main.to_embed())


    @button(emoji="▶",label="下一頁",row=2,custom_id="next",style=ButtonStyle.blurple)
    async def next_callback(self, interaction: Interaction,button:Button):
        if self.main.page - 1 <= 0:self.main.page = int((len(self.main.answers)-1)/8)+1
        else:self.main.page-=1
        return await interaction.response.edit_message(embed=self.main.to_embed())



    @select(
        placeholder="🎈其他選項",
        options=[
            SelectOption(label="回答",value = "respond",description="提出詢問 | 版主無法使用",emoji="💬"),
            SelectOption(label="刷新訊息",value = "resend",description="更新資料並移動至最新",emoji="🔄"),
            SelectOption(label="提示",value = "remind",description="為遊戲給予提示 | 僅限版主",emoji="💡"),
            SelectOption(label="結束訊息",value = "disconnect",description="結束遊戲 | 僅限版主",emoji=f"{BACK}")
        ],
        row=3
    )
    async def select_callback(self, interaction: Interaction,select:Select):
        a = select.values[0]
        if a=="respond":
            if interaction.user == self.main.author:
                return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 發起者不可提問喔","",RED))
            
            elif len(self.main.asks)>=8:
                return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} |  資料塞車拉！","請等待版主回答後再試一次",RED))
            return await interaction.response.send_modal(ask_modal(self.main))
        elif a=="resend":
            await interaction.message.delete()
            self.main.msg = await interaction.channel.send(embed=self.main.to_embed(),view = self)
            return
        elif a=="remind":
            if interaction.user != self.main.author:
                return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是遊戲發起者","",RED))
            return await interaction.response.send_modal(remind_modal(self.main))
        elif a=="disconnect":
            if interaction.user != self.main.author:
                return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是遊戲發起者","",RED))
            self.main.description += "\n(遊戲已經結束)"
            for i in self.children:
                if i.custom_id not in ['last','next']:i.disabled = True
            await interaction.response.edit_message(embed=self.main.to_embed(),view=self)
            await asyncio.sleep(300)
            return await self.main.msg.edit(embed=self.main.to_embed(),view=None)


#學生提問表單

class ask_modal(Modal):
    def __init__(self,main:SituationPuzzle) -> None:
        super().__init__(title="🍡提出問題",timeout=0)
        self.main = main
    description = TextInput(label="填入",style=TextStyle.short,placeholder="主角是水球嗎？",max_length=50,min_length=3,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.asks.append(self.main.option(interaction.user,self.description.value))
        await interaction.response.edit_message(embed = self.main.to_embed())


#提示

class remind_modal(Modal):
    def __init__(self,main:SituationPuzzle) -> None:
        super().__init__(title="💡 給點提示",timeout=0)
        self.main = main
    description = TextInput(label="填入",style=TextStyle.short,placeholder="主角是水球喔！",max_length=50,min_length=3,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.answers.append(self.main.option(interaction.user,self.description.value,"💡"))
        await interaction.response.edit_message(embed = self.main.to_embed())
