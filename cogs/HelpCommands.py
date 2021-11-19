from secrets import randbelow
from discord.ext import commands
import discord
from PIL import Image
from io import BytesIO
import requests
import json



def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(HelpCommands(bot))
