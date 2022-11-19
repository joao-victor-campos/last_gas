import discord
from discord.ext import commands
from discord import app_commands


class ScheduleSurveyModal(discord.ui.Modal, title="Survey"):
    schedule_name = discord.ui.TextInput(label="Schedule Name")
    days_of_week = discord.ui.TextInput(label="Days of Week")
    times_of_day = discord.ui.TextInput(label="Times of Day")
    args = discord.ui.TextInput(label="Args")
    kwargs = discord.ui.TextInput(label="Kwargs")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Submission entered", ephemeral=True)


class ScheduleCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, _, err):
        print(err)

    @app_commands.command(name="schedule")
    async def schedule_command(self, interaction) -> None:
        await interaction.response.send_modal(ScheduleSurveyModal())
