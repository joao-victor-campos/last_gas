import discord
from discord.ext import commands

class SurveyModal(discord.ui.Modal, title = "Survey"):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label="name", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_massage(f'Submission entered', ephemeral=True)

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

class SurveyView(discord.ui.View):
    def __init__(self, *, timeout=180) -> None:
        super().__init__()(timeout=timeout)
        self.add_item(Select())

async def modal_scheduler(ctx):
    print("Pinto")
    #await interaction.response.send_modal(SurveyModal())
    await ctx.send(view = SurveyView())


    
