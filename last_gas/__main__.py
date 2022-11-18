from discord.ext import commands
from discord import app_commands
import discord
import asyncio

from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers.time_scheduler import background_scheduler, SCHEDULES
from last_gas.domain.commands.promos import pelando_promos
from last_gas.domain.commands.register_schedules import modal_scheduler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
# aclient = client()
config_manager = EnvVarConfigLoader()


@bot.command()
async def promos(ctx, *search) -> None:
    """Register the pelando promotion command."""

    await pelando_promos(ctx, *search)

@commands.command()
async def schedule(ctx) -> None:
    """Register the modal command."""

    await modal_scheduler(ctx)


async def set_scheduled_functions() -> None:
    """Schedule bot actions."""

    for schedule in SCHEDULES:
        asyncio.create_task(
            background_scheduler(
                timed_func=schedule.timed_func,
                days_of_week=schedule.days_of_week,
                times_of_day=schedule.times_of_day,
                bot=bot,
                *schedule.args,
                **schedule.kwargs,
            )
        )

async def main():
    configs = config_manager.load_configs()
    await set_scheduled_functions()
    await bot.start(configs["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())