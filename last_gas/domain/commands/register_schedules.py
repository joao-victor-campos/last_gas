import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from sqlalchemy import create_engine

from last_gas.adapters.db_adapters import PostgresLoader
from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers import Schedules


class ScheduleSurveyModal(discord.ui.Modal, title="Survey"):
    schedule_name = discord.ui.TextInput(label="Schedule Name")
    schedule_type = discord.ui.TextInput(label="Schedule Type")
    days_of_week = discord.ui.TextInput(label="Days of Week")
    times_of_day = discord.ui.TextInput(label="Times of Day")
    args = discord.ui.TextInput(label="Args")
    kwargs = discord.ui.TextInput(label="Kwargs")

    async def on_submit(self, interaction: discord.Interaction):
        print(
            f"{self.schedule_name},{self.days_of_week},{self.times_of_day},{self.args},{self.kwargs}"
        )
        schedule = Schedules(
            self.schedule_name,
            self.days_of_week,
            self.times_of_day,
            self.args,
            self.kwargs,
            datetime.now(),
            datetime.now(),
            self.schedule_type,
        )
        config_manager = EnvVarConfigLoader()
        configs = config_manager.load_configs()
        database_url = configs["DATABASE_URL"]

        engine = create_engine(database_url)
        loader = PostgresLoader(engine)
        loader.insert(schedule)
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
