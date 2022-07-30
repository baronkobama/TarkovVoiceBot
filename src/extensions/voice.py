"""TarkovBot's Voice Extension"""

# Built-in Modules

# External Dependencies
from discord.ext import commands

# Local Modules
from src.bot import TarkovBot


class Voice(commands.Cog):
    def __init__(self, bot: TarkovBot):
        self.bot = bot


def setup(bot: TarkovBot):
    bot.add_cog(Voice(bot))
