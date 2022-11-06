import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
import discord
from discord.ext.commands import Bot
from typing import Any, Callable, Dict, List, Optional

from last_gas.domain.commands.promos import pelando_promos
from last_gas.domain.constants import CHANNEL_IDS
from assets.youtube_links import LINKS


@dataclass(frozen=True)
class ScheduleData:
    timed_func: Callable
    times_of_day: List[str]
    args: List[Any]
    kwargs: Dict[str, Any]
    days_of_week: Optional[List[int]] = None


def get_now_time() -> datetime:
    return datetime.utcnow() - timedelta(hours=3)


def get_next_valid_execution_time(now: datetime, allowed_times: List[str]) -> datetime:
    """Get next eligible time for running. If none is eligible, returns None."""

    for time_of_day in allowed_times:
        desired_time_of_day = datetime.strptime(time_of_day, "%H:%M:%S").time()
        target_time = datetime.combine(now.date(), desired_time_of_day)
        if now < target_time:
            return target_time
    return None


async def background_scheduler(
    timed_func: Callable,
    times_of_day: List[str],
    days_of_week: List[int] = None,
    *timed_func_args,
    **timed_func_kwargs,
) -> None:
    """Waits in the background until the right time to run the desired command

    Args:
        timed_func (Callable): Function to be executed at the desired time.
        times_of_day (str, optional): Which time of day to run. Defaults to "16:00:00".
        days_of_week (List[int], optional): Which days to run. If no days are set,
        the command runs every day. Monday is 0. Defaults to None.
    """

    days_of_week = days_of_week or range(7)
    while True:
        now = get_now_time()
        current_day_of_week = now.weekday()
        target_time = get_next_valid_execution_time(now, times_of_day)
        if current_day_of_week in days_of_week and target_time:
            seconds_until_target = (target_time - now).total_seconds()
            print("Waiting %s seconds ..." % (seconds_until_target))
            await asyncio.sleep(seconds_until_target)
            await timed_func(*timed_func_args, **timed_func_kwargs)
        print("Waiting until next exec")
        await asyncio.sleep(60 * 60)


async def send_link(bot: Bot, channel_id: str, link_name: str) -> None:
    """Sends a link to to a channel

    Args:
        bot (Bot): Discord bot
        channel_id (str): Channel id to send the message
        link_name (str): The key for the link in LINKS
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(LINKS[link_name])


async def send_file(bot: Bot, channel_id: str, file_path: str) -> None:
    """Sends a file to a channel

    Args:
        bot (Bot): Discord bot
        channel_id (str): Channel id to send the message
        file_path (str): Path to file
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(file=discord.File(file_path))


async def send_pelando_promos(
    bot: Bot, channel_id: str, search_list: List[str]
) -> None:
    """Send pelando promos to a channel

    Args:
        bot (Bot): Discord bot
        channel_id (str): Channel id to send the message
        search_list (List[str]): Keywords to search in pelando API
    """

    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(
        content=f"Searching promos for keywords: {', '.join(search_list)}"
    )
    await pelando_promos(channel, *search_list)


SCHEDULES = [
    ScheduleData(
        timed_func=send_link,
        days_of_week=[3],
        times_of_day=["11:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": "last_gas",
        },
    ),
    ScheduleData(
        timed_func=send_file,
        days_of_week=[0],
        times_of_day=["09:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["geralt"],
            "file_path": "assets/images/john_kleber_monday.jpeg",
        },
    ),
    ScheduleData(
        timed_func=send_link,
        days_of_week=[2],
        times_of_day=["16:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": "ximira_xelo",
        },
    ),
    ScheduleData(
        timed_func=send_link,
        days_of_week=[4],
        times_of_day=["17:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": "del_rey",
        },
    ),
    ScheduleData(
        timed_func=send_link,
        days_of_week=[0],
        times_of_day=["11:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["geralt"],
            "link_name": "bom_dia_pedrin",
        },
    ),
    # Show G29 promos
    ScheduleData(
        timed_func=send_pelando_promos,
        times_of_day=["10:00:00", "18:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["bot_promos"],
            "search_list": ["g29"],
        },
    ),
    # Show oculus quest promos
    ScheduleData(
        timed_func=send_pelando_promos,
        times_of_day=["10:00:00", "18:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["bot_promos"],
            "search_list": ["oculus quest 2"],
        },
    ),
    # Show headsets promos
    ScheduleData(
        timed_func=send_pelando_promos,
        times_of_day=["10:00:00", "18:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["bot_promos"],
            "search_list": ["headset"],
        },
    ),
        ScheduleData(
        timed_func=send_pelando_promos,
        times_of_day=["10:00:00", "18:00:00"],
        args=[],
        kwargs={
            "channel_id": CHANNEL_IDS["bot_promos"],
            "search_list": ["buds 2 pro"],
        },
    ),
]
