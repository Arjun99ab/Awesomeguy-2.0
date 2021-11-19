import os
from secrets import randbelow
import secrets
from PIL import Image
from io import BytesIO
import requests
import json
import time
import asyncio

from dotenv import load_dotenv

from discord import Message
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
import discord
from random import randint, choice
from itertools import islice

from datetime import datetime
from random import choice

from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption


intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

status = ['nothing', 'beta testing commands']


load_dotenv()
caillou_token = os.getenv("caillou_token")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    change_status.start()
    print(bot.user.name + ' has connected to Discord!')
    # await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('-help'))
    await bot.get_channel(847492628701511680).send("Bot is online")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Activity(type=discord.ActivityType.listening, name=choice(status)))


@bot.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def test(ctx):
    embed=discord.Embed(title="a")
    msg = await ctx.send(embed=embed)
    await msg.edit(content='Content Here', embed=None)


@bot.command()
async def guess(ctx):
    ch = ["1", "2", "3"]
    e = discord.Embed(title=f"{ctx.author}'s' Guessing Game!", description="> You haven't clicked on any button yet!",
                      color=0xFFEA00)

    e1 = discord.Embed(title=f"{ctx.author}, You Guessed It Right!", description="> You have won!", color=0x00FF00)

    e3 = discord.Embed(title=f"{ctx.author}, You didn't Click on Time", description="> Timed Out!",
                       color=discord.Color.red())

    e2 = discord.Embed(title=f"{ctx.author}, You Lost!", description="> You have lost!", color=discord.Color.red())

    m = await ctx.send(
        embed=e,
        components=[[Button(style=1, label="1"), Button(style=3, label="2"), Button(style=ButtonStyle.red, label="3")]
                    ],
    )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=15)
        if res.component.label == choice(ch):
            await m.edit(embed=e1, components=[], )
        else:
            await m.edit(embed=e2, components=[], )


    except TimeoutError:
        await m.edit(
            embed=e3,
            components=[],
        )



buttons = [
    [
        Button(style=ButtonStyle.grey, label='🗺️'),
        Button(style=ButtonStyle.grey, label='🡅'),
        Button(style=ButtonStyle.grey, label='🪓'),
        Button(style=ButtonStyle.grey, label=' ')
    ],
    [
        Button(style=ButtonStyle.blue, label='🡄'),
        Button(style=ButtonStyle.blue, label='🡇'),
        Button(style=ButtonStyle.blue, label='🡆'),
        Button(style=ButtonStyle.grey, label=' '),
        Button(style=ButtonStyle.grey, label='⏸️')
        
    ],
]
buttons1 = [
    [
        Button(style=ButtonStyle.grey, label='🔁'),
        Button(style=ButtonStyle.grey, label='🚫'),
        Button(style=ButtonStyle.grey, label='▶️'),
    ]
]

@bot.command()
async def button(ctx):

    await ctx.send(components=buttons, content="dab")

    while True:
        try:
            def check(res):
                return ctx.author == res.user and res.channel == ctx.channel

            res = await bot.wait_for("button_click", check=check, timeout=30)
            
            print(res.component.label)

            if res.component.label == "🡅":
                embed=discord.Embed(title="dab")
                await res.respond(embed=embed, type=7, components=buttons1)
            if res.component.label == "▶️":
                embed=discord.Embed(title="yrash")
                await res.respond(content="poggers", type=7, components=buttons, embed=())

        except asyncio.TimeoutError:
            print("exiting due to timeout")
            break


@bot.command()
async def select(ctx):
    test=[]
    test.append(SelectOption(label="Test", value="1", description="First", emoji='📖'))
    await ctx.send(
        "Hello, World!",
        components = [
            Select(placeholder="select something!", options=test) #description="", emoji=emoji
        ]
    )

    

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        interaction = await bot.wait_for("select_option", check=check, timeout=15)
        value = interaction.component

        print(value)
        print(type(value))

        embed=discord.Embed(title="test")
        await interaction.respond(content="", type=7, components=[], embed=embed)
    except TimeoutError:
        print("timed out")

    

@bot.command()
async def select1(ctx):
    await ctx.send(
        "Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="A"),
                    SelectOption(label="b", value="B"),
                ],
                custom_id="select1",
            )
        ],
    )
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel
    interaction = await bot.wait_for(
        "select_option", check=check
    )
    await interaction.send(content=f"{interaction.values[0]} selected!")






@bot.event
async def on_message(message):
    await bot.process_commands(message)

    msg = message.content


bot.run(caillou_token)
