from discord.ext import commands
import discord
import asyncio
import typing

admin_list2 = []

global muted_ethanp
muted_ethanp = False
skulling_eddie = False


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member) # Change accordingly


    @commands.command()
    async def dm(self, ctx, member: discord.Member, *, content):
        print(member)
        channel = await member.create_dm()
        print(channel)
        await channel.send(content)
        embed = discord.Embed(title="Message sent", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *, content):
        print(content)
        if ctx.author.id == 743819073917550682:
            if content == "@everyone" or content == "@here" or "<@" in content:
                await ctx.send("stfu")
            elif (content == "." or content == "e" or content == "sees" or content == "i-") and ctx.author.id != 743819073917550682:
                if ctx.guild.id == 882431857264828436: #frost server
                    mutedRole = discord.utils.get(ctx.guild.roles, name="muted L")
                    admin_role = discord.utils.get(ctx.guild.roles, id=882435188787916851)

                    member = ctx.author
                    global admin_list2

                    if member.id != 743819073917550682:
                        #check if person is admin, and if so remove admin and give muted

                        if admin_role in member.roles:
                            await member.remove_roles(admin_role)
                            await member.add_roles(mutedRole)
                            admin_list2.append(member)
                                
                            embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for 1m.", colour=discord.Colour.purple())
                            embed.add_field(name="Reason", value="Tried muting me smh", inline=True)
                            await ctx.send(embed=embed)
                            await asyncio.sleep(60)
                            admin_list2.remove(member)
                            await member.add_roles(admin_role)
                            await member.remove_roles(mutedRole)
                            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                            await ctx.send(embed=embed)
                        else:
                            await member.add_roles(mutedRole)
                            embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for 1m.", colour=discord.Colour.purple())
                            embed.add_field(name="Reason", value="Tried muting me smh", inline=True)
                            await ctx.send(embed=embed)
                            await asyncio.sleep(60)
                            await member.remove_roles(mutedRole)
                            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                            await ctx.send(embed=embed)
            else:
                await ctx.send(content)
        else:
            await ctx.send("no I won't")
    
    @commands.command()
    async def link(self, ctx, link, *, top):
        if ctx.author.id == 743819073917550682:
            await ctx.message.delete()
            print(link)
            embed = discord.Embed(title=f"{top}", description=f"[{top}]({link})", color=discord.Color.purple())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def spam(self, ctx, number, *, content):
        if ctx.author.id == 743819073917550682 or ctx.author.id == 535893497388204047 or ctx.author.id == 719316102710296739:
            if int(number) <= 50:
                print(content)
                count = 0
                while count < int(number):
                    await ctx.send(content)
                    await asyncio.sleep(0.2)
                    count += 1
            else:
                await ctx.send("other people need to use the bot andrew")
    
    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Bruv stop abusing me wait for 15 seconds", colour=discord.Colour.red())
            await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, amount: str):
        if ctx.author.id == 743819073917550682 or ctx.author.id == 535893497388204047:
            if amount == 'all':
                await ctx.channel.purge()
            else:
                await ctx.channel.purge(limit=(int(amount) + 1))
        else:
            embed = discord.Embed(title="No you can't abuse it", color=discord.Color.red())
            await ctx.send(embed=embed)

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="You gotta put what you want me to say", colour=discord.Colour.dark_red())
            await ctx.send(embed=embed)

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="You gotta put who you want to send to, and what you want me to say to them",
                                  colour=discord.Colour.dark_red())
            await ctx.send(embed=embed)

    
    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()
    
    
    @commands.command()
    async def bully_ethanp(self, ctx):
        global muted_ethanp
        if ctx.author.id == 743819073917550682:
            if muted_ethanp == True:
                muted_ethanp = False
            elif muted_ethanp == False:
                muted_ethanp = True
            print(muted_ethanp)
            await ctx.send(f"ok {muted_ethanp}")
        else:
            await ctx.send("no only cool people ww can use it")

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        global muted_ethanp
        global skulling_eddie
        
        if msg == "i love you awesomeguy":
            await message.channel.send("❤️💟❣️😍😻♥️🧡💛💚💙💜🤍🤎🖤💌💘👨‍❤️‍👨💗💓💕💖", reference=message)
        
        if "skull me up" in msg and message.author.id == 834862357775515658: #eddie
            skulling_eddie = True
            await message.add_reaction("💀")
            print("skulling eddie" + skulling_eddie)
        
        if msg == "stop skulling" and message.author.id == 834862357775515658: #eddie
            skulling_eddie = False
            print("skulling eddie" + skulling_eddie)
        if skulling_eddie and message.author.id == 834862357775515658: #eddie
            await message.add_reaction("💀")

        if message.author.id == 615676477912121393 and muted_ethanp == True and message.guild.id == 882431857264828436: #frost and ethan p
            mutedRole = discord.utils.get(message.guild.roles, name="muted L")
            member = message.author

            embed = discord.Embed(title="L", description=f"{member.mention} was muted.", colour=discord.Colour.purple())
            embed.add_field(name="Reason", value="he's ethan park.", inline=True)
            await message.channel.send(embed=embed)

            await member.add_roles(mutedRole)




        if msg == "." or msg == "e" or msg == "sees" or msg == "i-":
            if message.guild.id == 882431857264828436: #frost server
                mutedRole = discord.utils.get(message.guild.roles, name="muted L")
                admin_role = discord.utils.get(message.guild.roles, id=882435188787916851)

                member = message.author
                global admin_list2

                if member.id != 743819073917550682:
                    #check if person is admin, and if so remove admin and give muted

                    if admin_role in member.roles:
                        await member.remove_roles(admin_role)
                        await member.add_roles(mutedRole)
                        admin_list2.append(member)
                            
                        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for 1m.", colour=discord.Colour.purple())
                        embed.add_field(name="Reason", value="Said one of the unforgivable words.", inline=True)
                        await message.channel.send(embed=embed)
                        await asyncio.sleep(60)
                        admin_list2.remove(member)
                        await member.add_roles(admin_role)
                        await member.remove_roles(mutedRole)
                        embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                        await message.channel.send(embed=embed)
                    else:
                        await member.add_roles(mutedRole)
                        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for 1m.", colour=discord.Colour.purple())
                        embed.add_field(name="Reason", value="Said one of the unforgivable words.", inline=True)
                        await message.channel.send(embed=embed)
                        await asyncio.sleep(60)
                        await member.remove_roles(mutedRole)
                        embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                        await message.channel.send(embed=embed)
                    

        if "gottem" in msg or "boom4" in msg or "pog" in msg or "caillou" in msg or "yeet" in msg or "didnt ask" in msg or "did i ask" in msg or "sus" in msg or "gagnon" in msg or "bofa" in msg or "pudding" in msg or "phillip" in msg or "goblin" in msg or "no u" in msg:
            # Getting the ratelimit left
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None: #means user is good and is allowed to send
                if "gottem" in msg:
                    if message.guild.id == 882431857264828436: #frost
                        embed = discord.Embed(title="Oh got ||his ass|| huh what", color=discord.Color.blue())
                        embed.set_footer(text="-Patreek")
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Oh gottem good", color=discord.Color.blue())
                        await message.channel.send(embed=embed)

                if "boom4" in msg:
                    embed = discord.Embed(title="The Story of the Boom4s", description='There once was 4 booms then one booms decided to betray'
                                            ' to other booms and this boom was named boom4. Boom4 burnt'
                                            ' down the boom family house and stole all their chickens maki'
                                            'ng billions of dollars. No one liked boom4. Now whenever someone '
                                            'says the name boom4 they feel like burning down a house and stealing'
                                            ' chickens. Beware of these people.', color=discord.Color.blue())
                    await message.channel.send(embed=embed)

                if "pog" in msg:
                    embed = discord.Embed(title="POGCHAMP", color=discord.Color.blue())
                    await message.channel.send(embed=embed)

                if "caillou" in msg:
                    embed = discord.Embed(title="OMG CAILLOU MY FAVORITE TV SHOW AHHHHHHH")
                    await message.channel.send(embed=embed)

                if "yeet" in msg:
                    embed = discord.Embed(title="Yeet indeed", color=discord.Color.blue())
                    await message.channel.send(embed=embed)

                if "didnt ask" in msg or "did i ask" in msg:
                    embed = discord.Embed(title="Didn't ask for you not to ask", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                
                if "sus" in msg:
                    embed = discord.Embed(title=":rofl: :joy: :zany_face: :flushed: :weary: :ok_hand: :tired_face: :laughing:", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                if "gagnon" in msg:
                    embed = discord.Embed(title="gagnon deez nuts HA GOTTEM", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                
                if "bofa" in msg:
                    embed = discord.Embed(title="bofa deez nuts HA GOTTEM", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                if "pudding" in msg:
                    embed = discord.Embed(title="pudding deez nuts HA GOTTEM", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                if "phillip" in msg:
                    embed = discord.Embed(title="phillip deez nuts HA GOTTEM", color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                if "goblin" in msg:
                    embed = discord.Embed(title="goblin deez nuts HA GOTTEM", color=discord.Color.blue())
                    await message.channel.send(embed=embed)

                #if "bruh" in msg:
                    #embed = discord.Embed(title="Bruh momento")
                    #await message.channel.send(embed=embed)
                if "no u" in msg:
                    test = '{0.author.mention}'.format(message)
                    embed = discord.Embed(title='No u', description=test, color=discord.Color.blue())
                    await message.channel.send(embed=embed)

            else: #means user is bad and is NOT allowed to send
                print("cool down")


    


def setup(bot):
    bot.add_cog(MessageCommands(bot))