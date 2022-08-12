"""TarkovBot's Tarkov API Searching Extension"""

# Built-in Modules
from datetime import datetime

# External Dependencies
from discord.ext import commands
import discord

# Local Modules
from src.bot import TarkovBot


__all__ = (
    "Tarkov",
)


class Tarkov(commands.Cog):
    def __init__(self, bot: TarkovBot):
        self.bot = bot

    @commands.slash_command(name="search")
    async def search_api(
        self,
        ctx: discord.ApplicationContext,
        item: discord.Option(
            str,
            description="The item to search for.",
            required=True,
        ),
    ) -> None:
        """Searches the tarkov.dev API for an item."""
        await ctx.defer()
        req = await self.bot.api.get_item_info(item)
        items = req['data']['items']
        item = items[0] if len(items) > 0 else None

        if item:
            embed = discord.Embed(
                title=item["name"], url=item["link"],
                color=0x000000,
                fields=[
                    discord.EmbedField(
                        name="Price", value=f"**{item['avg24hPrice']:,}₽**", inline=False,
                    ),
                    discord.EmbedField(
                        name="48hr Difference", value=f"**{item['changeLast48hPercent']}%**", inline=False,
                    ),
                ],
            )
            embed.set_thumbnail(url=item["iconLink"])
            embed.set_footer(
                text=f"Last updated @ {item['updated']}"
                     f" \u200B - \u200B "
                     f"Data provided by https://tarkov.dev"
            )
            await ctx.send_followup(embed=embed)
        else:
            await ctx.send_followup(
                embed=discord.Embed(
                    description="No items found!",
                    color=0x000000,
                )
            )


def setup(bot: TarkovBot) -> None:
    bot.add_cog(Tarkov(bot))
