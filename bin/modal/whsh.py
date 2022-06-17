from bin.embed import getembed
from bin.system.whsh_setid import set_whsh_id
from config.color import LIGHT_BLUE, LIGHT_ORANGE, RED
from config.emoji import BACK, BLUE_STAR, DC_BOT, DOG, GREEN_CHECK, PINK_STAR, WHITE_STAR
from discord import TextStyle,Interaction
from discord.ui import Modal,TextInput




class bot_invite(Modal,title=f"申請加入機器人"):
    url = TextInput(label="🤖邀請連結",style=TextStyle.short,placeholder="https://discord.com",max_length=200,required=True)
    pro = TextInput(label="🍡目的 (可不填)",style=TextStyle.paragraph,placeholder="新增遊戲玩法、方便管理dc、增加管管人氣",max_length=200,required=False)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(964153866750926858)
        await channel.send(embed = getembed(
            f"{DC_BOT} | 機器人申請",
            f"連結 : {self.url.value}\n"
            f"目的 : {self.pro.value}",
            LIGHT_BLUE
        ))
        await interaction.response.send_message(embed=getembed(
            f"{GREEN_CHECK} | 成功提交申請資料",
            f"請稍等管理員回應，我們有決定機器人權限之權利",
            LIGHT_ORANGE
        ),ephemeral=True)

class whsh_admin_hire(Modal,title=f"申請加入管理員"):
    name = TextInput(label="🙋🏻‍♂️班級座號與姓名",style=TextStyle.short,placeholder="21214 王小明",max_length=20,required=True)
    pro = TextInput(label="🍡加入目的",style=TextStyle.paragraph,placeholder="幫忙管理discord訊息、開發或維護 disocrdbot、定期舉辦大型活動",max_length=200,required=True)
    dc = TextInput(label="💻自述對 discord 的熟悉程度",style=TextStyle.paragraph,placeholder="會編輯個身分組權限、了解discord所有規範",max_length=200,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(910385049273245777)
        await channel.send(embed = getembed(
            f"{DOG} | 申請加入管理員",
            f"{WHITE_STAR} 班級姓名：`{self.name.value}`\n\n"
            f"{BLUE_STAR} 目的：\n{self.pro.value}\n\n"
            f"{PINK_STAR} 對 discord 的熟悉程度：\n{self.dc.value}",
            LIGHT_BLUE
        ))
        await interaction.response.send_message(embed=getembed(
            f"{GREEN_CHECK} | 成功提交申請資料",
            f"請稍等管理員回應，感謝參與文華discord內部運作",
            LIGHT_ORANGE
        ),ephemeral=True)



class whsh_advice(Modal,title=f"意見回饋"):
    name = TextInput(label="🙋🏻‍♂️原名或暱稱",style=TextStyle.short,placeholder="老乾結水球",max_length=20,required=True)
    pro = TextInput(label="🍡回報內容",style=TextStyle.paragraph,placeholder="播放音樂發生錯誤、我想舉辦電競賽",max_length=1000,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(910385049273245777)
        await channel.send(embed = getembed(
            f"📜 | 意見回饋",
            f"{WHITE_STAR} 原名或暱稱：`{self.name.value}`\n\n"
            f"{BLUE_STAR} 內容：\n{self.pro.value}",
            LIGHT_BLUE
        ))
        await interaction.response.send_message(embed=getembed(
            f"{GREEN_CHECK} | 成功提交意見回饋",
            f"請稍等管理員回應，感謝參與文華discord內部運作",
            LIGHT_ORANGE
        ),ephemeral=True)



class whsh_setid(Modal,title=f"學號綁定"):
    name = TextInput(label="🙋🏻‍♂️姓名(真實姓名)",style=TextStyle.short,placeholder="王小明",max_length=20,required=True)
    classroom = TextInput(label="📚目前班級與座號",style=TextStyle.short,placeholder="21214",max_length=10,required=True)
    ids = TextInput(label="🍡學號",style=TextStyle.short,placeholder="911125",max_length=10,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        if self.classroom.value.isdigit() and self.ids.value.isdigit():return await set_whsh_id(interaction,self.name.value,int(self.classroom.value),self.ids.value)
        ### set_whsh_id -> bin.system.whsh_setid
        else:return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 格式錯誤","",RED))