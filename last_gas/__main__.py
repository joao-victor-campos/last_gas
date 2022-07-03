import re
from discord import Embed, Color
from discord.ext import commands

from last_gas.adapters import EnvVarConfigLoader
from last_gas.domain.schedulers.time_scheduler import background_scheduler, SCHEDULES
from last_gas.domain.sources import Pelando

config_manager = EnvVarConfigLoader()
bot = commands.Bot(command_prefix="$")


@bot.command()
async def promos(ctx, *search):
    """
    Returns a message with promos from Pelando website

    usage: $promos search string [-limit of results]

    :param ctx: context object
    """
    if re.match(r"^\-[0-9]+", search[-1]):
        limit = int(search[-1][1:])
        search = search[:-1]
    else:
        limit = 5

    search_str = " ".join(search)

    source = Pelando()

    # Check assets -> pelando_schema.graphql
    columns = [
        "title",
        "price",
        "temperature",
        "discountFixed",
        "discountPercentage",
        "sourceUrl",
        "image{url}",
        "store{name}",
        "couponCode",
    ]

    offers = source.search_offers(
        search=search_str,
        columns=columns,
        limit=limit,
    )

    for offer in offers:
        card = Embed(
            title=offer["title"],
            description=offer["store"]["name"],
            url=offer["sourceUrl"],
            color=Color.green(),
        )

        value_description = Pelando.get_value_description(offer)

        card.set_thumbnail(url=offer["image"]["url"])
        card.add_field(
            name=value_description, value=f"❄️ {int(offer['temperature'])}° 🔥"
        )

        if offer["couponCode"]:
            card.add_field(name="Cuponzin 🤑", value=offer["couponCode"])

        await ctx.send(embed=card)


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
