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
from discord_slash import SlashCommand
from discord.ext.commands import BucketType
from asyncdagpi import Client, ImageFeatures
from discord.utils import get
import aiohttp
from kasa import SmartPlug, SmartBulb
import webbrowser
import sys
import pymongo
from pymongo import MongoClient
import copy
import io


plug = SmartPlug("192.168.1.214")
bulb = SmartBulb("192.168.1.217")
#
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
async def verify(ctx, member_name):
    if ctx.guild.id == 882431857264828436:
        try:
            name_split = member_name.split("#")
            member = discord.utils.get(ctx.guild.members, name=name_split[0], discriminator=name_split[1])
            unverified_role = discord.utils.get(ctx.guild.roles, name="unverified boi")
            verified_role = discord.utils.get(ctx.guild.roles, name="verified")
            if unverified_role in member.roles:
                await member.remove_roles(unverified_role)
                await member.add_roles(verified_role)
                embed=discord.Embed(title="You have been successfully verified!", color=discord.Color.green())
                await bot.get_user(member.id).send(embed=embed)
                embed=discord.Embed(title=f"{member_name} has been successfully verified!", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"{member_name} is already verified.", color=discord.Color.purple())
                await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title="Format: -verify Name#Discriminator", color=discord.Color.red())
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



######################################################################
#                       Bot Testing Commands                         #
######################################################################
@bot.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')

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
    embed = discord.Embed(title="Bot Commands", description="Use the '-' prefix before every command.", color=discord.Color.blue())
    embed.add_field(name="Rank Commands", value="-rank, -rank @User, -lb", inline=True)
    embed.add_field(name="Fun Commands", value="-8ball, -inspire, -say, -dm, -random, -flip", inline=True)
    embed.add_field(name="Game Commands", value="-tictactoe, -rps, -guess, -duel" + "\n" + "**Look below to find more about these**", inline=True)
    embed.add_field(name="Help Commands", value="-tictactoe help, -rps help, -guess help, -duel help, -music help", inline=True)
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
    #                       Rock Paper Scissors                          #
    ######################################################################

    global game_in_session
    if game_in_session and msg != "-rps":

        moves = ["rock", "paper", "scissors"]

        num =   randint(0, 2)

        embed = discord.Embed(title="You played: " + msg + "\n"
                                                           "I played: " + moves[num])
        await message.channel.send(embed=embed)

        if not (msg in moves):
            embed = discord.Embed(title="Please answer with either 'rock', 'paper', or 'scissors'")
            await message.channel.send(embed=embed)
        elif moves.index(msg) - 2 == num:
            embed = discord.Embed(title="I win! EZ")
            await message.channel.send(embed=embed)
            giveXP(message.author.id, -5)
            embed = discord.Embed(title="You lost 5 exp for losing", color=discord.Color.red())
            await message.channel.send(embed=embed)
            await message.channel.send("You lost 5 exp for losing")
        elif moves.index(msg) + 2 == num:
            embed = discord.Embed(title="You win! GG")
            await message.channel.send(embed=embed)
            giveXP(message.author.id, 10)
            embed = discord.Embed(title="You received 10 exp for winning!", color=discord.Color.green())
            await message.channel.send(embed=embed)
        elif moves.index(msg) - 1 == num:
            embed = discord.Embed(title="You win! GG")
            await message.channel.send(embed=embed)
            giveXP(message.author.id, 10)
            embed = discord.Embed(title="You received 10 exp for winning!", color=discord.Color.green())
            await message.channel.send(embed=embed)
        elif moves.index(msg) == num:
            embed = discord.Embed(title="Draw -_-")
            await message.channel.send(embed=embed)
        elif moves.index(msg) + 1 == num:
            embed = discord.Embed(title="I win! EZ")
            await message.channel.send(embed=embed)
            giveXP(message.author.id, -5)
            embed = discord.Embed(title="You lost 5 exp for losing", color=discord.Color.red())
            await message.channel.send(embed=embed)

        game_in_session = False

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
        if question[1] == ' ':
            embed = discord.Embed(title="Say your question lol", description="(e.g. -8ball Am I trash?)", color=discord.Color.red())
            await message.channel.send(embed=embed)
        elif question[1] != ' ':
            print(("aaa"))
            embed = discord.Embed(title=(secrets.choice(list1)), color=discord.Color.random())
            await message.channel.send(embed=embed)

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














def giveWeapon(id, weapon):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("equipInfo", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("equipInfo", "r")
    list_of_lines = f.readlines()
    weapon = weapon + "\n"
    list_of_lines[line_number + 1] = weapon
    print(type(list_of_lines))
    # list_of_lines.append("\n")
    print(list_of_lines)

    f = open("equipInfo", "w")
    f.writelines(list_of_lines)
    f.close()


def giveWeapon2(id, weapon):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("equipInfo", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("equipInfo", "r")
    list_of_lines = f.readlines()
    weapon = weapon + "\n"
    list_of_lines[line_number + 2] = weapon
    print(type(list_of_lines))
    # list_of_lines.append("\n")
    print(list_of_lines)

    f = open("equipInfo", "w")
    f.writelines(list_of_lines)
    f.close()


def giveHeal(id, healInput):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("equipInfo", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("equipInfo", "r")
    list_of_lines = f.readlines()
    original_xp = int(list_of_lines[line_number + 3])
    healInt = healInput
    xp = str(healInt + original_xp) + "\n"
    list_of_lines[line_number + 3] = xp
    print(type(list_of_lines))
    # list_of_lines.append("\n")
    print(list_of_lines)

    f = open("equipInfo", "w")
    f.writelines(list_of_lines)
    f.close()


@bot.command()
async def buy(ctx, *, weapon):
    global line
    shopStuff = ["Nerf Gun", "Log", "Healing Potion", "Bazooka", "Fork"]
    shopStuffLower = ["nerf gun", "log", "healing potion", "bazooka", "fork"]
    shopStuffCost = [100, 60, 75, 200, 75]
    convertedId = str(ctx.author.id)
    if weapon in shopStuffLower:
        itemIndex = shopStuffLower.index(weapon)
        print(itemIndex)
        if convertedId in open("rankinfo").read():
            print("success")
            # print(convertedId + "aaa")
            phrase = convertedId
            line_number = "Phrase not found"
            f = open("rankinfo", "r")

            for number, line in enumerate(f):
                if phrase in line:
                    line_number = number
                    break
            f.close()

            print(line_number)  # "+1, its the user id"
            with open("rankinfo", 'r') as f:
                for line in islice(f, line_number + 1, line_number + 2):
                    print("User xp: " + line)
            f.close()
        elif convertedId not in open("rankinfo").read():
            embed = discord.Embed(title="Please use '-rank' to set up your XP profile before using this.",
                                  color=discord.Color.purple())
            await ctx.send(embed=embed)
        # print(line)
        global userXP
        userXP = int(line)

        print(userXP)
        if shopStuffCost[itemIndex] <= userXP:  # current xp
            giveXP(ctx.author.id, -shopStuffCost[itemIndex])
            if itemIndex == 2:
                giveHeal(ctx.author.id, 1)
                embed = discord.Embed(
                    title="You spent " + str(shopStuffCost[itemIndex]) + "XP on a " + shopStuff[itemIndex] + "!",
                    color=discord.Color.blue())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Respond with where you want this weapon to go to. 1 for primary, 2 for secondary.",
                    color=discord.Color.blue())
                await ctx.send(embed=embed)

                def is_correct(m):
                    return m.author == ctx.author and m.content.isdigit()

                msg = await bot.wait_for('message', check=is_correct, timeout=30)
                attempt = int(msg.content)

                if attempt == 1:
                    giveWeapon(ctx.author.id, weapon)
                    embed = discord.Embed(
                        title="You spent " + str(shopStuffCost[itemIndex]) + "XP on a " + shopStuff[itemIndex] + "!",
                        color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    # await ctx.send("Gave '" + weapon + "'!")
                elif attempt == 2:
                    giveWeapon2(ctx.author.id, weapon)
                    embed = discord.Embed(
                        title="You spent " + str(shopStuffCost[itemIndex]) + "XP on a " + shopStuff[itemIndex] + "!",
                        color=discord.Color.blue())
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You don't have enough xp to purchase this", color=discord.Color.red())
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="That's not a purchasable weapon", color=discord.Color.red())
        await ctx.send(embed=embed)

@buy.error
async def buy_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="You must specify an item to buy. You can find the list of items to buy using '-shop'.",
            color=discord.Color.purple())
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Please use '-shop' to set up your inventory and see available items to purchase.",
                              color=discord.Color.purple())
        await ctx.send(embed=embed)




        








@bot.group(invoke_without_command=True)
async def rps(ctx):
    if ctx.author == bot.user:
        return

    # temp_id = ctx.author.id
    global game_in_session

    # msg = ctx.content
    embed = discord.Embed(title="Rock")
    await ctx.send(embed=embed)
    time.sleep(1)
    embed = discord.Embed(title="Paper")
    await ctx.send(embed=embed)
    time.sleep(1)
    embed = discord.Embed(title="Scissors")
    await ctx.send(embed=embed)
    time.sleep(1)
    embed = discord.Embed(title="SHOOT")

    await ctx.send(embed=embed)

    # 0 = rock, 1 = paper, 2 = scissors

    game_in_session = True














player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

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

    if p2.id == ctx.author.id:
        embed=discord.Embed(title="Bruh", description="You can't play yourself lol", color=discord.Color.red())
        await ctx.send(embed=embed)

    elif gameOver:
        requested_person = p2
        embed=discord.Embed(title="TicTacToe Challenge", description=str(player1.mention) + "has challenged " + str(player2.mention) + " to a TicTacToe game!\n They have 15 seconds to accept.\nUse -tictactoe accept to accept the challenge!", color=discord.Color.purple())
        await ctx.send(embed=embed)

        await asyncio.sleep(15)

        if gameOver:
            requested_person = None
            embed = discord.Embed(title="Request Expired",description="TicTacToe request from " + str(player1.mention) + " to " + str(player2.mention) + " has expired.",color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print("passed")
            pass
    else:
        embed=discord.Embed(title="You are already in a game", description="If that person is afk just use 'place quit'.", color=discord.Color.red())
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
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        global board1
        board1 = [":one:", ":two:", ":three:",
                  ":four:", ":five:", ":six:",
                  ":seven:", ":eight:", ":nine:"]
        turn = ""
        gameOver = False
        count = 0


        print(player1)
        print(player2)

        embed = discord.Embed(title="Board Layout:", color=discord.Color.blue())
        await ctx.send(embed=embed)
        line1 = ""
        x = 0
        print("bruh")
        global arf
        arf = False
        while arf == False:
            if x == 2:
                print('here2')
                line1 += board1[x] + "\n"
                x += 1
            elif x == 5:
                line1 += board1[x] + "\n"
                print("here5")
                x += 1
            elif x == 8:
                line1 += board1[x]
                await ctx.send(line1)
                print("here8")
                arf = True
            else:
                line1 += board1[x] + " "
                print("here+1")
                x += 1

        line1 = ""
        x = 0
        print("bruh")
        arf = False
        while arf == False:
            if x == 2:
                print('here2')
                line1 += board[x] + "\n"
                x += 1
            elif x == 5:
                line1 += board[x] + "\n"
                print("here5")
                x += 1
            elif x == 8:
                line1 += board[x]
                await ctx.send(line1)
                print("here8")
                arf = True
            else:
                line1 += board[x] + " "
                print("here+1")
                x += 1

        # determine who goes first
        num = randint(1, 2)
        if num == 1:
            turn = player1
            embed = discord.Embed(title="Starting Turn", description="It is <@" + str(player1.id) + ">'s turn.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        elif num == 2:
            turn = player2
            embed = discord.Embed(title="Starting Turn", description="It is <@" + str(player2.id) + ">'s turn.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description="No one invited you to a game of TicTacToe.\nUse -tictactoe challenge @User to start a game.", color=discord.Color.red())
        await ctx.send(embed=embed)


@bot.command()
async def place(ctx, pos2):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if pos2 == "quit" and not gameOver:
        gameOver = True
        embed = discord.Embed(title="Force Quit", description="<@" + str(ctx.author.id) + "> has decided to quit.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        embed = discord.Embed(title="Game Finished!", description="Player resigned.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)
    pos = int(pos2)
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if player2.id == bot.user.id and turn == player2:
                board[3 - 1] = mark
                count += 1

                line1 = ""
                x = 0
                print("bruh")
                global arf
                arf = False
                while arf == False:
                    if x == 2:
                        print('here2')
                        line1 += board[x] + "\n"
                        x += 1
                    elif x == 5:
                        line1 += board[x] + "\n"
                        print("here5")
                        x += 1
                    elif x == 8:
                        line1 += board[x]
                        await ctx.send(line1)
                        print("here8")
                        arf = True
                    else:
                        line1 += board[x] + " "
                        print("here+1")
                        x += 1

                checkWinner(winningConditions, mark)
            elif 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                line1 = ""
                x = 0
                print("bruh")
                #global arf
                arf = False
                while arf == False:
                    if x == 2:
                        print('here2')
                        line1 += board[x] + "\n"
                        x += 1
                    elif x == 5:
                        line1 += board[x] + "\n"
                        print("here5")
                        x += 1
                    elif x == 8:
                        line1 += board[x]
                        await ctx.send(line1)
                        print("here8")
                        arf = True
                    else:
                        line1 += board[x] + " "
                        print("here+1")
                        x += 1

                checkWinner(winningConditions, mark)
                print(count)
                print(mark)
                print(type(mark))
                print(player1)
                if gameOver == True and mark == ":regional_indicator_x:":
                    print(player1.id)
                    print(player2.id)
                    giveXP(player1.id, 30)
                    giveXP(player2.id, -15)
                    embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                        player1.id) + "> was given 30 exp for winning." + "\n" + "<@" + str(
                        player2.id) + "> lost 15 exp for losing.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    print("here??? 2.0")
                elif gameOver == True and mark == ":o2:":
                    print(player1.id)
                    print(player2.id)

                    giveXP(player2.id, 20)
                    giveXP(player1.id, -15)
                    embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                        player2.id) + "> was given 20 exp for winning." + "\n" + "<@" + str(
                        player1.id) + "> lost 15 exp for losing.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    print("here???")

                elif count >= 9:
                    gameOver = True
                    embed=discord.Embed(title="Tie", description="No XP is awarded for tying", color=discord.Color.blue())
                    await ctx.send(embed=embed)

                # switch turns
                if turn == player1 and gameOver == False:
                    embed = discord.Embed(title="Turn change",
                                          description="It is now <@" + str(player2.id) + ">'s turn.",
                                          color=discord.Color.green())
                    await ctx.send(embed=embed)
                    turn = player2
                elif turn == player2 and gameOver == False:
                    embed = discord.Embed(title="Turn change",
                                          description="It is now <@" + str(player1.id) + ">'s turn.",
                                          color=discord.Color.green())
                    await ctx.send(embed=embed)
                    turn = player1
            else:
                embed = discord.Embed(title="Incorrect format",
                                      description="Put it like this: -place 'number'. Make sure the numbered square isn't filled",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="No cheating",
                                  description="It's not your turn bruh",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="No game going on", description="Start a new one using the 'tictactoe challenge' command.", color=discord.Color.red())
        await ctx.send(embed=embed)


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.command()
async def help(ctx):
    embed=discord.Embed(title="Tic Tac Toe", description="Tic Tac Toe, pretty self explanatory." + "\n" + "Using the command '-tictactoe' followed by mentioning 2 users (e.g. -tictactoe <@" + str(743819073917550682) + "> <@" + str(797239482830159912) + ">) will start a game of Tic Tac Toe with those two players." + "\n" + "Use '-place' followed by a place number to place an :regional_indicator_x: or :o2: in that corresponding box." + "\n" + "A board of the key to the place numbers will be printed at the beginning of each game, as well to the right.\nYou can use '-place quit' to exit a game.", color=discord.Color.blue())
    embed.add_field(name="Tic Tac Toe Correspondence", value=":one: :two: :three: | :white_large_square: :white_large_square: :white_large_square:" + "\n" ":four: :five: :six: | :white_large_square: :white_large_square: :white_large_square:" + "\n" + ":seven: :eight: :nine: | :white_large_square: :white_large_square: :white_large_square:" + "\n")
    await ctx.send(embed=embed)

@rps.command()
async def help(ctx):
    embed=discord.Embed(title="Rock Paper Scissors", description="RPS stands for Rock Paper Scissors, a commonly known game." + "\n" + "Using the command '-rps', the bot will countdown 'Rock', 'Paper', 'Scissors', and 'Shoot!'." + "\n" + "When it says shoot, you job is to type rock, paper, or scissors, and the bot will also generate one of them, and see who is the winner." + "\n" + "This was the first game project which is why it's lame good day", color=discord.Color.blue())
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

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Bruh enter a number", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Enter a number lol did you pass 2nd grade", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)

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

extensions = ['cogs.MessageCommands', 'cogs.MemberRoleCommands', 'cogs.FunCommands', 'cogs.MessageType', 'cogs.WeatherCommand', 'cogs.DuelCommands', 'cogs.Minecraft', 'cogs.AgainstBotCommands']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

bot.run(awesomeguy_token)
