import discord
from discord import ui
from bin.modal.user import edit_member_introduce_modal
from config.emoji import BACK, LIGHT_BLUE_CHECK, PENCIL
from config.zh_tw import CONCIAL, WHSH_PART_GET_SUCCESS





class member_information_edit_view(ui.View):
    def __init__(self):
        super().__init__(timeout=0)
    @discord.ui.button(emoji = f"{PENCIL}",label="編輯個人資料",style=discord.ButtonStyle.blurple)
    async def button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled = True
        await interaction.response.send_modal(edit_member_introduce_modal())




class part_color(ui.View):
    def __init__(self):
        super().__init__(timeout=0)
    @discord.ui.button(emoji = f"{LIGHT_BLUE_CHECK}",label="確定申請",style=discord.ButtonStyle.green)
    async def green_button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled = True
        guild =  interaction.client.get_guild(910150769624358914)
        member = guild.get_member(interaction.user.id)
        await member.add_roles(guild.get_role(913649078582272030))
        await interaction.response.edit_message(embed = WHSH_PART_GET_SUCCESS,view = self)
    @discord.ui.button(emoji = f"{BACK}",label="取消",style=discord.ButtonStyle.blurple)
    async def button_callback(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(embed = CONCIAL,view = self)