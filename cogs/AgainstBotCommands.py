from discord.ext import commands
import discord
import asyncio
from secrets import randbelow
from itertools import islice
from pymongo import MongoClient
import pymongo

from dotenv import load_dotenv
import os

load_dotenv()
mongo_cluster = os.getenv('mongo_cluster')

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

def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)


class AgainstBotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.group(invoke_without_command=True)
    async def guess(self, ctx):
        if ctx.author == self.bot.user:
            return
        number = randint(1,100)
        guess = 2
        await asyncio.sleep(1)
        embed = discord.Embed(title="Guess a number between 1 and 100. You have 3 guesses.", color=discord.Color.blue())
        await ctx.send(embed=embed)
        while guess != -1:
            print(guess)
            print(number)
            def is_correct(m):
                print(type(m.content))
                return m.author == ctx.author and (m.content.isdigit() or m.content == "quit")
            try:
                msg = await self.bot.wait_for('message', check=is_correct, timeout=30.0)
                print(msg)
            
                if msg.content == "quit":
                    embed = discord.Embed(title="You quit.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    break
                else:
                    attempt = int(msg.content)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Time's up", description="You were too slow bruh", color=discord.Color.red())
                await ctx.send(embed=embed)


            if attempt > number:
                if guess == 0:
                    print("endlow")
                    embed = discord.Embed(title="L incorrect, the correct number was " + str(number),
                                        color=discord.Color.red())
                    await ctx.send(embed=embed)
                    if number - 5 <= attempt <= number + 5:
                        giveXP(ctx.author.id, 3)
                        embed = discord.Embed(title="You received 3 exp for being kinda close",
                                            color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        break
                    else:
                        giveXP(ctx.author.id, -5)
                        embed = discord.Embed(title="You lost 5 exp for being bad",
                                            color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        break
                else:
                    embed = discord.Embed(title="Incorrect. You have " + str(guess) + " guesses left...", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    #await asyncio.sleep(1)
                    await ctx.send('Try going **lower**')
                    await asyncio.sleep(0.5)
                    guess -= 1
            elif attempt < number:
                if guess == 0:
                    print("endhigh")
                    print(attempt)
                    print(type(attempt))
                    embed = discord.Embed(title="L incorrect, the correct number was " + str(number), color=discord.Color.red())
                    await ctx.send(embed=embed)
                    if number - 5 <= attempt <= number + 5:
                        giveXP(ctx.author.id, 3)
                        embed = discord.Embed(title="You received 3 exp for being kinda close", color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        break
                    else:
                        giveXP(ctx.author.id, -5)
                        embed = discord.Embed(title="You lost 5 exp for being bad",
                                            color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        break
                else:
                    embed = discord.Embed(title="Incorrect. You have " + str(guess) + " guesses left...", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    #await asyncio.sleep(1)
                    await ctx.send('Try going **higher**')
                    await asyncio.sleep(0.5)
                    guess -=1
            elif attempt == number:
                embed = discord.Embed(title="You actually guessed it! What a gamer!", color=discord.Color.green())
                await ctx.send(embed=embed)
                giveXP(ctx.author.id, 15)
                embed = discord.Embed(title="You received 15 exp for guessing correctly!", color=discord.Color.blue())
                await ctx.send(embed=embed)
                print("ezzz")
                break
    @guess.command()
    async def help(ctx):
        embed=discord.Embed(title="Guessing Game", description="Guess is guessing game." + "\n" + "Using the command '-guess', the bot will give you 3 chances to guess a number 1-100, and you can respond with an integer to guess.\nYou can also respond with 'quit' to quit the game.", color=discord.Color.blue())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AgainstBotCommands(bot))