from secrets import randbelow
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.commands import BucketType
import discord
from PIL import Image
from io import BytesIO
import requests
import json
import os
import requests
from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption
import asyncio


err_color = discord.Color.red()
color = 0x0da2ff

def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        

    @commands.command()
    async def random(self, ctx, min, max):
        # message = await ctx.send()
        minRe = min.replace(',', '')
        print("String after removal of ',': " + minRe)
        minInt = int(minRe)
        maxInt = int(max)
        randomInt = randint(minInt, maxInt)
        # print(randomInt)
        embed = discord.Embed(title=randomInt, color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx):
        coin = randint(0, 1)
        if coin == 0:
            print("heads")
            embed = discord.Embed(title="It landed heads", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            print("tails")
            embed = discord.Embed(title="It landed tails", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx):
        die = randint(1, 6)
        embed = discord.Embed(title="It rolled a " + die, color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def inspire(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        get_quote = json_data[0]['q'] + " -" + json_data[0]['a']
        quote = get_quote
        embed = discord.Embed(title="Hopefully Inspirational Quote", description=quote, color=discord.Color.random())
        await ctx.channel.send(embed=embed)

    

    @commands.command()
    async def poll(self, ctx, *, msg):
        channel = ctx.channel
        try:
            op1, op2 = msg.split("or")
            txt = f"React with ✅ for {op1} or ❎ for {op2}"
        except:
            await channel.send("Format '-poll Option 1 or Option 2")

        embed = discord.Embed(title="Poll", description=txt, color=discord.Color.blue())
        msg = await channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")
        await ctx.message.delete()

    @commands.command()
    async def wanted(self, ctx, user: discord.User = None):
        if user == None:
            user = ctx.author
            print(user)
        
        print(user)

        wanted = Image.open("wantedImg.jpg")

        #await ctx.author.avatar_url.save("avatar1.jpg")
        #file = discord.File(fp=filename)
        #await ctx.send("Enjoy :>", file=file)

        asset = user.avatar_url_as(size=128)
        await asset.save("pfp.jpg")
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        #avatar = Image.open("avatar1.jpg")

        pfp = pfp.resize((276, 276))

        wanted.paste(pfp, (92, 234))

        wanted.save("profile.jpg")

        await ctx.send(file=discord.File("profile.jpg"))
    


    @commands.command()
    async def urban(self, ctx, *, word):
        url = f"https://api.urbandictionary.com/v0/define?term={word}"

        response = requests.request("GET", url)
        try:
            def_num = len(response.json()['list'])
            print(def_num)
        except KeyError:
            embed=discord.Embed(title="Error", description="An error occurred (request ID b7abadd0-c8d0-441c-ac69-5806d219db8d)", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        

        if def_num == 1 or def_num == 0:
            multiple_options = False

        else:
        
            dropdown = []
            count = 0
            while count <= def_num - 1:
                if count == 0:
                    label_msg = "1st Definition"
                elif count == 1:
                    label_msg = "2nd Definition"
                elif count == 2:
                    label_msg = "3rd Definition"
                else:
                    label_msg = f"{count+1}th Definition"


                dropdown.append(SelectOption(label=label_msg, value=count, description=f"👍: {response.json()['list'][count]['thumbs_up']} 👎: {response.json()['list'][count]['thumbs_down']}"))
                count += 1
                
            embed=discord.Embed(title="Multiple Options", description="There are multiple available definitions for this word. Use the dropdown below to select one.", color=discord.Color.blue())
            await ctx.send(embed=embed,
            components=[Select(placeholder="select something!", options=dropdown)])
            
            multiple_options = True

        
        if multiple_options == True:
            def check(res):
                return ctx.author == res.user and res.channel == ctx.channel

            try:
                interaction = await self.bot.wait_for("select_option", check=check, timeout=30)
                
                #value = interaction.component[0].value
                value = interaction.values[0]
                #value = lambda i: i.component[0].value
                #print(value)
                def_index = int(value)

                definition = response.json()['list'][def_index]['definition']
                word = response.json()['list'][def_index]['word']
                author = response.json()['list'][def_index]['author']
                examples = response.json()['list'][def_index]['example']
                upvotes = response.json()['list'][def_index]['thumbs_up']
                downvotes = response.json()['list'][def_index]['thumbs_down']

                date_weird = response.json()['list'][def_index]['written_on']
                date_num = str(date_weird)[:10]
                yearnum, monthnum, daynum = tuple(date_num.split('-'))
                date = f"{monthnum}/{daynum}/{yearnum}"


                embed=discord.Embed(title=f"{word}", color=discord.Color.purple())
                embed.add_field(name="Definition", value=f"{definition}", inline=False)
                embed.add_field(name="Example(s)", value=f"{examples}", inline=False)
                embed.add_field(name="Likes / Dislikes", value=f"👍: {upvotes} 👎: {downvotes}", inline=False)

                embed.set_footer(text=f"By {author} on {date}")
                try:
                    await interaction.respond(content="", type=7, components=[], embed=embed)
                except HTTPException:
                    await ctx.send("bro this guys definition was so bad discord cant even handle it")
                    await ctx.send("test")
                    await ctx.send()

            except TimeoutError:
                print("timed out")
        else:
            if def_num == 1:
                definition = response.json()['list'][0]['definition']
                word = response.json()['list'][0]['word']
                author = response.json()['list'][0]['author']            
                examples = response.json()['list'][0]['example']
                upvotes = response.json()['list'][0]['thumbs_up']
                downvotes = response.json()['list'][0]['thumbs_down']

                date_weird = response.json()['list'][0]['written_on']
                date_num = str(date_weird)[:10]
                yearnum, monthnum, daynum = tuple(date_num.split('-'))
                date = f"{monthnum}/{daynum}/{yearnum}"


                
                embed=discord.Embed(title=f"{word}", color=discord.Color.purple())
                embed.add_field(name="Definition", value=f"{definition}", inline=False)
                embed.add_field(name="Example(s)", value=f"{examples}", inline=False)
                embed.add_field(name="Likes / Dislikes", value=f"👍: {upvotes} 👎: {downvotes}", inline=False)

                embed.set_footer(text=f"By {author} on {date}")

                await ctx.send(embed=embed)
            
            elif def_num == 0:
                embed=discord.Embed(title="Error", description="There were no definitions found for query.", color=discord.Color.red())

    @commands.command()
    async def stats(self, ctx, player="Awesomeguyy"):
        url = f"https://karma-25.uc.r.appspot.com/player/{player}"

        response = requests.request("GET", url)

        print(response.json()['success'])

        if response.json()['success']:
            username = response.json()["mojang"]['username']
            
            coins = response.json()["player"]['stats']['Bedwars']["coins"]
            coins = f'{coins:,}'
            ws = response.json()["player"]['stats']['Bedwars']["winstreak"]
            ws = f'{ws:,}'
            level = response.json()["player"]['achievements']['bedwars_level']
            level = f'{level:,}'
            
            dias = response.json()["player"]['stats']['Bedwars']["diamond_resources_collected_bedwars"]
            dias = f'{dias:,}'
            ems = response.json()["player"]['stats']['Bedwars']["emerald_resources_collected_bedwars"]
            ems = f'{ems:,}'
            iron = response.json()["player"]['stats']['Bedwars']["iron_resources_collected_bedwars"]
            iron = f'{iron:,}'
            gold = response.json()["player"]['stats']['Bedwars']["gold_resources_collected_bedwars"]
            gold = f'{gold:,}'

            final_kills = response.json()["player"]['stats']['Bedwars']["final_kills_bedwars"]
            final_deaths = response.json()["player"]['stats']['Bedwars']["final_deaths_bedwars"]
            fkdr = final_kills/final_deaths
            final_kills = f'{final_kills:,}'
            final_deaths = f'{final_deaths:,}'

            wins = response.json()["player"]['stats']['Bedwars']["wins_bedwars"]
            losses = response.json()["player"]['stats']['Bedwars']["losses_bedwars"]
            wl = wins/losses
            wins = f'{wins:,}'
            losses = f'{losses:,}'

            beds = response.json()["player"]['stats']['Bedwars']["beds_broken_bedwars"]
            beds = f'{beds:,}'

            embed = discord.Embed(title=f"{username}'s Bedwars Stats", description=f"**Level:** {level}\n**Winstreak:** {ws}\n**Coins:** {coins}\n\n**Final Kills:** {final_kills}\n**Final Deaths:** {final_deaths}\n**FKDR:** {round(fkdr, 2)}\n**Wins:** {wins}\n**Losses:** {losses}\n**Win/Loss:** {round(wl, 2)}\n**Beds Broken:** {beds}", color=discord.Color.blue())
            #embed.add_field(name="Resources", value=f"**Diamonds Collected:** {dias}\n**Emeralds Collected:** {ems}\n**Iron Collected:** {iron}\n**Gold Collected:** {gold}", inline=True)
            #embed.add_field(name="Sweaty", value=f"**Final Kills:** {final_kills}\n**Final Deaths:** {final_deaths}\n**FKDR:** {round(fkdr, 2)}\n**Wins:** {wins}\n**Losses:** {losses}\n**Win/Loss:** {round(wl, 2)}\n**Beds Broken:** {beds}", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Error", description="No player found with that username.", color=discord.Color.red())




def setup(bot):
    bot.add_cog(FunCommands(bot))
