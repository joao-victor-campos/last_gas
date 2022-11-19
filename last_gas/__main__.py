import asyncio
from typing import Any

import discord

from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers.time_scheduler import background_scheduler, SCHEDULES
from last_gas.domain.commands.promos import PelandoPromosCog
from last_gas.domain.commands.register_schedules import ScheduleCog


class LastGasBot(discord.ext.commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="$", intents=intents)

    async def on_ready(self) -> None:
        commands_synced = await self.tree.sync()
        print(f"{len(commands_synced)} commands")
        print("Bot started!")

    async def on_message(self, message: Any) -> None:
        if message.content.startswith("$"):
            print(f"Message from {message.author}: {message.content}")
        await self.process_commands(message)


async def main() -> None:
    bot = LastGasBot()
    config_manager = EnvVarConfigLoader()
    configs = config_manager.load_configs()

    # Set commands
    await bot.add_cog(PelandoPromosCog(bot))
    await bot.add_cog(ScheduleCog(bot))

    # Set background tasks
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

    # Start bot
    await bot.start(configs["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
