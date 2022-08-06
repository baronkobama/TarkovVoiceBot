"""TarkovBot's Main Bot Class"""

# Built-in Modules
from datetime import datetime
import json
import os
import platform

# External Dependencies
import discord
import dotenv

# Local Modules


class TarkovBot(discord.Bot):
    def __init__(self):
        self.__version__ = "1.0.0"

        dotenv.load_dotenv()

        intents = discord.Intents.default()
        intents.members = True  # noqa

        super().__init__(
            debug_guilds=json.loads(os.getenv("DEBUG_GUILDS")),
            intents=intents,
        )

    # --- Bot Launch Functions ---

    def _startup(self) -> None:
        print("> ------------------------")
        print("> ----<TarkovVoiceBot>----")
        print("> ------------------------")
        print("> --------Sys Info--------")
        print(f"> Working Directory: {os.getcwd()}")
        print(f"> System Versioning: {platform.system()} {platform.release()} ({os.name})")
        print(f"> Python Version: {platform.python_version()}")
        print(f"> Py-cord Version: {discord.__version__}")
        print("> --------Bot Info--------")

        loaded = self.load_extension("src.extensions", recursive=True, store=True)

        for ext in sorted(loaded.items()):
            if ext[1] is not True:
                print(f"> Failed to Load Extension: {ext[0]}\n> Exception: {ext[1]}")
            else:
                print(f"> Loaded Extension: {ext[0]}")

    def run(self) -> None:
        """Runs local startup and then runs the bot w/ reconnection logic."""
        self._startup()

        try:
            super().run(os.getenv("TOKEN"), reconnect=True)
        except discord.LoginFailure:
            print("> Invalid token, please set a valid token in .env...")
            exit(-1)

    # --- Connection Event Monitors ---

    async def on_connect(self) -> None:
        await super().on_connect()
        print(f"> Connected to Discord - latency: {self.latency * 1000:,.0f} ms"
              f" - [{datetime.now().strftime('%H:%M:%S')}]")

    async def on_ready(self) -> None:
        print(f"> Tarkov Bot Version: v{self.__version__}")
        print("> Author: baronkobama#1157")
        print(f"> Intent Value: {self.intents.value}")
        print(f"> Name: {self.user.name}#{self.user.discriminator}")
        print(f"> ID: {self.user.id}")
        print(f"> Bot Online as of: {datetime.now().strftime('%H:%M:%S')}")
        print("> ------------------")
        await self.change_presence(activity=discord.Game("wit dat Tarky API >:)"), status=discord.Status.idle)

    @staticmethod
    async def on_disconnect() -> None:
        print(f"> Disconnected from Discord - [{datetime.now().strftime('%H:%M:%S')}]")

    async def on_resumed(self) -> None:
        print(f"> Reconnected to Discord - latency: {self.latency * 1000:,.0f} ms"
              f" - [{datetime.now().strftime('%H:%M:%S')}]")

    # --- General Event Monitors/Listeners ---

    async def on_guild_join(self, guild: discord.Guild) -> None:
        print(f"> Joined a new guild [{guild.name} - {guild.id}] as "
              f"{self.user.name}#{self.user.discriminator} with UID of {self.user.id}!")

    # --- Command Processing/Handling ---

    async def on_interaction(self, interaction: discord.Interaction) -> None:
        if not interaction.user.bot:
            await self.process_application_commands(interaction)
