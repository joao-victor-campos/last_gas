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


async def send_link(bot: Any, channel_id: str, link_name: str) -> None:
    """Sends a link to to a channel

    Args:
        bot (Any): Discord bot
        channel_id (str): Channel id to send the message
        link_name (str): The key for the link in LINKS
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(LINKS[link_name])


async def send_file(bot: Any, channel_id: str, file_path: str) -> None:
    """Sends a file to a channel

    Args:
        bot (Any): Discord bot
        channel_id (str): Channel id to send the message
        file_path (str): Path to file
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(file=discord.File(file_path))


SCHEDULES = [
    {
        "timed_func": send_link,
        "day_of_week": 3,
        "time_of_day": "11:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": LINKS["last_gas"],
        },
    },
    {
        "timed_func": send_file,
        "day_of_week": 0,
        "time_of_day": "09:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
            "file_path": "assets/images/john_kleber_monday.jpeg",
        },
    },
    {
        "timed_func": send_link,
        "day_of_week": 2,
        "time_of_day": "16:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": LINKS["ximira_xelo"],
        },
    },
    {
        "timed_func": send_link,
        "day_of_week": 4,
        "time_of_day": "17:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": LINKS["del_rey"],
        },
    },
    {
        "timed_func": send_link,
        "day_of_week": 0,
        "time_of_day": "11:00:00",
        "args": [],
        "kwargs": {
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": LINKS["bom_dia_pedrin"],
        },
    },
]
