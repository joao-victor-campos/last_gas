import discord 
import random, datetime, asyncio, requests
 

TOKEN = 'OTc5NTQ2MTI0NDcxODk4MTcy.GCfKmZ.qNjmi61tsHhKTqWEog2ro8dePaayxqX7dwGsyU'

client = discord.Client()

@client.event 
async def on_ready():
    print('último gás {0.user}'.format(client))


# @client.command 
async def schedule_daily_message():
    now = datetime.datime.now()
    # then = now + datetime.timedelta(days=1) 
    then = now.replace(hour=22, minute=19)
    wait_time = (then-now).total_sendods()
    await asyncio.sleep(wait_time)

    channel = client.get_chanell(338427143694581761)

    await channel.send("https://www.youtube.com/watch?v=OZpx3loLxg8")

client.run(TOKEN)