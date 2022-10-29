from discord.ext import commands

from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers.time_scheduler import background_scheduler, SCHEDULES
from last_gas.domain.commands.promos import pelando_promos


bot = commands.Bot(command_prefix="$")
config_manager = EnvVarConfigLoader()


@bot.command()
async def promos(ctx, *search) -> None:
    """Register the pelando promotion command."""

    await pelando_promos(ctx, *search)


def set_scheduled_functions() -> None:
    """Schedule bot actions."""

    for schedule in SCHEDULES:
        bot.loop.create_task(
            background_scheduler(
                timed_func=schedule.timed_func,
                days_of_week=schedule.days_of_week,
                times_of_day=schedule.times_of_day,
                bot=bot,
                *schedule.args,
                **schedule.kwargs,
            )
        )


if __name__ == "__main__":
    configs = config_manager.load_configs()
    set_scheduled_functions()
    bot.run(configs["TOKEN"])
