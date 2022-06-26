from discord.ext import commands

from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers.time_scheduler import background_scheduler, SCHEDULES

config_manager = EnvVarConfigLoader()
bot = commands.Bot(command_prefix="$")


if __name__ == "__main__":
    configs = config_manager.load_configs()
    for schedule in SCHEDULES:
        bot.loop.create_task(
            background_scheduler(
                timed_func=schedule["timed_func"],
                day_of_week=schedule["day_of_week"],
                time_of_day=schedule["time_of_day"],
                bot=bot,
                *schedule["args"],
                **schedule["kwargs"],
            )
        )
    bot.run(configs["TOKEN"])
