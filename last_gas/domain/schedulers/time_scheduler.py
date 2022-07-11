import asyncio
from datetime import datetime, timedelta
import discord
from typing import Any, Callable

from last_gas.domain.constants import CHANNEL_IDS
from assets.youtube_links import LINKS


def get_now_time() -> datetime:
    return datetime.utcnow() - timedelta(hours=3)


async def background_scheduler(
    timed_func: Callable,
    day_of_week: int = 0,
    time_of_day: str = "16:00:00",
    *timed_func_args,
    **timed_func_kwargs,
) -> None:
    """Waits in the background until the right time to run the desired command

    Args:
        timed_func (Callable): Function to be executed at the desired time.
        days_of_week (int, optional): Which day to run. Monday is 0. Defaults to 0.
        time_of_day (str, optional): Which time of day to run. Defaults to "16:00:00".
    """

    while True:
        now = get_now_time()
        current_day_of_week = now.weekday()
        desired_time_of_day = datetime.strptime(time_of_day, "%H:%M:%S").time()
        target_time = datetime.combine(now.date(), desired_time_of_day)
        if current_day_of_week == day_of_week and now < target_time:
            seconds_until_target = (target_time - now).total_seconds()
            print("Waiting %s seconds ..." % (seconds_until_target))
            await asyncio.sleep(seconds_until_target)
            await timed_func(*timed_func_args, **timed_func_kwargs)
        print("Waiting until next exec")
        await asyncio.sleep(60 * 60)


async def last_gas(bot: Any, channel_id: str) -> None:
    """Sends the "last gas" meme link to the channel

    Args:
        bot (Any): Discord bot
        channel_id (str): Channel id to send the message
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(LINKS["last_gas"])


async def sad_mondays(bot: Any, channel_id: str) -> None:
    """Sends the "John Kleber can't handle mondays" meme link to the channel

    Args:
        bot (Any): Discord bot
        channel_id (str): Channel id to send the message
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(file=discord.File("assets/images/john_kleber_monday.jpeg"))


async def ximira_xelo(bot: Any, channel_id: str) -> None:
    """Sends the "Ximira wants to stop working at 4pm on a Wednesday" meme link to the channel

    Args:
        bot (Any): Discord bot
        channel_id (str): Channel id to send the message
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(LINKS["ximira_xelo"])


SCHEDULES = [
    {
        "timed_func": last_gas,
        "day_of_week": 3,
        "time_of_day": "14:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
        },
    },
    {
        "timed_func": sad_mondays,
        "day_of_week": 0,
        "time_of_day": "09:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
        },
    },
    {
        "timed_func": ximira_xelo,
        "day_of_week": 2,
        "time_of_day": "16:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
        },
    },
]
