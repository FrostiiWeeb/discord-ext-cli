from aioconsole.stream import aprint
import discord
from discord import AutoShardedClient
from discord.ext import commands
from .channel import CLIChannel
from aioconsole import ainput
from .utils import fancy_print, Response
import sys, asyncio, time

class CLI(commands.Bot):
    def __init__(self, command_prefix, description=None, **options):
        super().__init__(command_prefix, description=description, **options)
        channel_id = options.pop("channel_id")
        receive_author = options.pop("receive_author", None)
        self.channel_id = channel_id
        self.receive_author = receive_author
        self.channel = CLIChannel(channel_id, bot=self)
        self._message_printing = False
        self._timeout = False
        self.started = False

    async def wait_until(self, delegate, timeout: int):
        end = time.time() + timeout
        while time.time() < end:
            if delegate():
                return True
            else:
                while True:
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
                    if delegate():
                        return True
                    await asyncio.sleep(5)
            return False

    def check(self):
        self._message_printing != True

    async def on_message(self, message : discord.Message):
        if message.channel.id == self.channel_id:
            if self._message_printing:
                await self.wait_until(self.check, 60)
            self._message_printing = True
            if message.author.bot:
                return await self.process_commands(message)
            if self.receive_author:
                if message.author.id == self.receive_author:
                    await fancy_print(f"[{message.author.name+'#'+message.author.discriminator}]: {message.content}\n", 0.2)
                    await self.send_message_prompt(message)
                    self._message_printing = False
            else:
                await fancy_print(f"[{message.author.name+'#'+message.author.discriminator}]: {message.content}\n", 0.2)
                await self.send_message_prompt(message)
                self._message_printing = False
        return await self.process_commands(message)

    async def send_prompt(self):
        await fancy_print("Would you like to start the cli? [y/n] ", 0.10)
        data = await ainput()
        data = data.lower()
        if data == "y":
            return Response("YES")
        else:
            return Response("NO")
    
    async def send_message_prompt(self, message : discord.Message):
        data = await ainput("[SERVER] Send a message: ")
        if data == "reply":
            id = await ainput("Send the message id to wich you want to reply to. ")
            id = int(id)
            content = await ainput("[SERVER] Send the content you want to reply with. ")
            msg = await message.channel.fetch_message(id)
            return await msg.reply(content)
        await self.channel.send(data)

    async def _start(self, token : str, **options):
        responses = ["YES", "NO"]
        data = await self.send_prompt()
        if data.response == responses[0]:
            await self.start(token, **options)
            await self.send_message_prompt()
        elif data.response == responses[1]:
            sys.exit(1)

    def run(self, token, **options):
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._start(token, **options))


class ShardedCLI(CLI, AutoShardedClient):
    pass
