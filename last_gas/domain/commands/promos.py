import re

from discord import Embed, Color
from last_gas.domain.sources import Pelando


PELANDO_SOURCE = Pelando()


async def pelando_promos(ctx, *search):
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
        "status",
    ]

    offers = PELANDO_SOURCE.search_offers(
        search=search_str,
        columns=columns,
        limit=limit,
    )

    cards = []
    for offer in offers:
        if offer["status"] == "ACTIVE":
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

            cards.append(card)

    if len(cards) > 0:
        for card in cards:
            await ctx.send(embed=card)
    else:
        await ctx.send(content="Nada nessa porra <:TRUCO:729720154866450553>")
