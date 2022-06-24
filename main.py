

from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio

TOKEN = 'OTc5NTQ2MTI0NDcxODk4MTcy.GCfKmZ.qNjmi61tsHhKTqWEog2ro8dePaayxqX7dwGsyU'
bot = commands.Bot(command_prefix="$")
WHEN = time(1, 27, 0)  # 1:29 PM UTC
channel_id = 338427143694581761 

async def called_once_a_week():  
    await bot.wait_until_ready() 
    channel = bot.get_channel(channel_id) 
    await channel.send("https://www.youtube.com/watch?v=OZpx3loLxg8")

async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  
        nextweek = datetime.combine(now.date() + timedelta(days=7), time(0))
        seconds = (nextweek - now).total_seconds()  
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_week()  # Call the helper function that sends the message
        nextweek = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (nextweek - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration


if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(TOKEN)