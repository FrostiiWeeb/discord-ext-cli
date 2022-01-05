import discord, typing
from discord.ext import commands

class CLIChannel():
    def __init__(self, channel_id, bot : typing.Union[commands.Bot, discord.AutoShardedClient, commands.AutoShardedBot] = None):
        self.data : typing.Any[discord.TextChannel] = None
        self.bot = bot
        self.channel_id = channel_id

    async def try_channel(self):
        data = self.bot.get_channel(self.channel_id)
        if not data:
            data = await self.bot.fetch_channel(self.channel_id)
        return data

    async def send(self, message : typing.AnyStr = None, **options):
        self.data = await self.try_channel()
        return await self.data.send(message, **options)