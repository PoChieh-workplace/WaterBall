import discord
from discord import ui
from discord.ext import commands
from core.classes import Cog_Extension
from config.color import *

class get_modal(ui.Modal,title="test"):
    answer1 = ui.TextInput(label="I am handsome",style=discord.TextStyle.short,placeholder="Yes",default="Yes",required=True,max_length=10)
    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=self.title,description=f"**{self.answer1.label}**\n{self.answer1}",color=BLUE)
        embed.set_author(name = interaction.user,icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

class get_button(ui.View):
    @discord.ui.button(label="click",style=discord.ButtonStyle.green,custom_id="123")
    async def button_callback(self,interaction,button):
        button.disabled = True
        await interaction.response.send_modal(get_modal())



class modal(Cog_Extension):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name = "modal",aliases=[])
    async def _set_modal(self,ctx):
        msg = await ctx.send(content = "button",view = get_button())

        
async def setup(bot):
    await bot.add_cog(modal(bot))