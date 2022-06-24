from discord.ext import commands
import discord
from itertools import islice
import time
import asyncio
from secrets import randbelow
import pymongo
from pymongo import MongoClient
import os

mongo_cluster = os.getenv('mongo_cluster')


player1 = ""
player2 = ""
gameOver = True

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

def writeRank(file, content):
    file.write(content + "\n")



def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)


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

class DuelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def buy(self, ctx, *, weapon):
        global line
        shopStuff = ["Nerf Gun", "Log", "Healing Potion", "Bazooka", "Fork"]
        shopStuffLower = ["nerf gun", "log", "healing potion", "bazooka", "fork"]
        shopStuffCost = [100, 60, 75, 200, 75]
        convertedId = str(ctx.author.id)
        collection = db["rank"]
        if weapon in shopStuffLower:
            itemIndex = shopStuffLower.index(weapon)
            print(itemIndex)
            user_xp = None
            member_stats = collection.find({"_id": ctx.author.id})
            for stat in member_stats:
                user_xp = stat["xp"]
                
            
            if user_xp == None:
                embed = discord.Embed(title="Please use '-rank' to set up your XP profile before using this.",
                                    color=discord.Color.purple())
                await ctx.send(embed=embed)
            # print(line)
            global userXP
            userXP = int(user_xp) 

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

                    msg = await self.bot.wait_for('message', check=is_correct, timeout=30)
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
    
    @commands.command()
    async def shop(self, ctx, member: discord.Member = None):
        # await ctx.send("in shop")
        if member == None:
            member = ctx.author
            print(member)

        print(member)
        print(type(member))
        convertedId = str(member.id)

        if convertedId in open("equipInfo").read():


            # print shop
            embed = discord.Embed(title="Weapons for sale",
                                description="**Nerf Gun Cost**: 100 xp\n**Log Cost**: 60 xp\n**Bazooka**: 200 xp\n**Fork**: 75 xp\n**Healing Potion**: 75 xp",
                                color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:

            f = open("equipInfo", 'a')
            writeRank(f, convertedId)
            writeRank(f, "stick")
            writeRank(f, "stick")
            writeRank(f, "0")
            f.close()
            embed = discord.Embed(title="Please wait, setting up your profile...", color=discord.Color.purple())
            await ctx.send(embed=embed)
            time.sleep(2)
            phrase = convertedId
            line_number = "Phrase not found"
            f = open("equipInfo", "r")

            for number, line in enumerate(f):
                if phrase in line:
                    line_number = number
                    print(line)
                    break
            f.close()

            print(line_number)
            # readRank("rankinfo", line_number+1, line_number+2)
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 1, line_number + 2):
                    primaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 2, line_number + 3):
                    print(line)
                    secondaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 3, line_number + 4):
                    print(line)
                    numHeals = line

                    embed = discord.Embed(title="Your Inventory",
                                        description="**Primary Weapon:** " + primaryWeapon + "**Secondary Weapon:** " + secondaryWeapon + "**Healing Potions:** " + numHeals,
                                        color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    # print shop
                    embed = discord.Embed(title="Weapons for sale",
                                        description="**Nerf Gun Cost**: 100 xp\n**Log Cost**: 60 xp\n**Bazooka**: 200 xp\n**Fork**: 75 xp\n**Healing Potion**: 75 xp",
                                        color=discord.Color.purple())
                    await ctx.send(embed=embed)
                f.close()
    @commands.command(name="inventory", aliases=['inv'])
    async def inventory(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
            print(member)

        print(member)
        print(type(member))
        convertedId = str(member.id)
        if convertedId in open("equipInfo").read():
            print("success")
            # print(convertedId + "aaa")
            phrase = convertedId
            line_number = "Phrase not found"
            f = open("equipInfo", "r")

            for number, line in enumerate(f):
                if phrase in line:
                    line_number = number
                    break
            f.close()

            print(line_number)  # "+1, its the user id"
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 1, line_number + 2):

                    primaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 2, line_number + 3):
                    print(line)

                    secondaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 3, line_number + 4):
                    print(line)

                    numHeals = line
                f.close()

            embed=discord.Embed(title="Your Inventory", description="**Primary Weapon:** " + primaryWeapon + "**Secondary Weapon:** " + secondaryWeapon + "**Healing Potions:** " + numHeals, color=discord.Color.blue())
            await ctx.send(embed=embed)


        else:

            f = open("equipInfo", 'a')
            writeRank(f, convertedId)
            writeRank(f, "stick")
            writeRank(f, "stick")
            writeRank(f, "0")
            f.close()
            embed = discord.Embed(title="Please wait, setting up your profile...", color=discord.Color.purple())
            await ctx.send(embed=embed)
            time.sleep(3)
            phrase = convertedId
            line_number = "Phrase not found"
            f = open("equipInfo", "r")

            for number, line in enumerate(f):
                if phrase in line:
                    line_number = number
                    break
            f.close()

            print(line_number)
            # readRank("rankinfo", line_number+1, line_number+2)
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 1, line_number + 2):
                    primaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 2, line_number + 3):

                    secondaryWeapon = line
                f.close()
            with open("equipInfo", 'r') as f:
                for line in islice(f, line_number + 3, line_number + 4):
                    numHeals = line
                f.close()

            embed = discord.Embed(title="Your Inventory",
                                description="**Primary Weapon:** " + primaryWeapon + "**Secondary Weapon:** " + secondaryWeapon + "**Healing Potions:** " + numHeals, color=discord.Color.blue())
            await ctx.send(embed=embed)

    

    @commands.group(invoke_without_command=True)
    async def duel(self, ctx, p2: discord.Member, inputHP2: int = 100):
        global inputHP
        inputHP = float(inputHP2)
        global player1
        global player2
        player1 = ctx.author
        player2 = p2
        global player1Health
        global player2Health
        player1Health = inputHP
        player2Health = inputHP
        global startingHP
        startingHP = inputHP
        global turn
        global gameOver
        global requested_person 
        if p2.id == ctx.author.id:
            embed=discord.Embed(title="Bruh", description="You can't play yourself lol", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif gameOver:
                requested_person = p2
                embed=discord.Embed(title="Duel Challenge", description=str(player1.mention) + "has challenged " + str(player2.mention) + " to duel!\n They have 30 seconds to accept.\nUse -duel accept to accept the challenge!", color=discord.Color.purple())
                await ctx.send(embed=embed)

                await asyncio.sleep(30)

                if gameOver:
                    requested_person = None
                    embed = discord.Embed(title="Request Expired",description="Duel request from " + str(player1.mention) + " to " + str(player2.mention) + " has expired.",color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    print("passed")
                    pass
        else:
            embed=discord.Embed(title="You are already in a game", description="If that person is afk just use 'place quit'.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @duel.command()
    async def accept(self, ctx):
        global player1
        global player2
        global player1Health
        global player2Health
        global startingHP
        global inputHP
        global turn
        global gameOver
        global requested_person
        
        if ctx.author.id == requested_person.id:
            requested_person = None

            gameOver = False
            count = 0

            #player1 = ctx.author
            print((player1))
            

            print("test")

            # determine who goes first
            num = randint(1, 2)
            if num == 1:
                turn = player1
                embed=discord.Embed(title="Turn", description="It is <@" + str(player1.id) + ">'s turn.", color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Game Info",
                                    description="Type **'-inv'** to see your available items.\nType **'-use (item)'** to use a certain item.\nYou both have **" + str(inputHP) + "** health starting.", color=discord.Color.blue())
                await ctx.send(embed=embed)
            elif num == 2:
                turn = player2
                embed = discord.Embed(title="Turn", description="It is <@" + str(player2.id) + ">'s turn.", color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Game Info", description="Type **'-inv'** to see your available items.\nType **'-use (item)'** to use a certain item.\nYou both have **" + str(inputHP) + "** health starting.", color=discord.Color.blue())
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Error", description="No one invited you to a duel.\nUse -duel @User to start a game.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def use(self, ctx, *, move):
        global turn
        global player1
        global player2
        global player1Health
        global player2Health
        global startingHP
        global gameOver


        #print(startingHP)
        if move == "quit" and not gameOver:
            gameOver = True
            embed = discord.Embed(title="Force Quit", description="<@" + str(ctx.author.id) + "> has decided to quit.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            embed = discord.Embed(title="Game Finished!", description="Player resigned.",
                                color=discord.Color.green())
            await ctx.send(embed=embed)
        if not gameOver:
            if turn == ctx.author:
                if turn == player1:
                    print("test1")
                    convertedId = str(player1.id)
                    phrase = convertedId
                    line_number = "Phrase not found"
                    f = open("equipInfo", "r")

                    for number, line in enumerate(f):
                        if phrase in line:
                            line_number = number
                            break
                    f.close()

                    print(line_number)
                    # readRank("rankinfo", line_number+1, line_number+2)
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 1, line_number + 2):
                            userWeapon1 = line
                            # embed = discord.Embed(title="Current Weapon: " + line, color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 2, line_number + 3):
                            userWeapon2 = line
                            # embed = discord.Embed(title="Current Weapon: " + line, color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 3, line_number + 4):
                            # print(line)
                            userHeals123 = line
                            # embed = discord.Embed(title="Number of Healing Potions: " + str(line), color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()

                    print(userWeapon1)
                    print(userWeapon2)
                    print(userHeals123)
                    userHeals = userHeals123.replace('\n', '')

                    weaponList = ["nerf gun", "log", "stick", "healing potion", "bazooka", "fork", " "]
                    weaponDmg = [30, 20, 10, 25, startingHP, 15, 40]
                    itemIndex = weaponList.index(move)
                    print(itemIndex)
                    if " " in move:
                        moveinputList = move.split(" ")
                    # make a while/for loop to allow a 2nd chance
                    if move + "\n" == userWeapon1 or move + "\n" == userWeapon2:
                        if move == "bazooka":
                            hitProb = randint(1, 4)
                            print(str(hitProb) + "HIT BAZOOKA PROB RAND")
                            if hitProb == 1:
                                embed = discord.Embed(
                                    title="You used " + move + " dealing " + str(
                                        player2Health) + " health! KO",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - player2Health
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(
                                                            player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            else: 
                                embed = discord.Embed(
                                    title="You used " + move + " but threw it too close to yourself dealing " + str(
                                        player1Health) + " to yourself lol!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - player1Health
                                print(str(player1Health) + " PLAYER 1 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(
                                                            player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                        else:
                            crit = randint(1, 5)
                            dodge = randint(1, 4)
                            selfHit = randint(1, 7)
                            print(str(crit) + "CRIT RAND")
                            print(str(dodge) + "DODGE RAND")
                            print(str(selfHit) + "SELF HIT RAND")

                            regDmg = weaponDmg[itemIndex] #when more cases use probability times probability
                            forkType = randint(1, 4)
                            print(str(forkType) + "FORK TYPE RAND")
                            if move.startswith("fork") and forkType == 1:
                                regDmg = weaponDmg[6]
                            elif move.startswith("fork") and (forkType == 2 or forkType == 3 or forkType == 4):
                                regDmg = weaponDmg[5]

                            if crit == 1 and dodge != 1:
                                print("only crit oppo")
                                embed = discord.Embed(
                                    title="You used " + move + " doing a **critical hit** dealing " + str(1.5*regDmg) + " health!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - 1.5*regDmg
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif crit == 1 and dodge == 1:
                                print("crit oppo, but he dodged")
                                embed = discord.Embed(
                                    title="You used " + move + " doing a **critical hit** which would have dealt " + str(1.5*regDmg) + " health,", description="But <@" + str(player2.id) + "> was smart enough to dodge!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif dodge == 1 and crit != 1:
                                print("only opponent dodged")
                                embed = discord.Embed(
                                    title="You used " + move + " which would have dealt " + str(regDmg) + " health,", description="But <@" + str(player2.id) + "> was smart enough to dodge!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)

                            elif selfHit == 1 and crit != 1:
                                print("hit yourself reg")
                                embed = discord.Embed(
                                    title="You used " + move + " which rebounded and hit yourself for " + str(regDmg) + " health lol",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - weaponDmg[itemIndex]
                                print(str(player1Health) + " PLAYER 1 HEALTH SELF HIT")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif selfHit == 1 and crit == 1:
                                print("hit yourself with crit")
                                embed = discord.Embed(
                                    title="You used " + move + " which rebounded and did a **critical hit** on yourself for " + str(1.5*regDmg) + " health lol",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - 1.5*regDmg
                                print(str(player1Health) + " PLAYER 1 HEALTH SELF CRIT")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)


                            else:
                                embed = discord.Embed(
                                    title="You used " + move + " dealing " + str(regDmg) + " health!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - regDmg
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:", description="<@" + str(player1.id) + ">'s Health: " + str(player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                    elif move == "healing potion" and int(userHeals) > 0:
                        print(userHeals)
                        if player1Health >= startingHP - 24:
                            hpGain = startingHP - player1Health
                            giveHeal(ctx.author.id, -1)
                            embed = discord.Embed(
                                title="You used " + move + " healing " + str(hpGain) + " of your health!",
                                color=discord.Color.green())
                            await ctx.send(embed=embed)
                            player1Health = player1Health + hpGain
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">'s Health: " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="You used " + move + " healing " + str(weaponDmg[itemIndex]) + " of your health!",
                                color=discord.Color.green())
                            await ctx.send(embed=embed)
                            giveHeal(ctx.author.id, -1)
                            player1Health = player1Health + weaponDmg[itemIndex]
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">'s Health: " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)


                    else:
                        embed = discord.Embed(title="You don't have that item. Check your inventory to see your available items.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                    if gameOver == True:
                        embed = discord.Embed(title="Player Healths:",
                                            description="<@" + str(player1.id) + ">**'s Health:** " + str(
                                                player1Health) + "\n<@" + str(player2.id) + ">**'s Health:** " + str(
                                                player2Health), color=discord.Color.green())
                        await ctx.send(embed=embed)
                        if player1Health == 0:
                            embed = discord.Embed(title="Game Finished!", description="<@" + str(player2.id) + "> won!",
                                                color=discord.Color.green())
                            await ctx.send(embed=embed)
                            xpEarned = int((startingHP * 3) / 10)
                            xpLost = int((startingHP * 3) / 20)
                            print(xpEarned)
                            print(type(xpEarned))
                            giveXP(player2.id, xpEarned)
                            giveXP(player1.id, -xpLost)
                            embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                                player2.id) + "> was given " + str(xpEarned) + " exp for winning." + "\n" + "<@" + str(
                                player1.id) + "> lost " + str(xpLost) + " exp for losing.", color=discord.Color.blue())
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title="Game Finished!", description="<@" + str(player1.id) + "> won!", color=discord.Color.green())
                            await ctx.send(embed=embed)
                            xpEarned = int((startingHP * 3) / 10)
                            xpLost = int((startingHP * 3) / 20)
                            print(xpEarned)
                            print(type(xpEarned))
                            giveXP(player1.id, xpEarned)
                            giveXP(player2.id, -xpLost)
                            embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                                player1.id) + "> was given " + str(xpEarned) + " exp for winning." + "\n" + "<@" + str(
                                player2.id) + "> lost " + str(xpLost) + " exp for losing.", color=discord.Color.blue())
                            await ctx.send(embed=embed)
                    else:
                        # switch turns

                        embed = discord.Embed(title="Turn change", description="It is now <@" + str(player2.id) + ">'s turn.",
                                            color=discord.Color.green())
                        await ctx.send(embed=embed)
                        turn = player2


                elif turn == player2:
                    print("test2")
                    convertedId = str(player2.id)
                    phrase = convertedId
                    line_number = "Phrase not found"
                    f = open("equipInfo", "r")

                    for number, line in enumerate(f):
                        if phrase in line:
                            line_number = number
                            break
                    f.close()

                    print(line_number)
                    # readRank("rankinfo", line_number+1, line_number+2)
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 1, line_number + 2):
                            userWeapon1 = line
                            # embed = discord.Embed(title="Current Weapon: " + line, color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 2, line_number + 3):
                            userWeapon2 = line
                            # embed = discord.Embed(title="Current Weapon: " + line, color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()
                    with open("equipInfo", 'r') as f:
                        for line in islice(f, line_number + 3, line_number + 4):
                            # print(line)
                            userHeals = line
                            # embed = discord.Embed(title="Number of Healing Potions: " + str(line), color=discord.Color.blue())
                            # await ctx.send(embed=embed)
                        f.close()

                    print(userWeapon1)
                    print(userWeapon2)
                    print(userHeals)

                    weaponList = ["nerf gun", "log", "stick", "healing potion", "bazooka", "fork", " "]
                    weaponDmg = [30, 20, 10, 25, startingHP, 15, 40]
                    itemIndex = weaponList.index(move)
                    print(itemIndex)

                    # make a while/for loop to allow a 2nd chance
                    if move + "\n" == userWeapon1 or move + "\n" == userWeapon2:
                        if move == "bazooka":
                            hitProb = randint(1, 4)
                            print(str(hitProb) + "HIT BAZOOKA PROB RAND")
                            if hitProb == 1:
                                embed = discord.Embed(
                                    title="You used " + move + " dealing " + str(
                                        player1Health) + " health! KO",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - player1Health
                                print(str(player2Health) + " PLAYER 1 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(
                                                            player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    title="You used " + move + " but threw it too close to yourself dealing " + str(player2Health) + " to yourself lol!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - player2Health
                                print(str(player2Health) + " PLAYER 2 HEALTH")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(
                                                            player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                        else:
                            crit = randint(1, 5)
                            dodge = randint(1, 4)
                            selfHit = randint(1, 7)
                            print(str(crit) + "CRIT RAND")
                            print(str(dodge) + "DODGE RAND")
                            print(str(selfHit) + "SELF HIT RAND")
                            regDmg = weaponDmg[itemIndex]  # when more cases use probability times probability
                            forkType = randint(1, 4)
                            print(str(forkType) + "FORK TYPE RAND")
                            if move.startswith("fork") and forkType == 1:
                                regDmg = weaponDmg[6]
                            elif move.startswith("fork") and (forkType == 2 or forkType == 3 or forkType == 4):
                                regDmg = weaponDmg[5]

                            if crit == 1 and dodge != 1:
                                print("only crit oppo")
                                embed = discord.Embed(
                                    title="You used " + move + " doing a **critical hit** dealing " + str(
                                        1.5 * regDmg) + " health!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - 1.5 * regDmg
                                print(str(player1Health) + " PLAYER 2 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif crit == 1 and dodge == 1:
                                print("crit oppo, but he dodged")
                                embed = discord.Embed(
                                    title="You used " + move + " doing a **critical hit** which would have dealt " + str(
                                        1.5 * regDmg) + " health,", description="But <@" + str(player1.id) + "> was smart enough to dodge!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health
                                print(str(player1Health) + " PLAYER 1 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif dodge == 1 and crit != 1:
                                print("only opponent dodged")
                                embed = discord.Embed(
                                    title="You used " + move + " which would have dealt " + str(
                                        regDmg) + " health,", description="But <@" + str(player1.id) + "> was smart enough to dodge!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health
                                print(str(player1Health) + " PLAYER 1 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)

                            elif selfHit == 1 and crit != 1:
                                print("hit yourself reg")
                                embed = discord.Embed(
                                    title="You used " + move + " which rebounded and hit yourself for " + str(regDmg) + " health lol!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - weaponDmg[itemIndex]
                                print(str(player1Health) + " PLAYER 2 HEALTH SELF HIT")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                            elif selfHit == 1 and crit == 1:
                                print("hit yourself with crit")
                                embed = discord.Embed(
                                    title="You used " + move + " which rebounded and did a **critical hit** on yourself for " + str(1.5*regDmg) + " health lol",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player2Health = player2Health - 1.5*regDmg
                                print(str(player1Health) + " PLAYER 2 HEALTH SELF CRIT")
                                if player2Health <= 0:
                                    gameOver = True
                                    player2Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)

                            else:
                                embed = discord.Embed(
                                    title="You used " + move + " taking away " + str(regDmg) + " health!",
                                    color=discord.Color.magenta())
                                await ctx.send(embed=embed)
                                player1Health = player1Health - weaponDmg[itemIndex]
                                print(str(player1Health) + " PLAYER 1 HEALTH")
                                if player1Health <= 0:
                                    gameOver = True
                                    player1Health = 0
                                else:
                                    embed = discord.Embed(title="Player Healths:",
                                                        description="<@" + str(player1.id) + ">'s Health: " + str(
                                                            player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                            player2Health), color=discord.Color.red())
                                    await ctx.send(embed=embed)
                    elif move == "healing potion" and int(userHeals) > 0:
                        if player2Health >= startingHP - 24:
                            hpGain = startingHP - player1Health
                            giveHeal(ctx.author.id, -1)
                            embed=discord.Embed(title="You used " + move + " healing " + str(hpGain) + " of your health!", color=discord.Color.green())
                            await ctx.send(embed=embed)
                            player2Health = player2Health + hpGain
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">'s Health: " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="You used " + move + " healing " + str(weaponDmg[itemIndex]) + " of your health!",
                                color=discord.Color.green())
                            await ctx.send(embed=embed)
                            giveHeal(ctx.author.id, -1)
                            player2Health = player2Health + weaponDmg[itemIndex]
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">'s Health: " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">'s Health: " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(title="You don't own that weapon", color=discord.Color.red())
                        await ctx.send(embed=embed)
                    if gameOver == True:
                        if player2Health == 0:
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">**'s Health:** " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">**'s Health:** " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)
                            embed = discord.Embed(title="Game Finished!", description="<@" + str(player1.id) + "> won!",
                                                color=discord.Color.green())
                            await ctx.send(embed=embed)
                            xpEarned = int((startingHP * 3) / 10)
                            xpLost = int((startingHP * 3) / 20)
                            print(xpEarned)
                            print(type(xpEarned))
                            giveXP(player1.id, xpEarned)
                            giveXP(player2.id, -xpLost)
                            embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                                player1.id) + "> was given " + str(xpEarned) + " exp for winning." + "\n" + "<@" + str(
                                player2.id) + "> lost " + str(xpLost) + " exp for losing.", color=discord.Color.blue())
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title="Player Healths:",
                                                description="<@" + str(player1.id) + ">**'s Health:** " + str(
                                                    player1Health) + "\n<@" + str(player2.id) + ">**'s Health:** " + str(
                                                    player2Health), color=discord.Color.red())
                            await ctx.send(embed=embed)
                            embed = discord.Embed(title="Game Finished!", description="<@" + str(player2.id) + "> won!", color=discord.Color.green())
                            await ctx.send(embed=embed)
                            xpEarned = int((startingHP * 3)/10)
                            xpLost = int((startingHP * 3) / 20)
                            print(xpEarned)
                            print(type(xpEarned))
                            giveXP(player2.id, xpEarned)
                            giveXP(player1.id, -xpLost)
                            embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                                player2.id) + "> was given " + str(xpEarned) + " exp for winning." + "\n" + "<@" + str(
                                player1.id) + "> lost " + str(xpLost) + " exp for losing.", color=discord.Color.blue())
                            await ctx.send(embed=embed)

                    else:
                        # switch turns

                        embed = discord.Embed(title="Turn change", description="It is now <@" + str(player1.id) + ">'s turn.",
                                            color=discord.Color.green())
                        await ctx.send(embed=embed)
                        turn = player1

            else:
                embed = discord.Embed(title="It's not your turn", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You are not in a duel currently. Use the '-duel' command to start one.", color=discord.Color.blue())
            await ctx.send(embed=embed)
    @duel.command()
    async def help(self, ctx):
        embed=discord.Embed(title="Duels", description="This bot's duels are pretty crappy but I was bored last year ok.", color=discord.Color.purple())
        embed.add_field(name="Shop Command", value="Now to see what new weapons and healing potions are available, you can use **'-shop'** to open the shop menu. This will display items available for purchase.")
        embed.add_field(name="Buy Command", value="To buy these items you can do **'-buy {item}'**. Watch out for spelling. For weapons it will ask you for a slot, 1 or 2. Don't make it complicated just enter '1' or '2' for the appropriate slot its not hard.")
        embed.add_field(name="Inventory Command", value="You can use **'-inv'** or **'-inventory'** to open your current inventory. This will display your current weapons and amount of healing potions.")
        embed.add_field(name="Duel Command", value="Now to actually duel someone you can do **'-duel @Person'**. They will have to accept, and the game explains itself from there on.")
        await ctx.send(embed=embed)
    

    

def setup(bot):
    bot.add_cog(DuelCommands(bot))