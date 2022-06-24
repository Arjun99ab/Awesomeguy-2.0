from secrets import randbelow
from discord.ext import commands
from discord.ext.commands import BucketType
import discord
from PIL import Image
from io import BytesIO
import requests
import json
import os


api_key = '55117ecc56c5742a942621ec406d8e5b'
color = 0xFF6500
key_features = {
    'temp' : 'Current Temperature',
    'feels_like' : 'Feels Like',
    'temp_min' : 'Minimum Temperature',
    'temp_max' : 'Maximum Temperature'
}

def parse_data(data):
    del data['humidity']
    del data['pressure']
    return data

def weather_message(data, location):
    location = location.title()
    message = discord.Embed(
        title=f'{location} Weather',
        description=f'This is the weather in {location}.',
        color=color
    )
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message

def error_message(location):
    location = location.title()
    return discord.Embed(
        title='Error',
        description=f"Some random error retrieving weather data for {location}. Can't really do anything about it, just state a more specific place.",
        color=color
    )


class WeatherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    async def weather(self, ctx, *, location1):
        location = location1.lower()
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
        try:
            data = parse_data(json.loads(requests.get(url).content)['main'])
            await ctx.send(embed=weather_message(data, location))
        except KeyError:
            await ctx.send(embed=error_message(location))

    

    


def setup(bot):
    bot.add_cog(WeatherCommand(bot))
