from discord.ext import commands
import discord
import pickle
import pymongo
from pymongo import MongoClient
import asyncio
import datetime
import os

mongo_cluster = os.getenv('mongo_cluster')

cluster = MongoClient(mongo_cluster)
db = cluster["AwesomeguyTwoPointO"]

global admin_list
admin_list = []



class MemberRoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.id == 743819073917550682:
            await member.kick(reason=reason)
            print(reason)
            embed=discord.Embed(title="L", description=f"Kicked {member.mention} because idk")
        else:
            embed = discord.Embed(title="You don't have perms to kick them", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    @commands.command()
    async def unban(self, ctx, member: discord.Member):
        #user = await self.bot.fetch_user(member.id)
        #guild = self.bot.get_guild(1)
        #await guild.unban(user)
        pass
    
    global muted_person
    
            
    
    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration = None, *, reason = None):
        if ctx.message.author.guild_permissions.administrator:
            global admin_list
            admin_role = discord.utils.get(ctx.guild.roles, id=882435188787916851)
            if admin_role in ctx.author.roles or ctx.author.id == 743819073917550682:
                guild = ctx.guild
                #FROST SERVER
                if guild.id == 882431857264828436:
                    
                    
                    mutedRole = discord.utils.get(guild.roles, name="muted L")
                    unit = duration[-1]
                    amount = duration[:-1]
                    if amount.isdigit() == False and unit.isalpha() == False:
                        reason = duration
                        duration = None


                    #check if person is admin, and if so remove admin and give muted
                    if admin_role in member.roles and ctx.author.id == 743819073917550682:
                        await member.remove_roles(admin_role)
                        await member.add_roles(mutedRole)
                        admin_list.append(member)
                        if duration is not None:
                            unit = duration[-1]
                            amount = int(duration[:-1])
                            print(unit, amount)
                            embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for {amount}{unit}.", colour=discord.Colour.purple())
                            if reason is not None:
                                embed.add_field(name="Reason", value=f"{reason}", inline=True)
                            await ctx.send(embed=embed)
                            if unit == "s":
                                wait = 1 * amount
                                await asyncio.sleep(wait)
                            elif unit == "m":
                                wait = 60 * amount
                                await asyncio.sleep(wait)
                            elif unit == "h":
                                wait = 3600 * amount
                                await asyncio.sleep(wait)
                            admin_list.remove(member)
                            await member.add_roles(admin_role)
                            await member.remove_roles(mutedRole)
                            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                            
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title="L", description=f"{member.mention} was muted because he was bad.", colour=discord.Colour.purple())
                            if reason is not None:
                                embed.add_field(name="Reason", value=f"{reason}", inline=True)
                            await ctx.send(embed=embed)
                    elif admin_role in member.roles and admin_role in ctx.author.roles:
                        pass
                    else:
                        if duration is not None:
                            unit = duration[-1]
                            amount = int(duration[:-1])
                            print(unit, amount)
                            embed = discord.Embed(title="L Muted", description=f"{member.mention} was muted for {amount}{unit}.", colour=discord.Colour.purple())
                            if reason is not None:
                                embed.add_field(name="Reason", value=f"{reason}", inline=True)
                            await ctx.send(embed=embed)
                            await member.add_roles(mutedRole)
                            if unit == "s":
                                wait = 1 * amount
                                await asyncio.sleep(wait)
                            elif unit == "m":
                                wait = 60 * amount
                                await asyncio.sleep(wait)
                            elif unit == "h":
                                wait = 3600 * amount
                                await asyncio.sleep(wait)
                            if mutedRole in member.roles:
                                await member.remove_roles(mutedRole)
                                embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title="L Muted", description=f"{member.mention} was muted because he was bad.", colour=discord.Colour.purple())
                            if reason is not None:
                                embed.add_field(name="Reason", value=f"{reason}", inline=True)
                            await ctx.send(embed=embed)
                            await member.add_roles(mutedRole)

                    
                    

                    
                elif ctx.author.id == 743819073917550682: 
                    guild = ctx.guild
                    mutedRole = discord.utils.get(guild.roles, name="Muted")

                    if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")
                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                    if duration is not None:
                        unit = duration[-1]
                        amount = int(duration[:-1])
                        print(unit, amount)
                        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted for {amount}{unit}.", colour=discord.Colour.purple())
                        await ctx.send(embed=embed)
                        await member.add_roles(mutedRole)
                        if unit == "s":
                            wait = 1 * amount
                            await asyncio.sleep(wait)
                        elif unit == "m":
                            wait = 60 * amount
                            await asyncio.sleep(wait)
                        elif unit == "h":
                            wait = 3600 * amount
                            await asyncio.sleep(wait)
                        if mutedRole in member.roles:
                            await member.remove_roles(mutedRole)
                            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                            await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.purple())
                        await ctx.send(embed=embed)
                        await member.add_roles(mutedRole)
                    
          

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.administrator:

            admin_role = discord.utils.get(ctx.guild.roles, id=882435188787916851)
            if admin_role in ctx.author.roles or ctx.author.id == 743819073917550682:
                guild = ctx.guild
                #FROSTIES
                if guild.id == 882431857264828436:
                    mutedRole = discord.utils.get(guild.roles, name="muted L")

                    if member in admin_list and ctx.author.id == 743819073917550682:
                        admin_list.remove(member)
                        await member.add_roles(admin_role)
                        
                        embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                        await ctx.send(embed=embed)
                        await member.remove_roles(mutedRole)
                    elif member in admin_list and ctx.author.id != 743819073917550682:
                        await ctx.send("You do not have perms to unmute this person")
                    else:
                        
                        embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                        await ctx.send(embed=embed)
                        await member.remove_roles(mutedRole)
                else:
                    mutedRole = discord.utils.get(guild.roles, name="Muted")

                    if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")

                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                    embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted.", colour=discord.Colour.purple())
                    await ctx.send(embed=embed)
                    await member.remove_roles(mutedRole)

    @commands.command()
    async def addrole(self, ctx, role: discord.Role, member: discord.Member):
        if ctx.author.id == 743819073917550682:
            await member.add_roles(role)
            await ctx.send(f"Successfully given {role.mention} to {member.mention}!")

    @commands.command()
    async def removerole(self, ctx, role: discord.Role, member: discord.Member):
        if ctx.author.id == 743819073917550682:
            await member.remove_roles(role)
            await ctx.send(f"Successfully removed {role.mention} from {member.mention}!")

    @commands.group(invoke_without_command=True)
    async def roles(self):
        pass
    @roles.command()
    async def start(self, ctx):
        if ctx.author.id == 743819073917550682:
            collection = db["reactionrole"]

            all_messages = []

            starting_message = ctx.message
            list_roles_message = await ctx.send("list roles")
            all_messages.append(starting_message)
            all_messages.append(list_roles_message)


            input_roles = []

            def is_correct(m):
                return m.author == ctx.author
            while True:
                msg = await self.bot.wait_for('message', check=is_correct)

                #print(msg.content)
                if msg.content == "done":
                    all_messages.append(msg)
                    print(input_roles)
                    print("done")
                    break
                
                msg_separate = msg.content.split(' ')
                input_roles.append((msg_separate[0])[3:-1])
                input_roles.append(msg_separate[1])
                print(input_roles)
                
                await msg.add_reaction("✅")
                all_messages.append(msg)
            
            for msg in all_messages:
                await msg.delete()
            
            roles_list = []
            emoji_list = []

            count = 0
            for item in input_roles:
                if count % 2 == 0:
                    roles_list.append(int(item))
                elif count % 2 == 1:
                    emoji_list.append(item)
                count += 1

            print(roles_list)
            print(emoji_list)

            desc_string = ""
            count = 0
            for id1 in roles_list:
                role = discord.utils.get(ctx.guild.roles, id=int(id1))
                emoji = emoji_list[count]
                desc_string += str(emoji) + " " + role.mention + "\n"
                count += 1

            embed = discord.Embed(
                title="React to get role",
                description=desc_string,
                color=discord.Color.blue(),
            )  # timestamp=datetime.now(),
            reaction_role_msg = await ctx.send(embed=embed)
            post1 = {"_id": reaction_role_msg.id, "roles": roles_list, "emojis": emoji_list}
            collection.insert_one(post1)
            
            for reaction in emoji_list:
                await reaction_role_msg.add_reaction(str(reaction))
    
    @roles.command()
    async def edit(self, ctx):
        if ctx.author.id == 743819073917550682:
            try:
                msg_id = ctx.message.reference.message_id
            except AttributeError:
                print("need to reply to a message")
                return
            collection = db["reactionrole"]
            guild = self.bot.get_guild(ctx.guild.id)
            bot_member = guild.get_member(self.bot.user.id)
            bot_roles = []
            for role in bot_member.roles:
                bot_roles.append(role)
            print(bot_roles)

            all_messages = []

            starting_message = ctx.message
            list_roles_message = await ctx.send("list roles")
            all_messages.append(starting_message)
            all_messages.append(list_roles_message)


            input_roles = []

            def is_correct(m):
                return m.author == ctx.author
            while True:
                msg = await self.bot.wait_for('message', check=is_correct)

                #print(msg.content)
                if msg.content == "done":
                    all_messages.append(msg)
                    print(input_roles)
                    print("done")
                    break

                msg_separate = msg.content.split(' ')
                input_roles.append((msg_separate[0])[3:-1])
                input_roles.append(msg_separate[1])

                await msg.add_reaction("✅")
                all_messages.append(msg)
            
            for msg in all_messages:
                await msg.delete()

            col1 = collection.find_one({"_id": msg_id})
            print(col1)
            current_roles = col1["roles"]
            current_emojis = col1["emojis"]
            print(current_roles) #good
            print(current_emojis) #good


            roles_list = []
            emoji_list = []
            count = 0
            for item in input_roles:
                if count % 2 == 0:
                    roles_list.append(item)
                elif count % 2 == 1:
                    emoji_list.append(item)
                count += 1
            print(roles_list)
            print(emoji_list)

            for role in roles_list:
                current_roles.append(int(role))
            for emoji in emoji_list:
                current_emojis.append(emoji)
            print(current_roles)
            print(current_emojis)


            collection.update_one({"_id": col1["_id"]}, {"$set": {"roles": current_roles, "emojis": current_emojis}})
            
            reaction_role_msg = await ctx.fetch_message(msg_id)
            for reaction in emoji_list:
                await reaction_role_msg.add_reaction(str(reaction))

            desc_string = ""
            count = 0
            for id1 in current_roles:
                role = discord.utils.get(ctx.guild.roles, id=int(id1))
                emoji = current_emojis[count]
                desc_string += str(emoji) + " " + role.mention + "\n"
                count += 1

            embed = discord.Embed(
                title="React to get role",
                description=desc_string,
                color=discord.Color.blue(),
            )
            await reaction_role_msg.edit(embed=embed)

    @roles.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Roles Setup and Usage", color=discord.Color.blue())
        embed.add_field(name="Creation", value="Use '-roles start' to create a reaction role. When listing roles and emojis use this format: {@Role}{:emoji:}. The bot will react with checkmarks when it is ready for the next role. Type 'done' when you're complete!", inline=True)
        embed.add_field(name="Editing", value="To edit an existing reaction role, reply to the reaction role message with '-roles edit'. When it prompts for roles to be added, use the same format and procedure as when creating a reaction role.", inline=True)
        
        await ctx.send(embed=embed)




    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.member.id)
        print(self.bot.user.id)
        

        
        emoji = str(payload.emoji.name)
        print(emoji)

        if payload.guild_id == 882431857264828436:
            
            if emoji == "⭐":
                collection = db["starboard"]
                channelid = payload.channel_id
                channel = self.bot.get_channel(channelid)
                reacted_id = payload.message_id
                reacted_msg = await channel.fetch_message(reacted_id)
                print(reacted_msg.content)
                author = reacted_msg.author

                dict1 = {}
                print(reacted_msg.reactions)
                for reactions in reacted_msg.reactions:
                    print(reactions)
                    print(reactions.count)
                    reaction = str(reactions)
                    count = int(reactions.count)
                    dict1[reaction] = count
                if dict1["⭐"] >= 3:
                    print("hi")
                    if len(reacted_msg.attachments) > 0:
                        col1 = collection.find_one({"_id": reacted_id})
                        num_stars = dict1["⭐"]

                        if col1 == None:
                            print("hi22")
                            embed=discord.Embed(description=f"{reacted_msg.content}", timestamp=datetime.datetime.utcnow(), color=discord.Color.purple())
                            embed.set_author(name=author.display_name, icon_url=author.avatar_url)
                            embed.add_field(name="Source:", value=f"[Jump to message]({reacted_msg.jump_url})", inline=True)
                            embed.set_image(url=f"{reacted_msg.attachments[0].url}")


                            starboard_channel = self.bot.get_channel(885345136517709835)
                            sent_msg = await starboard_channel.send(content=f"{num_stars} :star: <#{channelid}>", embed=embed)

                            post1 = {"_id": reacted_id, "sent_id": sent_msg.id}
                            collection.insert_one(post1)
                        else:
                            channel = self.bot.get_channel(885345136517709835)
                            msg = await channel.fetch_message(col1["sent_id"])
                            await msg.edit(content=f"{num_stars} :star: <#{channelid}>")
                    else:
                        col1 = collection.find_one({"_id": reacted_id})
                        num_stars = dict1["⭐"]

                        if col1 == None:
                            embed=discord.Embed(timestamp=datetime.datetime.utcnow(), color=discord.Color.purple())
                            embed.set_author(name=author.display_name, icon_url=author.avatar_url)
                            embed.add_field(name="Message:", value=f"{reacted_msg.content}", inline=False)
                            embed.add_field(name="Source:", value=f"[Jump to message]({reacted_msg.jump_url})", inline=False)


                            starboard_channel = self.bot.get_channel(885345136517709835)
                            sent_msg = await starboard_channel.send(content=f"{num_stars} :star: <#{channelid}>", embed=embed)

                            post1 = {"_id": reacted_id, "sent_id": sent_msg.id}
                            collection.insert_one(post1)
                        else:
                            channel = self.bot.get_channel(885345136517709835)
                            msg = await channel.fetch_message(col1["sent_id"])
                            await msg.edit(content=f"{num_stars} :star: <#{channelid}>")
    
        collection = db["reactionrole"]

        msg_id = None
        results = collection.find({"_id": payload.message_id})
        for result in results:
            msg_id = result["_id"]
            message_info = result
        
        if msg_id is not None:
            member = payload.member
            guild = member.guild
            print(member)
            print(guild)

            emoji_list = message_info['emojis']
            roles_list = message_info['roles']

            emoji = payload.emoji.name
            count = 0
            for reaction in emoji_list:
                if emoji == reaction: 
                    role = discord.utils.get(guild.roles, id=int((roles_list[count])))
                    await member.add_roles(role)
                    print(f"Successfully given {role.mention} to {member.mention}!")
                    print(role)
                count += 1
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        #starboard
        emoji = str(payload.emoji.name)
        
        if payload.guild_id == 882431857264828436:
            if emoji == "⭐":
                collection = db["starboard"]
                channelid = payload.channel_id
                channel = self.bot.get_channel(channelid)
                reacted_id = payload.message_id
                reacted_msg = await channel.fetch_message(reacted_id)
                print(reacted_msg.content)

                dict1 = {}
                print(reacted_msg.reactions)
                for reactions in reacted_msg.reactions:
                    print(reactions)
                    print(reactions.count)
                    reaction = str(reactions)
                    count = int(reactions.count)
                    dict1[reaction] = count
                print(dict1)
                try:
                    if dict1["⭐"] >= 3:
                        col1 = collection.find_one({"_id": reacted_id})
                        num_stars = dict1["⭐"]

                        channel = self.bot.get_channel(885345136517709835) 
                        msg = await channel.fetch_message(col1["sent_id"])
                        await msg.edit(content=f"{num_stars} :star: <#{channelid}>")
                    else:
                        col1 = collection.find_one({"_id": reacted_id})
                        channel = self.bot.get_channel(885345136517709835)
                        msg = await channel.fetch_message(col1["sent_id"])
                        await msg.delete()
                        collection.find_one_and_delete({"_id": reacted_id})
                except KeyError:
                    print("rip")

        

        #reaction role
        collection = db["reactionrole"]

        msg_id = None
        results = collection.find({"_id": payload.message_id})
        for result in results:
            msg_id = result["_id"]
            message_info = result
        
        if msg_id is not None:
            guild = await(self.bot.fetch_guild(payload.guild_id))
            emoji = payload.emoji.name
            print(emoji)
            print(guild)

            emoji_list = message_info['emojis']
            roles_list = message_info['roles']

            count = 0
            for reaction in emoji_list:
                if emoji == reaction: 
                    role = discord.utils.get(guild.roles, id=int((roles_list[count])))
                    print(role)
                count += 1
            member = await(guild.fetch_member(payload.user_id))
            if member is not None:
                await member.remove_roles(role)
                print(f"{member} was successfully removed from {role}")
            else:
                print("Member is bad not found")
        

    
    

def setup(bot):
    bot.add_cog(MemberRoleCommands(bot))


