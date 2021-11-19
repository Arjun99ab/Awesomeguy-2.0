import os
from secrets import randbelow
import secrets
from PIL import Image
from io import BytesIO
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
import asyncio


load_dotenv()
awesomeguy_token = os.getenv('awesomeguy_token')

player1 = ""
player2 = ""

intents = discord.Intents.default()
intents.members = True
intents.presences = True


bot=commands.Bot(command_prefix='-', intents=intents)
bot.remove_command('help')

ddb = DiscordComponents(bot)

#rs = RandomStuff(async_mode=True)

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



######################################################################
#                       Bot and User Startup Commands                #
######################################################################

status = ['-help', '-tictactoe', 'absolutely nothing']

@bot.event
async def on_ready():
    change_status.start()
    print(bot.user.name + ' has connected to Discord!')
    user = discord.utils.get(bot.get_all_members(), id='743819073917550682')
    print(user)

    if user is not None:
        await bot.send_message(user, "A message for you")
    else:
        print("bad")
        # Your bot can't see the user, and therefore wouldn't have permission to DM them anyway.
        # Choose how you want to handle this here.
    #await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('-help'))
    await bot.get_channel(847492628701511680).send("Bot is online")

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=choice(status)))

ROLE = "new role"

@bot.event
async def on_member_join(member):
    await member.send("Welcome! I just gave you role 'No School?'. To assign yourself to a school go to the #roles channel!")
    role = discord.utils.get(member.guild.roles, name=ROLE)
    await member.add_roles(role)
    print(f"{member} was given {role}")
    print("gg")

@bot.event
async def on_member_leave(member):
    await member.send("Bad")
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



######################################################################
#                       Help and Updatelog Commands                  #
######################################################################

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Use the '-' prefix before every command." + "\n" + "**Check out the update log for info and stuff by using '-updatelog'.**", color=discord.Color.blue())
    embed.add_field(name="Word Responses", value="If you say certain words, the bot will respond. Custom responses soon...",inline=True)
    embed.add_field(name="Fun Commands", value="-8ball, -inspire, -say, -dm, -random, -flip, -wanted", inline=True)
    embed.add_field(name="Game Commands", value="-tictactoe, -rps, guess" + "\n" + "**Read more about these below**", inline=True)

    embed.add_field(name="How to Play Tic Tac Toe", value="Tic Tac Toe, pretty self explanatory." + "\n" + "Using the command '-tictactoe' followed by mentioning 2 users (e.g. -tictactoe @Awesomeguy @Awesomeguy 2.0) will start a game of Tic Tac Toe with those two players." + "\n" + "Use '-place' followed by a place number to place an :regional_indicator_x: or :o2: in that corresponding box." + "\n" + "A board of the key to the place numbers will be printed at the beginning of each game, as well to the right.", inline=True)
    embed.add_field(name="Tic Tac Toe Correspondence", value=":one: :two: :three: | :white_large_square: :white_large_square: :white_large_square:" + "\n" ":four: :five: :six: | :white_large_square: :white_large_square: :white_large_square:" + "\n" + ":seven: :eight: :nine: | :white_large_square: :white_large_square: :white_large_square:" + "\n")
    embed.add_field(name="How to Play RPS", value="RPS stands for Rock Paper Scissors, a commonly known game." + "\n" + "Using the command '-rps', the bot will countdown 'Rock', 'Paper', 'Scissors', and 'Shoot!'." + "\n" + "When it says shoot, you job is to type rock, paper, or scissors, and the bot will also generate one of them, and see who is the winner." + "\n" + "This was the first game project which is why it's lame good day", inline=True)
    #embed.add_field(name="How to Play 'Minecraft'", value="This is absolute garbage ok it's not good don't expect it to be an exact replica of actual Minecraft." + "\n" + "Using the command '-minecraft', the bot will launch a 2D 'Minecraft'. You can move left and right by typing 'left' and 'right'." + "\n" + "**NOTE:** This is insanely early beta meaning that I literally programmed it yesterday so it sucks and glitches. If people actually use it I'll make it completely functional.", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def updatelog(ctx):
    embed = discord.Embed(title="Awesomeguy 2.0 Update Log", description="Hello this is where I'll be posting updates even though no one will read this.", color=discord.Color.blue())
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
#                       Message Type Testing                         #
######################################################################

@bot.command()
async def embed(ctx, title="a ", description="a ", footer=None):
    embed = discord.Embed(title=title, description=description, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)

@bot.command()
async def edit(ctx):
    message = await ctx.author.send("hello")
    time.sleep(2)
    await message.edit(content="new content")
    await ctx.author.send("aaaa")

@bot.command()
async def testembed(ctx):
    file = discord.File("wanted2.jpg")
    e = discord.Embed(color=discord.Color.blue())
    e.set_image(url="attachment://wanted2.jpg")
    await ctx.send(file=file, embed=e)

@bot.command()
async def audio(ctx):
    await ctx.send(file=discord.File("ExampleAudioFile.mp3"))


######################################################################
#                       Bot Message Commands                    #
######################################################################

@bot.command()
async def dm(ctx, member: discord.Member, *, content):
    print(member)
    channel = await member.create_dm()
    print(channel)
    await channel.send(content)
    embed = discord.Embed(title="Message sent", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, content):
    print(content)
    embed = discord.Embed(title=content, color=discord.Color.dark_magenta())
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) + 1))



######################################################################
#                       General Functions                            #
######################################################################

def randint(a, b):
    "Return random integer in range [a, b], including both end points."
    return a + randbelow(b - a + 1)



######################################################################
#                       Member and Role Commands                     #
######################################################################

@bot.command()
@commands.has_role('new role')
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Successfully kicked {member.mention}!")

@bot.command()
async def addrole(ctx, role: discord.Role, member: discord.Member):
    await member.add_roles(role)
    await ctx.send(f"Successfully given {role.mention} to {member.mention}!")

@bot.command()
async def removerole(ctx, role: discord.Role, member: discord.Member):
    await member.remove_roles(role)
    await ctx.send(f"Successfully removed {role.mention} from {member.mention}!")
@bot.event
async def on_raw_reaction_add(payload):
    MessageID = 848700516880220170

    if MessageID == payload.message_id:
        member = payload.member
        guild = member.guild
        print(member)
        print(guild)

        emoji = payload.emoji.name
        if emoji == '🟦':  # blue
            role = discord.utils.get(guild.roles, name="frosties")
        elif emoji == '🟧':  # orange
            role = discord.utils.get(guild.roles, name="cabin john uh")
        elif emoji == '🟩':  # green
            role = discord.utils.get(guild.roles, name="takoma ;-;")
        elif emoji == '🟥':  # red
            role = discord.utils.get(guild.roles, name="east earn")
        elif emoji == '🟨':  # yellow
            role = discord.utils.get(guild.roles, name="hoover?")

        await member.add_roles(role)
        print(role)
        print(f"{member} was successfully given {role}")

@bot.event
async def on_raw_reaction_remove(payload):
    MessageID = 848700516880220170

    if MessageID == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        if emoji == '🟦': #blue
            role = discord.utils.get(guild.roles, name="frosties")
        elif emoji == '🟧': #orange
            role = discord.utils.get(guild.roles, name="cabin john uh")
        elif emoji == '🟩': #green
            role = discord.utils.get(guild.roles, name="takoma ;-;")
        elif emoji == '🟥': #red
            role = discord.utils.get(guild.roles, name="east earn")
        elif emoji == '🟨': #yellow
            role = discord.utils.get(guild.roles, name="hoover?")
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
            print(f"{member} was successfully removed from {role}")
        else:
            print("Member is bad not found")



@bot.command()
async def roleMessage(ctx):
    frosties = discord.utils.get(ctx.guild.roles, name='frosties')
    cabin = discord.utils.get(ctx.guild.roles, name='cabin john uh')
    takoma = discord.utils.get(ctx.guild.roles, name='takoma ;-;')
    east = discord.utils.get(ctx.guild.roles, name='east earn')
    hoover = discord.utils.get(ctx.guild.roles, name='hoover?')

    embed = discord.Embed(
        title="React to get role",
        description=f"🟦 {frosties.mention}\n🟧 {cabin.mention}\n🟩 {takoma.mention}\n🟥 {east.mention}\n🟨 {hoover.mention}",
        color=discord.Color.blue(),
    ) #timestamp=datetime.now(),
    msg = await ctx.send(embed=embed)

    #blue square
    await msg.add_reaction('🟦')
    #orange square
    await msg.add_reaction('🟧')
    #green
    await msg.add_reaction('🟩')
    #red
    await msg.add_reaction('🟥')
    #yellow
    await msg.add_reaction('🟨')

    await ctx.message.add_reaction('✅')



######################################################################
#                       Fun Commands                                 #
######################################################################

@bot.command()
async def random(ctx, min, max):
    #message = await ctx.send()
    minRe = min.replace(',', '')
    print("String after removal of ',': " + minRe)
    minInt = int(minRe)
    maxInt = int(max)
    randomInt = randint(minInt, maxInt)
    #print(randomInt)
    embed = discord.Embed(title=randomInt, color=discord.Color.random())
    await ctx.send(embed=embed)

@bot.command()
async def flip(ctx):
    coin = randint(0, 1)
    if coin == 0:
        print("heads")
        embed = discord.Embed(title="It landed heads", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        print("tails")
        embed = discord.Embed(title="It landed tails", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def roll(ctx):
    die = randint(1, 6)
    embed = discord.Embed(title="It rolled a " + die, color=discord.Color.random())
    await ctx.send(embed=embed)

@bot.command()
async def inspire(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    get_quote = json_data[0]['q'] + " -" + json_data[0]['a']
    quote = get_quote
    embed = discord.Embed(title="Hopefully Inspirational Quote", description=quote, color=discord.Color.random())
    await ctx.channel.send(embed=embed)

@bot.command()
async def wanted(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
        print(user)

    wanted = Image.open("wantedImg.jpg")

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((276, 276))

    wanted.paste(pfp, (92, 234))

    wanted.save("profile.jpg")

    await ctx.send(file=discord.File("profile.jpg"))

@bot.command()
async def pokemon(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
        print(user)

    pokemon = Image.open("cardTemplate.png")

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((358, 257))

    pokemon.paste(pfp, (48, 71))

    pokemon.save("pokemon.png")

    await ctx.send(file=discord.File("pokemon.png"))


######################################################################
#                       Rank System                                 #
######################################################################

def writeRank(file, content):
    file.write(content + "\n")

def readRank(file, min, max):
    with open(file, 'r') as f:
        print("hola")
        for line in islice(f, min, max+1):
            print(line, end='')

def giveXP(id, xpInput):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("rankinfo", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("rankinfo", "r")
    list_of_lines = f.readlines()
    original_xp = int(list_of_lines[line_number + 1])
    xpInt = xpInput
    xp = str(xpInt + original_xp) + "\n"
    list_of_lines[line_number + 1] = xp
    print(type(list_of_lines))
    #list_of_lines.append("\n")
    print(list_of_lines)

    f = open("rankinfo", "w")
    f.writelines(list_of_lines)
    f.close()

@bot.command()
async def rank(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
        print(member)

    print(member)
    print(type(member))
    convertedId = str(member.id)

    if convertedId in open("rankinfo").read():
        print("success")
        #print(convertedId + "aaa")
        phrase = convertedId
        line_number = "Phrase not found"
        f = open("rankinfo", "r")

        for number, line in enumerate(f):
            if phrase in line:
                line_number = number
                break
        f.close()

        print(line_number) #"+1, its the user id"
        with open("rankinfo", 'r') as f:
            for line in islice(f, line_number + 1, line_number + 2):
                embed=discord.Embed(title="Current XP: " + line, color=discord.Color.blue())
                await ctx.send(embed=embed)
        f.close()

    else:

        f = open("rankinfo", 'a')
        writeRank(f, convertedId)
        writeRank(f, "0")
        f.close()
        embed = discord.Embed(title="Please wait, setting up your profile...", color=discord.Color.purple())
        await ctx.send(embed=embed)
        time.sleep(3)
        phrase = convertedId
        line_number = "Phrase not found"
        f = open("rankinfo", "r")

        for number, line in enumerate(f):
            if phrase in line:
                line_number = number
                break
        f.close()

        print(line_number)
        #readRank("rankinfo", line_number+1, line_number+2)
        with open("rankinfo", 'r') as f:
            for line in islice(f, line_number+1, line_number+2):
                embed = discord.Embed(title="Current XP: " + line, color=discord.Color.blue())
                await ctx.send(embed=embed)
            f.close()

@bot.command()
@commands.has_role('new role')
async def rank_add(ctx, xp):
    print(ctx.author.id)
    print(type(ctx.author.id))
    print(xp)
    print(type(xp))
    xp2 = int(xp)
    giveXP(ctx.author.id, xp2)
    embed = discord.Embed(title="Total XP updated. Stop cheating tho", color=discord.Color.green())
    await ctx.send(embed=embed)


######################################################################
#                       On Message Stuff                             #
######################################################################

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.author.id)

    msg = message.content.lower()

    await bot.process_commands(message)




    if "-button" in msg:

        await message.channel.send(
            "Button List",
            components=[
                Button(style=ButtonStyle.blue, label="Blue"),
                Button(style=ButtonStyle.red, label="Red"),
                Button(style=ButtonStyle.green, label="Green"),
                Button(style=ButtonStyle.URL, label="Test Link", url="https://example.org"),
                Button(style=ButtonStyle.randomColor(), label="Random", url="https://www.google.com/"),
            ],
        )
        i=0
        while i<100: #adjust this for the amount of regular buttons i have
            res = await bot.wait_for("button_click")

            if res.channel == message.channel:
                print(res.component.label),
                print(type(res.component.label))
                if res.component.label == "Red":
                    await message.channel.send("Red")
                    await res.respond(
                        type=InteractionType.ChannelMessageWithSource,
                        content='aaaaaaaaaaaaaaaaaaa',
                    )
                else:
                    await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f'{res.component.label} clicked',
                    )
            i = i+1

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
            giveXP(message.author.id, 5)
            embed = discord.Embed(title="You received 5 exp for winning!", color=discord.Color.green())
            await message.channel.send(embed=embed)
        elif moves.index(msg) - 1 == num:
            embed = discord.Embed(title="You win! GG")
            await message.channel.send(embed=embed)
            giveXP(message.author.id, 5)
            embed = discord.Embed(title="You received 5 exp for winning!", color=discord.Color.green())
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
    if "gottem" in msg:
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

    if "cailou" in msg:
        embed = discord.Embed(title="OMG CAILLOU MY FAVORITE TV SHOW AHHHHHHH")
        await message.channel.send(embed=embed)

    if "yeet" in msg:
        embed = discord.Embed(title="Yeet indeed", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    if "shut up" in msg:
        embed = discord.Embed(title="Didn't ask ha gg", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    if "didnt ask" in msg or "did i ask" in msg:
        embed = discord.Embed(title="Didn't ask for you not to ask", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    #if "bruh" in msg:
        #embed = discord.Embed(title="Bruh momento")
        #await message.channel.send(embed=embed)
    if "no u" in msg:
        test = '{0.author.mention}'.format(message)
        embed = discord.Embed(title='No u', description=test, color=discord.Color.blue())
        await message.channel.send(embed=embed)



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
    curseWord = ['stupid', 'curse2']
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

@bot.command(name="rps")
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


@bot.command()
async def guess(ctx):
    if ctx.author == bot.user:
        return
    number = randint(1,100)
    guess = 2
    await asyncio.sleep(1)
    await ctx.send('Guess a number between 1 and 100. You have 3 guesses.')
    while guess != -1:
        print(guess)
        def check(author):
            print(number)
            def inner_check(message):
                if message.author != author:
                    return False
                try:
                    int(message.content)
                    return True
                except ValueError:
                    return False
            return inner_check

        msg = await bot.wait_for('message', check=check, timeout=30)
        attempt = int(msg.content)

        if attempt > number:
            if guess == 0:
                print("endlow")
                await ctx.send("L incorrect, the correct number was " + str(number))
                break
            else:
                await ctx.send('Incorrect. You have ' + str(guess) + ' guesses left...')
                #await asyncio.sleep(1)
                await ctx.send('Try going **lower**')
                await asyncio.sleep(1)
                guess -= 1
        elif attempt < number:
            if guess == 0:
                print("endhigh")
                await ctx.send("L incorrect, the correct number was " + str(number))
                break
            else:
                await ctx.send('Incorrect. You have ' + str(guess) + ' guesses left...')
                #await asyncio.sleep(1)
                await ctx.send('Try going **higher**')
                await asyncio.sleep(1)
                guess -=1
        elif attempt == number:
            await ctx.send('You actually guessed it! What a gamer!')
            giveXP(ctx.author.id, 20)
            embed = discord.Embed(title="You received 20 exp for guessing correctly!", color=discord.Color.green())
            await ctx.send(embed=embed)
            print("ezzz")
            break




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

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def tictactoe(ctx, p2: discord.Member): #p1: discord.Member,
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
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

        player1 = ctx.author
        print((player1))
        player2 = p2

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
            turn    = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("You're already in a game lol. If that person is afk good luck")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
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
                print(count)
                print(mark)
                print(type(mark))
                print(player1)
                if gameOver == True and mark == ":regional_indicator_x:":
                    await ctx.send("<@" + str(player1.id) + ">'s wins! What a gamer")
                    channel = await player2.create_dm()
                    print(channel)
                    embed = discord.Embed(title="Lmao you lost L", color=discord.Color.dark_blue())
                    print(player1.id)
                    print(player2.id)
                    await channel.send(embed=embed)
                    giveXP(player1.id, 30)
                    giveXP(player2.id, -15)
                    embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                        player1.id) + "> was given 30 exp for winning." + "\n" + "<@" + str(
                        player2.id) + "> lost 15 exp for losing.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    print("here??? 2.0")
                elif gameOver == True and mark == ":o2:":
                    await ctx.send("<@" + str(player2.id) + "> wins! What a gamer")
                    channel = await player1.create_dm()
                    print(channel)
                    embed = discord.Embed(title="Lmao you lost L", color=discord.Color.dark_blue())
                    await channel.send(embed=embed)
                    print(player1.id)
                    print(player2.id)

                    giveXP(player2.id, 30)
                    giveXP(player1.id, -15)
                    embed = discord.Embed(title="Exp earnings/losses:", description="<@" + str(
                        player2.id) + "> was given 30 exp for winning." + "\n" + "<@" + str(
                        player1.id) + "> lost 15 exp for losing.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    print("here???")

                elif count >= 9:
                    gameOver = True
                    await ctx.send("Bruh you tied")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Put it like this: -place 'number'. Make sure the numbered square isn't filled.")
        else:
            await ctx.send("Bruh stop trying to cheat it aint your turn")
    else:
        await ctx.send("There aint a game going on. Start a new one using the -tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True




######################################################################
#                         Error Compensation                         #
######################################################################

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="You gotta put what you want me to say", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Don't try to kick the owner or me lmao", color=discord.Color.dark_red())
        await ctx.send(embed=embed)

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="You gotta put who you want to send to, and what you want me to say to them", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)

@testdm.error
async def testdm_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Put a message you want to test", color=discord.Color.dark_red())
        await ctx.send(embed=embed)

@random.error
async def random_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Bruh it has to be in the format '-random min, max'", colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)

@wanted.error
async def wanted_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandInvokeError):
        print("It prints image, so idk why it gives error CommandInvokeError")

@rank_add.error
async def rank_add_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(title="Lol tryna cheat but don't know how")
        await ctx.send(embed=embed)

@guess.error
async def guess_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Some random error that I still need to fix but im too lazy to. Just go again")
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
bot.run(awesomeguy_token)
