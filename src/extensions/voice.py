"""TarkovBot's Voice Extension"""

# Built-in Modules
import asyncio
import io
import threading

# External Dependencies
from discord.ext import commands
import discord

# Local Modules
from src.bot import TarkovBot

__all__ = (
    "Voice",
)


class Voice(commands.Cog):
    def __init__(self, bot: TarkovBot):
        self.bot = bot

        self.sessions: dict[int, dict[int, discord.sinks.AudioData]] = {}  # {guild_id: {user_id: user_audio_data}}

    async def audio_data_monitor(self, ctx: discord.ApplicationContext, sink: discord.sinks.Sink) -> None:
        while True:
            # adding new or updated audio data instances to our session storage
            for uid, data in sink.audio_data.items():
                # data.file.seek(0)
                # print(data.file.read())
                print(data.file.getbuffer().nbytes)
                # instead of using a VAD, read the nbytes to determine if someone is speaking. i.e.: if the bytes
                # have not changed for ~0.1-2 seconds (figure out this interval at some point), then we can safely
                # assume the person is done talking and process the audio
                if guild_data := self.sessions.get(ctx.guild_id, False):
                    guild_data[uid] = data
                else:
                    self.sessions[ctx.guild_id] = {uid: data}

            # plan: (read above) to determine when a person has stopped speaking. once they have stopped speaking,
            # run speech recognition. if it amounts to nothing, clear the audio data. otherwise, use the recognized
            # text (with the bot identifier stripped) to query the tarkov.dev API.

    async def recording_end_callback(self, sink: discord.sinks.Sink):
        print(sink.audio_data)
        print(sink.__dict__)

    @commands.slash_command(name="start")
    async def start(self, ctx: discord.ApplicationContext) -> None:
        """Starts the TarkovBot's voice listening."""
        client: discord.VoiceClient = await ctx.author.voice.channel.connect()

        client.start_recording(
            sink := discord.sinks.WaveSink(),
            self.recording_end_callback,
        )

        write_mon = threading.Thread(
            target=asyncio.run,
            args=(self.audio_data_monitor(ctx, sink), ),
        )
        write_mon.start()
        #
        # await asyncio.sleep(5)
        #
        # client.stop_recording()


def setup(bot: TarkovBot) -> None:
    bot.add_cog(Voice(bot))
