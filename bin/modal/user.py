from bin.json import open_json_member_inf,write_json_member_inf
from bin.embed import getembed
from discord import TextStyle,Interaction
from discord.ui import TextInput,Modal
from config.color import GREEN
from config.emoji import GREEN_CHECK
from config.zh_tw import PRE



class edit_member_introduce_modal(Modal,title="🎀修改個人資料"):
    birthday = TextInput(label="🎂生日 Birthday",style=TextStyle.short,placeholder="2000/1/1",max_length=30,required=False)
    introduce = TextInput(label="🍡個人簡介",style=TextStyle.paragraph,placeholder="我只想說管理員很帥",max_length=200,required=False)
    async def on_submit(self, interaction: Interaction) -> None:
        data = open_json_member_inf()
        if data.get(interaction.user.id) == None:
            data["{}".format(interaction.user.id)] = {
                "mate":"單身",
                "birthday":"未填寫",
                "information":"未填寫"
            }
        if self.birthday.value != "":data["{}".format(interaction.user.id)]["birthday"] = self.birthday.value
        if self.introduce.value != "":data["{}".format(interaction.user.id)]["information"] = self.introduce.value
        write_json_member_inf(data)
        await interaction.response.send_message(embed=getembed(
            f"{GREEN_CHECK} | 成功編輯資料",
            f"可再次使用 **{PRE}member** 查看修正",
            GREEN
        ),ephemeral=True)
