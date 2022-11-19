import re
from typing import Any

from discord import Embed, Color, Client
from discord.ext import commands
from last_gas.domain.sources import Pelando


PELANDO_SOURCE = Pelando()


class PelandoPromosCog(commands.Cog):
    def __init__(self, bot: Client) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, _, err):
        print(err)

    @staticmethod
    async def pelando_promos(ctx: Any, *search_strings) -> None:
        """
        Returns a message with promos from Pelando website

        usage: $promos search_strings string [-limit of results]

        :param ctx: context object
        """
        if re.match(r"^\-[0-9]+", search_strings[-1]):
            limit = int(search_strings[-1][1:])
            search_strings = search_strings[:-1]
        else:
            limit = 5

        search_str = " ".join(search_strings)

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

    @commands.command()
    async def promos(self, ctx: Any, *search_strings) -> None:
        await PelandoPromosCog.pelando_promos(ctx, *search_strings)
