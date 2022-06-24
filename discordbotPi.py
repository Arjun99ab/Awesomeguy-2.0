from collections import UserList
import os
from secrets import randbelow
import secrets
from PIL import Image
from io import BytesIO
from discord.ext.commands.errors import CommandInvokeError
import requests
import json
import time
from discord.ext import commands, tasks
import discord
from random import randint, choice
from dotenv import load_dotenv
from itertools import islice
#from prsaw import RandomStuff
from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption
import asyncio
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import BucketType
from asyncdagpi import Client, ImageFeatures
from discord.utils import get
import aiohttp
from kasa import SmartPlug, SmartBulb
import webbrowser
import sys
import pymongo
from copy import deepcopy
from pymongo import MongoClient
import copy
import io
import aiohttp
import discord
import datetime
import warnings
from discord.ext import commands


plug = SmartPlug("192.168.1.214")
bulb = SmartBulb("192.168.1.217")

load_dotenv()
awesomeguy_token = os.getenv('awesomeguy_token')
mongo_cluster = os.getenv('mongo_cluster')

player1 = ""
player2 = ""

intents = discord.Intents.default()
intents.members = True
intents.presences = True


bot=commands.AutoShardedBot(command_prefix='-', intents=intents)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)
bot.session = aiohttp.ClientSession()

cluster = MongoClient(mongo_cluster)
db = cluster["AwesomeguyTwoPointO"]


def giveXP(id, xp):
    added_xp = int(xp)
    user_id = int(id)
    collection = db["rank"]
    #check if member is in the databse
    current_xp = None
    member_stats = collection.find({"_id": user_id})
    for stat in member_stats:
        current_xp = stat["xp"]
    #if they're not, create one for them
    if current_xp == None:
        rank_info = {"_id": user_id, "xp": 0}
        collection.insert_one(rank_info)
        print("added!")
        current_xp = 0
    #update their info
    collection.update_one({"_id": user_id}, {"$inc": {"xp": added_xp}})

global game_in_session
global minecraft_in_session
minecraft_in_session = False
game_in_session = False
global x1
global y1
global x2
global y2
x1 = 1
y1 = 2
x2 = 2
y2 = 2
global deleteTrue
deleteTrue = False

def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)

def valuesList(dictionary: dict):
    stringValues = str(dictionary.values())
    substringStringValues = stringValues[13:len(stringValues)-2]
    sentenceValues = substringStringValues.split(', ')

    return(sentenceValues)


def keysList(dictionary: dict):
    stringKeys = str(dictionary.keys())
    substringStringKeys = stringKeys[12:len(stringKeys)-3]
    sentenceKeys = substringStringKeys.split("', '")

    return(sentenceKeys)


######################################################################
#                       Bot and User Startup Commands                #
######################################################################

status = ['-help', '-duel', 'absolutely nothing', 'gcodes', '-help']



@bot.event
async def on_ready():
    DiscordComponents(bot)
    
    change_status.start()
    print(bot.user.name + ' has connected to Discord!')
    embed=discord.Embed(title="Bot is online", color=discord.Color.purple())
    await bot.get_user(743819073917550682).send(embed=embed) #me
    await bot.get_channel(847492628701511680).send(embed=embed) #channel

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=choice(status)))

frost_role = "unverified boi"
acsl_role = "gamer"

@bot.event
async def on_member_join(member):
    if member.guild.id == 882431857264828436:
        embed = discord.Embed(title="Welcome to " + str(member.guild.name) + "!", description='Go to welcome and verify to get verified, and after go to roles to assign yourself to some roles.', color=discord.Color.blue())
        await member.send(embed=embed)
        role = discord.utils.get(member.guild.roles, name=frost_role)
        await member.add_roles(role)
        print(f"{member} was given {role}")
        embed=discord.Embed(title="Member Joined", description=f"{member.name}#{member.discriminator} has joined the server.\nUse -verify {member.name}#{member.discriminator} to automatically verify them.", color=discord.Color.purple())
        await bot.get_channel(883781331086090300).send(embed=embed) #channel
        await bot.get_channel(883781331086090300).send(f"**Copy this:**\n{member.name}#{member.discriminator}")
    if member.guild.id == 886619114557304833:
        role = discord.utils.get(member.guild.roles, name=acsl_role)
        await member.add_roles(role)
        print(f"{member} was given {role}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def verify(ctx, member: discord.Member = None):
    if ctx.guild.id == 939323947906920509:
        verified_role = discord.utils.get(ctx.guild.roles, name="Blair")
        if member is not None:
            try:
                if verified_role not in member.roles:
                    await member.add_roles(verified_role)
                    embed=discord.Embed(title=f"You have been successfully verified in {member.guild.name}!", color=discord.Color.green())
                    await bot.get_user(member.id).send(embed=embed)
                    embed=discord.Embed(title=f"{member.display_name} has been successfully verified!", color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"{member.display_name} is already verified.", color=discord.Color.purple())
                    await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="Format: '-verify @Person'", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Format: '-verify @Person'", color=discord.Color.red())
            await ctx.send(embed=embed)
    if ctx.guild.id == 882431857264828436:
        unverified_role = discord.utils.get(ctx.guild.roles, name="unverified boi")
        verified_role = discord.utils.get(ctx.guild.roles, name="verified")
        if member != None:
            try:
                if unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                    await member.add_roles(verified_role)
                    embed=discord.Embed(title=f"You have been successfully verified in {member.guild.name}!", color=discord.Color.green())
                    await bot.get_user(member.id).send(embed=embed)
                    embed=discord.Embed(title=f"{member.display_name} has been successfully verified!", color=discord.Color.green())
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"{member.display_name} is already verified.", color=discord.Color.purple())
                    await ctx.send(embed=embed)

            except:
                embed=discord.Embed(title="Format: '-verify @Person'", color=discord.Color.red())
                await ctx.send(embed=embed)
        elif member == None:
            try:
                msg = ctx.message.reference
            except AttributeError:
                await ctx.send("Format: '-verify @Person'")
                return
            
            member = msg.author
            print(member)
            if unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                    await member.add_roles(verified_role)
                    embed=discord.Embed(title="You have been successfully verified!", color=discord.Color.green())
                    await bot.get_user(member.id).send(embed=embed)
                    embed=discord.Embed(title=f"{member.display_name} has been successfully verified!", color=discord.Color.green())
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"{member.display_name} is already verified.", color=discord.Color.purple())
                await ctx.send(embed=embed)

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title="You don't have perms bruv", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.event
async def on_member_leave(member):
    await member.send("Imagine leaving rip")
    print("sent message to " + member)



async def timeout_user(*, user_id: int, guild_id: int, until, removing: False):
    json1 = {'communication_disabled_until'}
    print(json1)
    headers = {"Authorization": f"Bot {bot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    if not removing:
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
        json = {'communication_disabled_until': timeout}
    else:
        json = {'communication_disabled_until': None}
    print(json)
    async with bot.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
            return True
        return False

global admin_list2
admin_list2 = []

@bot.command(aliases=['tm'])
async def timeout(ctx, member: discord.Member, duration = None):
    if ctx.message.author.guild_permissions.administrator:
        unit = duration[-1]
        print(unit)
        amount = int(duration[:-1])
        print(amount)
        
        if unit == "m":
            wait = 1 * amount
        elif unit == "h":
            wait = 60 * amount
        elif unit == "d":
            wait = 1440 * amount
        if ctx.guild.id == 882431857264828436: #FROST SERVER
            global admin_list2
            admin_role = discord.utils.get(ctx.guild.roles, id=882435188787916851)
            owner_role = discord.utils.get(ctx.guild.roles, id=883170021407350844)
            
            if owner_role in ctx.author.roles and admin_role in member.roles:
                await member.remove_roles(admin_role)
                admin_list2.append(member)
                handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=wait, removing=False)

                if handshake:
                    embed = discord.Embed(title="Timeout", description=f"{member.mention} is now in timeout for {amount}{unit}.", colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                    await asyncio.sleep()
                else:
                    embed = discord.Embed(title="Error", description="Discord api is either exploding or my bot is.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            elif admin_role in ctx.author.roles and admin_role not in member.roles:
                handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=wait, removing=False)

                if handshake:
                    embed = discord.Embed(title="Timeout", description=f"{member.mention} is now in timeout for {amount}{unit}.", colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Error", description="Discord api is either exploding or my bot is.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="You don't have permissions to timeout people.", color=discord.Color.red())
                await ctx.send(embed=embed)
            
        
        else:
            handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=wait, removing=False)

            if handshake:
                embed = discord.Embed(title="Timeout", description=f"{member.mention} is now in timeout for {amount}{unit}.", colour=discord.Colour.purple())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description=f"Discord api is either exploding or my bot is.", color=discord.Color.red())
                await ctx.send(embed=embed)

@bot.command(aliases=['untm'])
async def untimeout(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        if ctx.guild.id == 882431857264828436: #FROST SERVER
            if member in admin_list2:
                handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=0, removing=True)
                if handshake:
                    embed = discord.Embed(title="Timeout", description=f"{member.mention} was removed from their timeout.", colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                    await member.add_roles(discord.utils.get(ctx.guild.roles, id=882435188787916851))
                    admin_list2.remove(member)
                else:
                    embed = discord.Embed(title="Error", description=f"Discord api is either exploding or my bot is.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=0, removing=True)
                if handshake:
                    embed = discord.Embed(title="Timeout", description=f"{member.mention} was removed from their timeout.", colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Error", description=f"Discord api is either exploding or my bot is.", color=discord.Color.red())
                    await ctx.send(embed=embed)
        else:
            handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=0, removing=True)
            if handshake:
                embed = discord.Embed(title="Timeout", description=f"{member.mention} was removed from their timeout.", colour=discord.Colour.purple())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description=f"Discord api is either exploding or my bot is.", color=discord.Color.red())
                await ctx.send(embed=embed)

######################################################################
#                       Bot Testing Commands                         #
######################################################################
@bot.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')

@slash.slash(name="dapmeup", description="daps you up!!", guild_ids=[917917980938096670, 882431857264828436, 809070827076976644, 939323947906920509])
async def _dap(ctx: SlashContext):
    embed = discord.Embed(title="ON GODDD DAP ME UP THIS INSTANT", description=f"*daps* {ctx.author.mention}", color=discord.Color.purple())
    await ctx.send(embed=embed)

@bot.command()
async def testdm(ctx):
    print(ctx.author)
    print(type(ctx.author))
    await ctx.author.send("test message")

@bot.command()
async def amogus(ctx):
    await ctx.send(file=discord.File('amogus.mp4'))

@bot.command()
async def die(ctx):
    if ctx.author.id == 743819073917550682:
        await ctx.send("offline")
        sys.exit()
    else:
        await ctx.send("shut up jason")

@bot.command()
async def restart(ctx):
    if ctx.author.id == 743819073917550682:
        await ctx.send("restarting")
        exec(open("discordbotPi.py").read())
        time.sleep(5)
        sys.exit()
    else:
        await ctx.send("no u")




    



@bot.group(invoke_without_command=True)
async def plug():
    print("plug")

@plug.command()
async def on(ctx):
    try:

        if ctx.author.id == 743819073917550682 or ctx.author.id == 764256343393304597:
            await plug.update()
            print(plug.alias)

            await plug.turn_on()
            embed = discord.Embed(title="Printer Light is **ON**", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have permission to use this command")
    except SmartDeviceException:
        await ctx.send("device not plugged in")


@plug.command()
async def off(ctx):
    print(ctx.author.id, "trash")
    if ctx.author.id == 743819073917550682 or ctx.author.id == 764256343393304597:
        await plug.update()
        print(plug.alias)
        await plug.turn_off()
        embed = discord.Embed(title="Printer Light is **OFF**", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to use this command")


@bot.group(invoke_without_command=True)
async def light():
    print("light")
    

global lightrgb
lightrgb = False

@light.command()
async def normal(ctx):
    if ctx.author.id == 743819073917550682:
        global lightrgb
        
        await bulb.update()
        await bulb.set_brightness(100)
        await bulb.set_hsv(0, 0, 100)
        await bulb.set_color_temp(5500)
        embed = discord.Embed(title="Room Light in **NORMAL** mode", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to use this command")

@light.command()
async def rgb(ctx):
    if ctx.author.id == 743819073917550682:
        await bulb.update()
        print(bulb.alias)
        embed = discord.Embed(title="Room Light in RGB mode", color=discord.Color.green())
        await ctx.send(embed=embed)
        x = 0
        rgb = True
        while x < 361:
            await bulb.set_hsv(x, 100, 80)
            await bulb.update()
            x = x + 1
            if x == 361:
                x = 0
    else:
        await ctx.send("You don't have permission to use this command")

@rgb.error
async def rgb_light_error(ctx, error):
    print(error)
    if isinstance(error, RuntimeError):
        print("when it goes from RGB to Normal, this allows it to pass without error")

@light.command()
async def dim(ctx):
    if ctx.author.id == 743819073917550682:
        await bulb.update()
        print(bulb.alias)
        current_brightness = bulb.brightness
        await bulb.set_brightness(current_brightness-10)
        embed = discord.Embed(title="Room Light dimmed by 10 percent", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to use this command")
@light.command()
async def bright(ctx):
    if ctx.author.id == 743819073917550682:
        await bulb.update()
        print(bulb.alias)
        current_brightness = bulb.brightness
        await bulb.set_brightness(current_brightness+10)
        embed = discord.Embed(title="Room Light dimmed by 10 percent", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to use this command")


@light.command()
async def info(ctx):
    if ctx.author.id == 743819073917550682:
        await bulb.update()
        print(bulb.alias)
        print(type(bulb.state_information))
        embed = discord.Embed(title="Light Info", color=discord.Color.blue())
        info_keys = keysList(bulb.state_information)
        info_values = valuesList(bulb.state_information)
        print(bulb.state_information)
        print(info_keys)
        print(info_values)
        i = 0
        while i < len(bulb.state_information):
            name = info_keys[i]
            value = info_values[i]
            embed.add_field(name=name, value=value, inline=True)
            i = i + 1
        embed.add_field(name=name, value=value, inline=True)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to use this command")




######################################################################
#                       Help and Updatelog Commands                  #
######################################################################

@bot.group(invoke_without_command=True)
async def music():
    pass

@music.command()
async def help(ctx):
    embed=discord.Embed(title="Music Commands", description="**connect:** Connects to vc\n**disconnect:** Disconnects from vc\n**play <song>:** Plays a specific song\n**skip:** Skips current song\n**pause:** Pauses current song\n**resume:** Resumes song\n**seek <seconds> [reverse=False]:** Jumps to specific part of song\n**!volume <vol> [forced=False]:** Adjusts volume (1 - 100)\n**loop [type]:** Loops song, (none, current, queue)\n**np:** Shows the status of the current song\n**queue:** Displays all songs in the queue\n**equalizer:** Adjusts equalizer for song", color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Use the '-' prefix before every command.\nCheck how laggy the bot is with '-ping'!", color=discord.Color.blue())
    embed.add_field(name="Rank Commands", value="-rank, -rank @User, -lb, -lb global", inline=False)
    embed.add_field(name="Fun Commands", value="-inspire, -dm @User, -random, -flip, -roll, -urban {word}, -wanted @User", inline=False)
    embed.add_field(name="Game Commands", value="-minecraft, -tictactoe, -rps, -guess, -duel" + "\n" + "**Look below to find more about these**", inline=False)
    embed.add_field(name="Help Commands", value="-minecraft help, -tictactoe help, -rps help, -guess help, -duel help, -roles help", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def updatelog(ctx):
    embed = discord.Embed(title="Awesomeguy 2.0 Update Log", description="Hello this is where I'll be posting updates even though no one will read this.", color=discord.Color.blue())
    embed.add_field(name="v1.7.0", value="Yep skipping to 1.7.0 cuz progress is very good, item prices and dmg balanced, and quit command and cool stuff yay")
    embed.add_field(name="v1.6.4 and v1.6.5", value="First iteration of the duel commands done, its probably very buggy but is the baseline and stuff and stuff ok bye")
    embed.add_field(name="v1.6.3", value="Ok I added heal pots, I'll actually start working on the game now that all the fundamentals are down.")
    embed.add_field(name="v1.6.2", value="Ok I actually became smart and completely fixed the XP, items, and giving stuff commands and stuff now **I need ideas for weapon names.**")
    embed.add_field(name="v1.6.1", value="Completely failed working on the duel gamemode shop and items setup lol")
    embed.add_field(name="v1.6.0", value="Rank system added to all gamemodes, RPS, guess the number, and TicTacToe.")
    embed.add_field(name="v1.5.8 and v1.5.9", value="Work on duel gamemode, with buying stuff and stuff and stuff. Cool ok bye")
    embed.add_field(name="v1.5.7", value="Experimenting with cogs to make code more efficient and cleaner. Some minor ping adjustments, and implemented slash commands.")
    embed.add_field(name="v1.5.6", value="Completely fixed rank system. Now I'll be able to more easily implement the rank system into gamemodes")
    embed.add_field(name="v1.5.5", value="Guess the number command is online just use -guess it might be a little broken bc first time im using bot.wait_for method ok bye")
    embed.add_field(name="v1.5.4", value="Started working on 'guess the number' command")
    embed.add_field(name="v1.5.3", value="Some text based projects blah blah blah yes im not doing any work why idk")
    embed.add_field(name="v1.5.2", value="Testing with PIL library ill prob make some pokemon thing other than that nothing ok bye")
    embed.add_field(name="v1.5.1", value="K i did some stuff thats about it good day")
    embed.add_field(name="v1.5.0", value="Yes v.1.5.0 but no one reads these insane. Cleaned up a ton of code and experimented with buttons, events, and image processing. Reaction roles and join roles are now here as well as some image roles. Lastly, the bot will be running 24/7 unless something explodes. I'm working on a couple different things, so the next big game/system might be a bit. ok goodbye")
    embed.add_field(name="v1.4.9", value="Added -wanted command allowing to make someones pfp in a wanted poster or yours. More 'fun' image commands coming in the future.")
    embed.add_field(name="v1.4.8", value="Added -addrole and -removerole, pretty self explanatory. Also tried to implement ranking system into TicTacToe but I don't have enough testing to confirm whether it works, it 100% does't. Might continue it in the future when I have time and an alt account")
    embed.add_field(name="v1.4.7", value="Added additional ending messages and reworked a part of TicTacToe logic.")
    embed.add_field(name="v1.4.65", value="Removed 'bruh' response by majority vote")
    embed.add_field(name="v1.4.6", value="Created and updated this, the update log.")
    embed.add_field(name="v1.4.5", value="Updated TicTacToe game, allowing faster gameplay and optimization for printing, as well as added commands to avoid errors.")
    embed.add_field(name="v1.4.4", value="Removed the '-minecraft' command as no one uses it and its really crap anyways. If you want it back just ping me.")
    embed.add_field(name="1.4.3", value="Broke the code somehow but then I fixed it so idk")
    embed.add_field(name="v1.4.2", value="Modified '-rps' to actually work")
    embed.add_field(name="v1.4.1", value="Cleaned up code, allowing smoother transitions between games and commands.")
    embed.add_field(name="v1.4", value="Added the TicTacToe game. Use '-help' to read more on how to play.")
    await ctx.send(embed=embed)







######################################################################
#                       Rank System                                 #
######################################################################

@bot.command()
async def rank(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    collection = db["rank"]

    print(member)

    user_xp = None
    member_stats = collection.find({"_id": member.id})
    for stat in member_stats:
        user_xp = stat["xp"]

    if user_xp == None:
        rank_info = {"_id": member.id, "xp": 0}
        collection.insert_one(rank_info)
        print("added!")
        user_xp = 0
    embed=discord.Embed(title=f"Current XP: {user_xp}", color=discord.Color.blue())
    await ctx.send(embed=embed)
    



@bot.command()
async def rank_add(ctx, xp, member: discord.Member = None):
    if ctx.author.id == 743819073917550682:
        if member == None:
            member = ctx.author
            print(member)
        collection = db["rank"]
        
        giveXP(member.id, xp)
        #retrive and send their new current xp
        member_stats = collection.find({"_id": member.id})
        for stat in member_stats:
            user_xp = stat["xp"]
        embed=discord.Embed(title="Total XP updated", color=discord.Color.green())
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="You are missing a vital step in achieving this power", color=discord.Color.red())
        await ctx.send(embed=embed)


def rankIds():
    collection = db["rank"]

    user_ids = []
    results = collection.find({})
    for result in results:
        user_ids.append(result["_id"])
    return(user_ids)

def rankPoints():
    collection = db["rank"]

    user_points = []
    results = collection.find({})
    for result in results:
        user_points.append(result["xp"])
    return(user_points)


@bot.group(invoke_without_command=True)
async def lb(ctx):
    lb_dict = dict(zip(rankIds(), rankPoints()))

    server_ids = []
    guild = bot.get_guild(ctx.guild.id)
    for user_id in rankIds():
        if guild.get_member(user_id) is not None:
            server_ids.append(user_id)
    
    server_points = []
    for id1 in server_ids:
        server_points.append(lb_dict[id1])
    
    points_descending = copy.deepcopy(server_points)
    points_descending.sort(reverse=True)

    lb_string = ""
    count = 0
    while count < 3:
        try:
            lb_string = lb_string + "<@" + str(server_ids[server_points.index(points_descending[count])]) + ">: " + str(points_descending[count]) + "\n"
        except IndexError:
            break
        count += 1
    embed=discord.Embed(title="Leaderboard", description=lb_string, color=discord.Color.blue())
    await ctx.send(embed=embed)

@lb.command(aliases=['global'])
async def everyone(ctx):
    points_descending = rankPoints()
    points_descending.sort(reverse=True)
    
    lb_string = ""
    count = 0
    while count < 3:
        try:
            lb_string = lb_string + "<@" + str(rankIds()[rankPoints().index(points_descending[count])]) + ">: " + str(points_descending[count]) + "\n"
        except IndexError:
            break
        count += 1
    embed=discord.Embed(title="Leaderboard", description=lb_string, color=discord.Color.blue())
    await ctx.send(embed=embed)




@bot.command()
async def nerf(ctx, item):
    if ctx.author.id == 743819073917550682:
        embed=discord.Embed(title="Creator has nerfed " + item + "!", color=discord.Color.purple())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You aren't the creator bruh try getting good to use this command", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def emoji(ctx):
    if ctx.author.id == 743819073917550682:
        for guild in bot.guilds:
            if guild.id == 840392576452132874:
                server = guild
        image = Image.open("red.png")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        await server.create_custom_emoji(name="amongus", image=img_byte_arr)
    else:
        embed = discord.Embed(title="Try getting good to use this command", color=discord.Color.red())
        await ctx.send(embed=embed)







######################################################################
#                       On Message Stuff                             #
######################################################################

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #print(message.author.id)

    msg = message.content.lower()

    #await bot.process_commands(message)
    
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)


    embeds = message.embeds
    for embed in embeds:
        embed_dict = embed.to_dict()
        #print(embed_dict)
        if "Printing is done" in embed_dict.get('title') and message.author.id == 797311463169327114:
            embed = discord.Embed(title="", description="<@" + str(743819073917550682) + ">, the print finished!", color=discord.Color.green())
            await message.channel.send(embed=embed)
            embed=discord.Embed(title="Print finished!", color=discord.Color.green())
            await bot.get_user(743819073917550682).send(embed=embed)
            await bot.get_user(743819073917550682).send(embed=embed)
            await bot.get_user(743819073917550682).send(embed=embed)
        elif "Printing is done" in embed_dict.get('title') and message.author.id == 873312017618980894:
            embed = discord.Embed(title="", description="<@" + str(753249383230865469) + ">, the print finished!", color=discord.Color.green())
            await message.channel.send(embed=embed)
            embed=discord.Embed(title="Print finished!", color=discord.Color.green())
            await bot.get_user(753249383230865469).send(embed=embed)



    ######################################################################
    #                       Word Responses                               #
    ######################################################################
    

    if msg.startswith('-8ball'):
        list1 = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.',
                 'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is decidedly so.',
                 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Outlook good.',
                 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes',
                 'Yes – definitely.', 'You may rely on it.']
        question = msg.split(' ')
        print(question)
        question.append(' ')
        print(question)
        await ctx.send("...")
        """
        if question[1] == ' ':
            embed = discord.Embed(title="Say your question lol", description="(e.g. -8ball Am I trash?)", color=discord.Color.red())
            await message.channel.send(embed=embed)
        elif question[1] != ' ':
            print(("aaa"))
            embed = discord.Embed(title=(secrets.choice(list1)), color=discord.Color.random())
            await message.channel.send(embed=embed)"""

    global deleteTrue
    if "-delete_trigger" in msg:
        if deleteTrue == False:
            deleteTrue = True
            print(deleteTrue)
        elif deleteTrue == True:
            deleteTrue = False
            print(deleteTrue)

    #global deleteTrue
    #print(deleteTrue)
    curseWord = ['yui', 'curse2']
    # delete curse word if match with the list
    if deleteTrue == True and any(word in msg for word in curseWord):
        await message.delete()




    #Ending minecraft or rock paper scissors
    if msg == "endgame":
        print("endgame")
        game_in_session = False
        print(game_in_session)
        await bot.process_commands(message)
        return



######################################################################
#                       Other Game Commands                          #
######################################################################
def writeRank(file, content):
    file.write(content + "\n")

def readRank(file, min, max):
    with open(file, 'r') as f:
        for line in islice(f, min, max+1):
            print(line, end='')










player1 = ""
player2 = ""
turn = ""
gameOver = True



winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

tictactoe_board = [
    [
        Button(style=ButtonStyle.grey, label=' ', id=1),
        Button(style=ButtonStyle.grey, label=' ', id=2),
        Button(style=ButtonStyle.grey, label=' ', id=3),
    ],
    [
        Button(style=ButtonStyle.grey, label=' ', id=4),
        Button(style=ButtonStyle.grey, label=' ', id=5),
        Button(style=ButtonStyle.grey, label=' ', id=6), 
        
    ],
    [
        Button(style=ButtonStyle.grey, label=' ', id=7),
        Button(style=ButtonStyle.grey, label=' ', id=8),
        Button(style=ButtonStyle.grey, label=' ', id=9),
        #Button(style=ButtonStyle.green, label='⛔', id="quit"), 
        
    ],
]

def checkWinner(board):
    for cond in winningConditions:
        check = all(item in board for item in cond)
        if check is True:
            return True


@bot.group(invoke_without_command=True)
async def tictactoe(ctx, p2: discord.Member):  # p1: discord.Member,
    global count
    global player1
    global player2
    global turn
    global gameOver
    global requested_person
    player1 = ctx.author
    player2 = p2

    # if p2.id == ctx.author.id:
    #embed=discord.Embed(title="Bruh", description="You can't play yourself lol", color=discord.Color.red())
    # await ctx.send(embed=embed)

    if gameOver:
        requested_person = p2
        embed = discord.Embed(title="TicTacToe Challenge", description=str(player1.mention) + "has challenged " + str(player2.mention) +
                              " to a TicTacToe game!\n They have 30 seconds to accept.\nUse -tictactoe accept to accept the challenge!", color=discord.Color.purple())
        starting_msg = await ctx.send(embed=embed)

        await asyncio.sleep(30)

        if gameOver:
            print(gameOver)
            print("sending expired msg")
            requested_person = None
            embed = discord.Embed(title="Request Expired", description="TicTacToe request from " + str(
                player1.mention) + " to " + str(player2.mention) + " has expired.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print("passed")
            pass
    else:
        embed = discord.Embed(title="You are already in a game",
                              description="If that person is afk just use 'place quit'.", color=discord.Color.red())
        await ctx.send(embed=embed)




@tictactoe.command()
async def accept(ctx):
    global count
    global player1
    global player2
    global turn
    global gameOver
    global requested_person

    if ctx.author.id == requested_person.id:
        requested_person = None
        
        turn = ""
        initial_turn = " "
        gameOver = False
        count = 0

        msg = await ctx.send(components=tictactoe_board, embed=discord.Embed(title="Loading...", color=discord.Color.blurple()))
        


        print(player1)
        print(player2)

        # determine who goes first
        num = randint(1, 2)
        if num == 1:
            turn = player1
            initial_turn = turn
            embed = discord.Embed(title="Starting Turn", description="It is <@" + str(player1.id) + ">'s turn.\nClick on a gray tile to place your marker there!",
                                  color=discord.Color.green())
            await msg.edit(embed=embed)

        elif num == 2:
            turn = player2
            initial_turn = turn
            embed = discord.Embed(title="Starting Turn", description="It is <@" + str(player2.id) + ">'s turn.\nClick on a gray tile to place your marker there!",
                                  color=discord.Color.green())
            await msg.edit(embed=embed)
        
        ingame_board = deepcopy(tictactoe_board)
        game_array_p1 = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        game_array_p2 = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


        while True:
            gameOver = False
            try:
                def check(res):
                    return turn.id == res.user.id and res.channel == ctx.channel

                res = await bot.wait_for("button_click", check=check, timeout=30)
                
                print(res.component.label)
                print(res.component.id)
                if res.component.id == "quit":
                    embed = discord.Embed(title="Force Quit", description="<@" + str(ctx.author.id) + "> has decided to quit.",
                                color=discord.Color.red())
                    break
                if res.component.id.startswith("marked"):
                    await res.respond(content="That box is already marked. Click an unfilled (gray) box.", ephemeral=True)
                else:
                    row = int((int(res.component.id)-1)/3)
                    column = (int(res.component.id)%3)-1

                    if turn == player1:
                        ingame_board[row][column] = Button(style=ButtonStyle.blue, label=' ', id=f"marked{res.component.id}")
                        game_array_p1[int(res.component.id)-1] = int(res.component.id)-1
                        
                        if checkWinner(game_array_p1):
                            embed = discord.Embed(title="Game Finished!", color=discord.Color.blue())
                            embed.add_field(name="Winner:", value=f"{player1.mention}", inline=True)
                            embed.add_field(name="Exp earnings/losses:", value=f"{player1.mention} received 30 exp for winning.\n{player2.mention} lost 15 exp for losing.")
                            await res.respond(embed=embed, type=7, components=ingame_board)
                            giveXP(player1.id, 30)
                            giveXP(player2.id, -15)
                            gameOver = True
                            break
                        if(initial_turn == player1):
                            filled = 0
                            for box in game_array_p1:
                                if box != " ":
                                    filled += 1
                            if filled == 5:
                                embed = discord.Embed(title="Game Finished!", color=discord.Color.blue())
                                embed.add_field(name="Tie", value="No winners", inline=True)
                                embed.add_field(name="Exp earnings/losses:", value=f"{player1.mention} received 5 exp for tying.\n{player2.mention} received 5 exp for tying.")
                                await res.respond(embed=embed, type=7, components=ingame_board)
                                giveXP(player1.id, 5)
                                giveXP(player2.id, 5)
                                gameOver = True
                                break

                    elif turn == player2:
                        ingame_board[row][column] = Button(style=ButtonStyle.red, label=' ', id=f"marked{res.component.id}")
                        game_array_p2[int(res.component.id)-1] = int(res.component.id)-1
                        print(ingame_board)
                        if checkWinner(game_array_p2):
                            embed = discord.Embed(title="Game Finished!", color=discord.Color.blue())
                            embed.add_field(name="Winner:", value=f"{player2.mention}", inline=True)
                            embed.add_field(name="Exp earnings/losses:", value=f"{player2.mention} received 30 exp for winning.\n{player1.mention} lost 15 exp for losing.")
                            await res.respond(embed=embed, type=7, components=ingame_board)
                            giveXP(player2.id, 30)
                            giveXP(player1.id, -15)
                            gameOver = True
                            break
                        if(initial_turn == player2):
                            filled = 0
                            for box in game_array_p2:
                                if box != " ":
                                    filled += 1
                            if filled == 5:
                                embed = discord.Embed(title="Game Finished!", color=discord.Color.blue())
                                embed.add_field(name="Tie", value="No winners", inline=True)
                                embed.add_field(name="Exp earnings/losses:", value=f"{player1.mention} received 5 exp for tying.\n{player2.mention} received 5 exp for tying.")
                                await res.respond(embed=embed, type=7, components=ingame_board)
                                giveXP(player1.id, 5)
                                giveXP(player2.id, 5)
                                gameOver = True
                                break

                    if turn == player1:
                        turn = player2
                        
                    elif turn == player2:
                        turn = player1

                    embed=discord.Embed(title="Turn Change", description=f"It is now {turn.mention}'s turn.")
                    
                    await res.respond(embed=embed, type=7, components=ingame_board)
            except asyncio.TimeoutError:
                await ctx.send(f"{turn.mention} you took too long. If you're still there, request to play another game of tictactoe.")
                gameOver = True
                break
    else:
        embed = discord.Embed(
            title="Error", description="No one invited you to a game of TicTacToe.\nUse -tictactoe challenge @User to start a game.", color=discord.Color.red())
        await ctx.send(embed=embed)



@tictactoe.command()
async def help(ctx):
    embed=discord.Embed(title="Tic Tac Toe", description="Tic Tac Toe, pretty self explanatory." + "\n" + "Using the command '-tictactoe @Person' to duel them (e.g. -tictactoe <@" + str(797239482830159912) + ">) will start a game of Tic Tac Toe with me :D (it actually won't)." + "\n" + "To play, just click on a gray tile to place your marker there.", color=discord.Color.blue())
    await ctx.send(embed=embed)





######################################################################
#                         Error Compensation                         #
######################################################################

@rank_add.error
async def rank_add_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title="You are missing a vital step in achieving this power")
        await ctx.send(embed=embed)


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Mention who you wanna play against", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Mention another person lmao", description="(i.e. <@743819073917550682>).", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='**Still on cooldown,** stop trying so hard. Try again in {:.2f}s'.format(error.retry_after), color=discord.Color.red())
        await ctx.send(embed=embed)
'''
@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Bruh enter a number", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Enter a number lol did you pass 2nd grade", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
'''

@bot.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


######################################################################
#                       Run Bot                                      #
######################################################################

extensions = ['cogs.MessageCommands', 'cogs.MemberRoleCommands', 'cogs.FunCommands', 'cogs.MessageType', 'cogs.WeatherCommand', 'cogs.DuelCommands', 'cogs.MinecraftBUTTONS', 'cogs.AgainstBotCommands']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

bot.run(awesomeguy_token)
