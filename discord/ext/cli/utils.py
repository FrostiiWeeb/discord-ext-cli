from aioconsole import aprint
import asyncio


class Response(object):
    def __init__(self, response : str) -> None:
        super().__init__()
        self.response = response
        
async def fancy_print(text, speed, newline=True):
    for letter in text:
        current_letter = 1
        await asyncio.sleep(speed)
        await aprint(letter, end="", flush=True)
        if current_letter == len(text):
            if newline:
                await aprint(end="")
        current_letter += 1