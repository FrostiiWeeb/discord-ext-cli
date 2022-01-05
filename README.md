# discord.ext.cli

A basic CLI to talk to a channel with terminal.

Example:
```py
from discord.ext.cli import CLI

bot = CLI(command_prefix="$", channel_id=381383689470984003)

bot.run("Nzg0KTIyMDYxMjE5OTU0LzA4.X8kskw.bqfFDZGfNPv41jUqJ9DF8TFxq1w")
```