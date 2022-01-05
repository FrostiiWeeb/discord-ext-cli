import discord
from discord import AutoShardedClient
from discord.ext import commands
from .channel import CLIChannel
from aioconsole import ainput
from .utils import fancy_print, Response
import sys

class CLI(commands.Bot):
    def __init__(self, command_prefix, help_command=..., description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
        channel_id = options.pop("channel_id")
        receive_author = options.pop("receive_author", None)
        self.channel_id = channel_id
        self.receive_author = receive_author
        self.channel = CLIChannel(channel_id, bot=self)

    async def on_message(self, message : discord.Message):
        if self.receive_author:
            if message.author.id == self.receive_author:
                await fancy_print(f"[{message.author.name+'#'+message.author.discriminator}]: {message.content}", 0.5)
        await fancy_print(f"[{message.author.name+'#'+message.author.discriminator}]: {message.content}", 0.5)
        return await self.process_commands(message)

    async def send_prompt(self):
        await fancy_print("Would you like to start the cli? [y/n]", 0.10)
        data = await ainput()
        data = data.lower()
        if data == "y":
            return Response("YES")
        else:
            return Response("NO")

    async def run(self, token : str, **options):
        responses = ["YES", "NO"]
        data = await self.send_prompt()
        if data.response == responses[0]:
            await self.start(token, **options)
            while True:
                data = await ainput("[SERVER] Send a message: ")
                await self.channel.send(data)
        elif data.response == responses[1]:
            sys.exit(1)


class ShardedCLI(CLI, AutoShardedClient):
    pass
