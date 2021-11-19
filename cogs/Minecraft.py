from ntpath import join
from secrets import randbelow
from discord.ext import commands
from discord.ext.commands import BucketType
import discord
from PIL import Image
from io import BytesIO
from discord.ext.commands.errors import CommandError, CommandInvokeError
import requests
import json
import os
from random import randint
import time
from itertools import islice
import asyncio
import copy

def fixfield(arr):
    x = 0
    new_arr = []

    for i in arr:
        #print(i)
        #print(x)
        if x == 0 or x == 1 or x == 12 or x == 13:
            new_line = [""] * 14
            new_arr.append(new_line)
        else:
            new_line = i[1:11]
            new_line.insert(0, "")
            new_line.insert(1, "")
            new_line.insert(12, "")
            new_line.insert(13, "")
            
            new_arr.append(new_line)
        x = x + 1

    return new_arr


def randomgenfield(field):
    random_gen = []
    line = []
    x = 0

    for i in field:
        #print(i)
        for block in i:
            tree_chance = randint(1, 13)
            if tree_chance == 1:
                line.append(":palm_tree:")
                x = x + 1
            else:
                line.append(":green_square:")
                x = x + 1
            
            if x == 14:
                random_gen.append(line)
                line = []
                x = 0
    
    return random_gen



def boardfield(field, playerx, playery):
    global row1, row2, row3, row4, row5
    start_col = playery - 2
    start_row = playerx - 2
    x = 0
    y = 0

    for i in field:
        #print(i)
        if x == start_row:
            if y == 0:
                row1 = i[start_col] + i[start_col + 1] + i[start_col + 2] + i[start_col + 3] + i[start_col + 4]
                #print(row1)
                y = y + 1
            elif y == 1:
                row2 = i[start_col] + i[start_col + 1] + i[start_col + 2] + i[start_col + 3] + i[start_col + 4]
                #print(row2)
                y = y + 1
            elif y == 2:
                row3 = i[start_col] + i[start_col + 1] + i[start_col + 2] + i[start_col + 3] + i[start_col + 4]
                #print(row3)
                y = y + 1
            elif y == 3:
                row4 = i[start_col] + i[start_col + 1] + i[start_col + 2] + i[start_col + 3] + i[start_col + 4]
                #print(row4)
                y = y + 1
            elif y == 4:
                row5 = i[start_col] + i[start_col + 1] + i[start_col + 2] + i[start_col + 3] + i[start_col + 4]
                #print(row5)
                break

        else:
            x = x + 1

    return row1 + "\n" + row2 + "\n" + row3 + "\n" + row4 + "\n" + row5

def writeFile(file, content):
    file.write(content + "\n")

def readRecord(file, id):
    phrase = str(id)
    line_number = "Phrase not found"
    f = open(file, "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            break
    f.close()

    with open(file, 'r') as f:
        for line in islice(f, line_number + 1, line_number + 2):
            current_record = line
    f.close()
    return current_record

def writeTime(id, time):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("minecraftlb", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("minecraftlb", "r")
    list_of_lines = f.readlines()
    list_of_lines[line_number + 1] = time + "\n"
    print(type(list_of_lines))
    #list_of_lines.append("\n")
    #print(list_of_lines)

    f = open("minecraftlb", "w")
    f.writelines(list_of_lines)
    f.close()

def writeWorld(id, world):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("minecraftworlds", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    f = open("minecraftworlds", "r")
    list_of_lines = f.readlines()
    list_of_lines[line_number + 1] = str(world) + "\n"
    #print(type(list_of_lines))
    #list_of_lines.append("\n")
    #print(list_of_lines)

    f = open("minecraftworlds", "w")
    f.writelines(list_of_lines)
    f.close()


def clearWorld(id):
    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("minecraftworlds", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            #print(type(line_number))
            break
    f.close()
    f = open("minecraftworlds", "r")
    list_of_lines = f.readlines()
    del list_of_lines[line_number]
    del list_of_lines[line_number]
    f.close()
    #print(type(list_of_lines))
    #list_of_lines.append("\n")
    #print(list_of_lines)

    f = open("minecraftworlds", "w")
    f.writelines(list_of_lines)
    f.close()


def readWorld(id): #id

    convertedId = str(id)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("minecraftworlds", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()
    
    f = open("minecraftworlds", "r")
    list_of_lines = f.readlines()
    removed_brackets2 = list_of_lines[line_number + 1][2:]
    #removed_brackets2 = second_line[2:]
    removed_brackets = removed_brackets2[:-3]
    firstWorldList = removed_brackets.split("], [")
    print(len(firstWorldList))
    #"'', '', '', '', '', '', '', '', '', '', '', '', '', ''"
    a = 0
    list_line = []
    twoarray_line = []
    while a < len(firstWorldList):
        for i in firstWorldList[a].split(", "):
            fixed = ''.join(i.split("'", 2))
            list_line.append(fixed)
        twoarray_line.append(list_line)
        list_line = []
        a = a + 1

    return twoarray_line

def readReplay(id, time):
    convertedId = str(id + " " + time)
    phrase = convertedId
    line_number = "Phrase not found"
    f = open("minecraftworlds", "r")

    for number, line in enumerate(f):
        if phrase in line:
            line_number = number
            int(line_number)
            print(type(line_number))
            break
    f.close()


    with open("minecraftworlds", 'r') as f:
        for line in islice(f, line_number + 1, line_number + 2):
            replay_moves = line
    f.close()
    return replay_moves


def rankIds():
        x = 0
        user_ids = []
        num_lines = sum(1 for line in open('minecraftlb'))
        with open("minecraftlb", 'r') as file:
            while x <= num_lines:
                for line in islice(file, x, x + 1):
                    line = int(line.strip('\n'))
                    user_ids.append(line)
                x = x + 2
                file.seek(0, 0)
        # print(file.read())
        file.close()
        return(user_ids)

def rankPoints():
    x = 1
    user_points = []
    num_lines = sum(1 for line in open('minecraftlb'))
    with open("minecraftlb", 'r') as file:
        while x <= num_lines:
            for line in islice(file, x, x + 1):
                line = float(line.strip('\n'))
                user_points.append(line)
            x = x + 2
            file.seek(0, 0)
    # print(file.read())
    file.close()
    return(user_points)


def gameIds():
        x = 0
        user_ids = []
        num_lines = sum(1 for line in open('minecraftworlds'))
        with open("minecraftworlds", 'r') as file:
            while x <= num_lines:
                for line in islice(file, x, x + 1):
                    line = (line.strip('\n'))
                    user_ids.append(line)
                x = x + 2
                file.seek(0, 0)
        # print(file.read())
        file.close()
        return(user_ids)

def gameMaps():
    x = 1
    user_points = []
    num_lines = sum(1 for line in open('minecraftworlds'))
    with open("minecraftworlds", 'r') as file:
        while x <= num_lines:
            for line in islice(file, x, x + 1):
                line = float(line.strip('\n'))
                user_points.append(line)
            x = x + 2
            file.seek(0, 0)
    # print(file.read())
    file.close()
    return(user_points)


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, aliases=['mc'])
    async def minecraft(self, ctx, character=":sunglasses:"):
        player = character
        blocks = ":green_square:"
        

        rows, cols = (14, 14)
        arr = [[blocks]*rows for _ in range(cols)]
        field = fixfield(randomgenfield(arr))
        x, y = (randint(2, 11), randint(2, 11))
        field[x][y] = player

        start_field = copy.deepcopy(field)

        #print(original_field)
        #world_replay = {}       
        #world_replay[ctx.author.id] = start_field
        #print(world_replay)
        list_moves = []
        list_moves.append(start_field)
        #print(list_moves)
        #print("first", world_replay[ctx.author.id])


        #print("second", world_replay[ctx.author.id])
        
        

        #f = open("minecraftworlds", 'a')
        #writeFile(f, str(world_replay[0]))
        #writeFile(f, str(world_replay[1]))
        #f.close()
        
        
        

        # print(big_line)
        printed_field = await ctx.send(boardfield(field, x, y))
        await printed_field.add_reaction('⬆')
        await printed_field.add_reaction('⬇')
        await printed_field.add_reaction('⬅')
        await printed_field.add_reaction('➡')
        #await printed_field.add_reaction('🇮')
        await printed_field.add_reaction('🗺️')
        global mapview
        mapview = False
        await printed_field.add_reaction('⏸')
        x1 = x - 1
        y1 = y - 1
        minable_tree = False
        while True:
            if field[x1][y1] == ":palm_tree:":
                minable_tree = True
                minable_tree_coord = (x1, y1)
                #print(minable_tree)
                #print(minable_tree_coord)
                await printed_field.add_reaction('🪓')
                break
            else:
                y1 = y1 + 1
                if y1 > y + 1:
                    y1 = y - 1
                    x1 = x1 + 1
                    if x1 > x + 1:
                        minable_tree = False
                        #print(minable_tree)
                        break
        
        initial_time = time.perf_counter()
        print(initial_time)
        
    
        
        

        while True:            

            try:
                def check(reaction, user):
                    return reaction.message.id == printed_field.id and user.id == ctx.author.id

                reaction1 = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)

                move = str(reaction1[0])

                #print(world_replay)
                
                print(x, y)

                if move == "⏸":
                    await printed_field.remove_reaction("⏸", self.bot.get_user(ctx.author.id))
                    pause_time = time.perf_counter() - initial_time
                    print(pause_time)
                    await printed_field.edit(content="**PAUSED**\n" + boardfield(field, x, y))
                    embed=discord.Embed(title="Pause Menu", color=discord.Color.purple())
                    embed.add_field(name="Options", value="🔁 Generates new seed\n🚫 Exits game\n▶️ Resumes game", inline=True)
                    printed_pause_menu = await ctx.send(embed=embed)
                    await printed_pause_menu.add_reaction('🔁')
                    await printed_pause_menu.add_reaction('🚫')
                    await printed_pause_menu.add_reaction('▶️')
                    def check(reaction, user):
                        return reaction.message.id == printed_pause_menu.id and user.id == ctx.author.id

                    reaction1 = await self.bot.wait_for('reaction_add', check=check) #timeout=120.0
                    selection = str(reaction1[0])

                    if selection == "🔁":
                        #embed.add_field(name="Generating new seed", value="**Tip:** Use the map to see where you are!", inline=True)
                        #await printed_pause_menu.edit(embed=embed)
                        #time.sleep(3)
                        rows, cols = (14, 14)
                        arr = [[blocks]*rows for _ in range(cols)]
                        field = fixfield(randomgenfield(arr))
                        x, y = (randint(2, 11), randint(2, 11))
                        field[x][y] = player
                        await printed_pause_menu.delete()
                        await printed_field.edit(content=boardfield(field, x, y))
                        initial_time = time.perf_counter()
                        print(initial_time)
                        mapview = False
                        continue
                    elif selection == "🚫":
                        embed=discord.Embed(title="Exiting", description="Use '-minecraft' to play again!", color=discord.Color.dark_magenta())
                        await ctx.send(embed=embed)
                        break
                    elif selection == "▶️":
                        b = 3
                        while b > 0:
                            embed=discord.Embed(title="Pause Menu", color=discord.Color.purple())
                            embed.add_field(name="Options", value="🔁 Generates new seed\n🚫 Exits game\n▶️ Resumes game", inline=True)
                            embed.add_field(name="Resuming", value="Resuming in **" + str(b) + "** seconds", inline=True)
                            await printed_pause_menu.edit(embed=embed)
                            time.sleep(1)
                            b = b - 1
                        await printed_pause_menu.delete()
                        initial_time = time.perf_counter() - pause_time
                        print(initial_time)
                        await printed_field.edit(content=boardfield(field, x, y))


                
                if move == "🗺️":
                    if mapview == False:
                        big_line = ""
                        var = 0
                        for i in field:
                            for j in i:
                                big_line = big_line + str(j)
                                var = var + 1
                                if var == len(i):
                                    big_line = big_line + j + "\n"
                                    var = 0
                        mapview = True
                        #print(big_line)
                        await printed_field.edit(content=big_line)
                        await printed_field.remove_reaction("🗺️", self.bot.get_user(ctx.author.id))
                    else:
                        await printed_field.edit(content=boardfield(field, x, y))
                        await printed_field.remove_reaction("🗺️", self.bot.get_user(ctx.author.id))
                        mapview = False
                if move == "🪓":
                    #print(minable_tree_coord)
                    treex, treey = minable_tree_coord
                    field[treex][treey] = blocks

                    new_field = copy.deepcopy(field)
                    list_moves.append(new_field)

                    await printed_field.edit(content=boardfield(field, x, y))
                    await printed_field.remove_reaction("🪓", self.bot.get_user(ctx.author.id))

                    trees_chopped = True

                    for i in field:
                        for j in i:
                            if j == ":palm_tree:":
                                trees_chopped = False
                    if trees_chopped == True:
                        final_time = str(round(time.perf_counter()-initial_time, 3))
                        if str(ctx.author.id) not in open("minecraftlb").read():
                            f = open("minecraftlb", 'a')
                            writeFile(f, str(ctx.author.id))
                            writeFile(f, "0")
                            f.close()
                        embed=discord.Embed(title="You won with a time of " + final_time + "!", color=discord.Color.blue())
                        if float(final_time) < float(readRecord("minecraftlb", ctx.author.id)):
                            print(float(readRecord("minecraftlb", ctx.author.id)))
                            embed.add_field(name="You also beat your previous record!", value="This time was better than your previous record by " + str(float(readRecord("minecraftlb", ctx.author.id)) - float(final_time)) + " seconds!\nI have saved this game because it is a personal best. You can view it using '-minecraft view'.", inline=True)
                            writeTime(ctx.author.id, final_time)
                            create_replay = True                        
                        elif float(final_time) > float(readRecord("minecraftlb", ctx.author.id)):
                            if float(final_time) <= 30:
                                create_replay = True
                                embed.add_field(name="Sadly this is worse than your record.", value="Your record is " + str(round(float(final_time) - float(readRecord("minecraftlb", ctx.author.id)), 3)) + " seconds faster than this run.\nI have saved this game because it is a time under 30 seconds. You can view it using '-minecraft view'", inline=True)
                            else:
                                create_replay = False
                                embed.add_field(name="Sadly this is worse than your record.", value="Your record is " + str(round(float(final_time) - float(readRecord("minecraftlb", ctx.author.id)), 3)) + " seconds faster than this run.", inline=True)

                        
                        
                        #add last movce
                        new_field = copy.deepcopy(field)
                        list_moves.append(new_field)


                        if create_replay == True:
                            list_moves_file = ""
                            move_count = 0
                            for move in list_moves:
                                if move_count == len(list_moves) - 1:
                                    list_moves_file = list_moves_file + str(move)
                                    break
                                else:
                                    list_moves_file = list_moves_file + str(move) + " & "
                                    move_count = move_count + 1
                            #print(list_moves_file)
                            f = open("minecraftworlds", 'a')
                            writeFile(f, str(ctx.author.id) + " " + final_time)
                            writeFile(f, str(list_moves_file))
                            f.close()
                        
                        list_moves = []
                        

                        embed.add_field(name="Play again?", value="React with with 🔁 to play again, or 🚫 to exit.", inline=True)
                        printed_finish = await ctx.send(embed=embed)
                        await printed_finish.add_reaction("🔁")
                        await printed_finish.add_reaction("🚫")
                        try:
                            def check1(reaction, user):
                                return reaction.message.id == printed_finish.id and user.id == ctx.author.id

                            reaction1 = await self.bot.wait_for('reaction_add', check=check1, timeout=45.0)

                            move = str(reaction1[0])

                            if move == "🔁":
                                await printed_finish.delete()
                                rows, cols = (14, 14)
                                arr = [[blocks]*rows for _ in range(cols)]
                                field = fixfield(randomgenfield(arr))
                                #print(field)
                                x, y = (randint(2, 11), randint(2, 11))
                                field[x][y] = player
                                await printed_field.edit(content=boardfield(field, x, y))
                                initial_time = time.perf_counter()
                                print(initial_time)
                                mapview = False
                                start_field = copy.deepcopy(field)
                                list_moves = []
                                list_moves.append(start_field)
                                continue
                            elif move == "🚫":
                                embed=discord.Embed(title="Exiting", description="Use '-minecraft' to play again!", color=discord.Color.dark_magenta())
                                await ctx.send(embed=embed)
                                break

                        except asyncio.TimeoutError:
                            embed=discord.Embed(title="Timeout Error", description="Use '-minecraft' to play again.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            #full_exit = True
                            break                     
                        
                    #CHECKS AGAIN
                    x1 = x - 1
                    y1 = y - 1
                    minable_tree = False
                    while True:
                        if field[x1][y1] == ":palm_tree:":
                            minable_tree = True
                            minable_tree_coord = (x1, y1)
                            print(minable_tree)
                            #print(minable_tree_coord)
                            await printed_field.add_reaction('🪓')
                            break
                        else:
                            y1 = y1 + 1
                            if y1 > y + 1:
                                y1 = y - 1
                                x1 = x1 + 1
                                if x1 > x + 1:
                                    minable_tree = False
                                    print(minable_tree)
                                    await printed_field.remove_reaction("🪓", self.bot.get_user(self.bot.user.id))
                                    break

                    #GIVE PLAYER WOOD


                if move == "⬆":
                    if mapview == False:
                        #print(field[x-1][y])
                        if field[x-1][y] == ":palm_tree:":
                            field[x][y] = player
                        else:
                            field[x][y] = blocks
                            x = x - 1
                            if x <= 1:
                                x = 2
                            field[x][y] = player
                            new_field = copy.deepcopy(field)
                            list_moves.append(new_field)
                            print(x, y)
                            await printed_field.edit(content=boardfield(field, x, y))
                            x1 = x - 1
                            y1 = y - 1
                            minable_tree = False
                            while True:
                                if field[x1][y1] == ":palm_tree:":
                                    minable_tree = True
                                    minable_tree_coord = (x1, y1)
                                    print(minable_tree)
                                    #print(minable_tree_coord)
                                    await printed_field.add_reaction('🪓')
                                    break
                                else:
                                    y1 = y1 + 1
                                    if y1 > y + 1:
                                        y1 = y - 1
                                        x1 = x1 + 1
                                        if x1 > x + 1:
                                            minable_tree = False
                                            print(minable_tree)
                                            break

                    await printed_field.remove_reaction('⬆', self.bot.get_user(ctx.author.id))
                    

                if move == "⬇":
                    if mapview == False:
                        if field[x+1][y] == ":palm_tree:":
                            field[x][y] = player
                        else:
                            field[x][y] = blocks
                            x = x + 1
                            if x >= 12:
                                x = 11
                            field[x][y] = player
                            print(x, y)
                            new_field = copy.deepcopy(field)
                            list_moves.append(new_field)
                            await printed_field.edit(content=boardfield(field, x, y))
                            x1 = x - 1
                            y1 = y - 1
                            minable_tree = False
                            while True:
                                if field[x1][y1] == ":palm_tree:":
                                    minable_tree = True
                                    minable_tree_coord = (x1, y1)
                                    print(minable_tree)
                                    #print(minable_tree_coord)
                                    await printed_field.add_reaction('🪓')
                                    break
                                else:
                                    y1 = y1 + 1
                                    if y1 > y + 1:
                                        y1 = y - 1
                                        x1 = x1 + 1
                                        if x1 > x + 1:
                                            minable_tree = False
                                            print(minable_tree)
                                            break
                    await printed_field.remove_reaction('⬇', self.bot.get_user(ctx.author.id))

                
                if move == "⬅":
                    if mapview == False:
                        if field[x][y-1] == ":palm_tree:":
                            field[x][y] = player
                        else:
                            field[x][y] = blocks
                            y = y - 1
                            if y <= 1:
                                y = 2
                            field[x][y] = player
                            print(x, y)
                            new_field = copy.deepcopy(field)
                            list_moves.append(new_field)
                            await printed_field.edit(content=boardfield(field, x, y))
                            x1 = x - 1
                            y1 = y - 1
                            minable_tree = False
                            while True:
                                if field[x1][y1] == ":palm_tree:":
                                    minable_tree = True
                                    minable_tree_coord = (x1, y1)
                                    print(minable_tree)
                                    #print(minable_tree_coord)
                                    await printed_field.add_reaction('🪓')
                                    break
                                else:
                                    y1 = y1 + 1
                                    if y1 > y + 1:
                                        y1 = y - 1
                                        x1 = x1 + 1
                                        if x1 > x + 1:
                                            minable_tree = False
                                            print(minable_tree)
                                            break
                    await printed_field.remove_reaction('⬅', self.bot.get_user(ctx.author.id))

                
                if move == "➡":
                    if mapview == False:
                        if field[x][y+1] == ":palm_tree:":
                            field[x][y] = player
                        else:
                            field[x][y] = blocks
                            y = y + 1
                            if y >= 12:
                                y = 11
                            field[x][y] = player
                            print(x, y)
                            new_field = copy.deepcopy(field)
                            list_moves.append(new_field)
                            await printed_field.edit(content=boardfield(field, x, y))
                            x1 = x - 1
                            y1 = y - 1
                            minable_tree = False
                            while True:
                                if field[x1][y1] == ":palm_tree:":
                                    minable_tree = True
                                    minable_tree_coord = (x1, y1)
                                    print(minable_tree)
                                    #print(minable_tree_coord)
                                    await printed_field.add_reaction('🪓')
                                    break
                                else:
                                    y1 = y1 + 1
                                    if y1 > y + 1:
                                        y1 = y - 1
                                        x1 = x1 + 1
                                        if x1 > x + 1:
                                            minable_tree = False
                                            print(minable_tree)
                                            break
                    await printed_field.remove_reaction('➡', self.bot.get_user(ctx.author.id))
             
                
            
            except asyncio.TimeoutError:
                embed=discord.Embed(title="Timeout Error", description="How do you take this long to make a move.", color=discord.Color.red())
                await ctx.send(embed=embed)
                join_game = False
                #full_exit = True
                break
        
        
        

    @minecraft.command()
    async def online(self, ctx, character=":sunglasses:"):

        player = character
        blocks = ":green_square:"


        
        
        #field = fixfield(randomgenfield(arr))
        if os.path.getsize("minecraftworlds") != 0:
            embed=discord.Embed(title="Game Selection", description="There are currently game(s) available. Would you like you join one of them or start your own?\n:one: Start your own game\n:1234: Join an available game", color=discord.Color.blue())
            game_type_selection = await ctx.send(embed=embed)
            await game_type_selection.add_reaction('1️⃣')            
            await game_type_selection.add_reaction('🔢')
            await game_type_selection.add_reaction('🚫')

            try:
                def check1(reaction, user):
                    return reaction.message.id == game_type_selection.id and user.id == ctx.author.id
                reaction1 = await self.bot.wait_for('reaction_add', check=check1, timeout=30.0)
                game_type = str(reaction1[0])
                if game_type == "🔢":
                    a = 0
                    embed=discord.Embed(title="Available Games", color=discord.Color.purple())
                    embed.add_field(name="React with :white_check_mark: to join this user's game:", value="<@" + str(gameIds()[a]) + "> " + str(a), inline=True)
                    printed_games = await ctx.send(embed=embed)
                    await printed_games.add_reaction('🚫')
                    while a < len(gameIds()):
                        if a == 0 and a == len(gameIds()) - 1:
                            try:
                                await printed_games.remove_reaction("➡", self.bot.get_user(self.bot.user.id))
                                await printed_games.remove_reaction("⬅", self.bot.get_user(self.bot.user.id))
                            except:
                                pass
                            await printed_games.add_reaction('✅')
                        elif a == 0:
                            try:
                                await printed_games.remove_reaction("⬅", self.bot.get_user(self.bot.user.id))
                            except:
                                pass
                            await printed_games.add_reaction('✅')
                            await printed_games.add_reaction('➡')
                        elif a == len(gameIds()) - 1:
                            try:
                                await printed_games.remove_reaction("➡", self.bot.get_user(self.bot.user.id))
                            except:
                                pass
                            await printed_games.add_reaction('⬅')
                            await printed_games.add_reaction('✅')
                        else:
                            await printed_games.add_reaction('⬅')
                            await printed_games.add_reaction('✅')
                            await printed_games.add_reaction('➡')
                        
                        try:
                            def check1(reaction, user):
                                return reaction.message.id == printed_games.id and user.id == ctx.author.id
                            reaction1 = await self.bot.wait_for('reaction_add', check=check1, timeout=30.0)
                            game = str(reaction1[0])
                            if game == "🚫":
                                embed=discord.Embed(title="Exiting", description="**Tip:** You can use '-minecraft' to play solo.", color=discord.Color.dark_magenta())
                                await ctx.send(embed=embed)
                                join_game = False
                                break
                            if game == "✅":
                                #global person_id
                                person_id = gameIds()[a]
                                print(gameIds(), "DAB")
                                field = readWorld(person_id)
                                join_game = True
                                break
                            elif game == "➡":
                                a = a + 1
                                await printed_games.remove_reaction("➡", self.bot.get_user(ctx.author.id))
                            elif game == "⬅":
                                a = a - 1
                                await printed_games.remove_reaction("⬅", self.bot.get_user(ctx.author.id))
                            embed=discord.Embed(title="Available Games", color=discord.Color.purple())
                            embed.add_field(name="React with :white_check_mark: to join this user's game:" , value="<@" + str(gameIds()[a]) + "> " + str(a), inline=True)
                            await printed_games.edit(embed=embed)
                        except asyncio.TimeoutError:
                            embed=discord.Embed(title="Timeout Error", description="Use '-minecraft online' to view the games again.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            join_game = False
                            break
                elif game_type == "1️⃣":
                    embed=discord.Embed(title="Starting Game Server", description="**Tip:** others can join your game using the '-minecraft online' menu!", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    print("creating world")
                    person_id = ctx.author.id
                    join_game = True
                    rows, cols = (14, 14)
                    arr = [[blocks]*rows for _ in range(cols)]
                    field = fixfield(randomgenfield(arr))
                    f = open("minecraftworlds", 'a')
                    writeFile(f, str(ctx.author.id))
                    writeFile(f, str(field))
                    f.close()
                    await asyncio.sleep(3)
                elif game_type == "🚫":
                    embed=discord.Embed(title="Exiting", description="**Tip:** You can use '-minecraft' to play regular solo.", color=discord.Color.dark_magenta())
                    await ctx.send(embed=embed)
                    join_game = False
                    



            except asyncio.TimeoutError:
                embed=discord.Embed(title="Timeout Error", description="Use '-minecraft online' to view the games again.", color=discord.Color.red())
                await ctx.send(embed=embed)
                join_game = False

            
        else:
            embed=discord.Embed(title="No available games", description="There are currently no available games. Would you like to start one?\n:white_check_mark: Yes\n:no_entry_sign: No", color=discord.Color.blue())
            printed_start_game = await ctx.send(embed=embed)
            await printed_start_game.add_reaction('✅')
            await printed_start_game.add_reaction('🚫')
            
            try:
                def check1(reaction, user):
                    return reaction.message.id == printed_start_game.id and user.id == ctx.author.id
                reaction1 = await self.bot.wait_for('reaction_add', check=check1, timeout=30.0)
                decision = str(reaction1[0])
                if decision == "✅":
                    print("creating world")
                    person_id = ctx.author.id
                    join_game = True
                    rows, cols = (14, 14)
                    arr = [[blocks]*rows for _ in range(cols)]
                    field = fixfield(randomgenfield(arr))
                    f = open("minecraftworlds", 'a')
                    writeFile(f, str(ctx.author.id))
                    writeFile(f, str(field))
                    f.close()
                elif decision == "🚫":
                    embed=discord.Embed(title="Exiting", description="**Tip:** You can use '-minecraft' to play solo.", color=discord.Color.dark_magenta())
                    await ctx.send(embed=embed)
                    join_game = False
            except asyncio.TimeoutError:
                    embed=discord.Embed(title="Timeout Error", description="Use '-minecraft online' to try again.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    join_game = False
        if join_game == True:
            x, y = (randint(2, 11), randint(2, 11))
            field[x][y] = player

            writeWorld(person_id, field)

            # print(big_line)
            printed_field = await ctx.send(boardfield(field, x, y))
            await printed_field.add_reaction('⬆')
            await printed_field.add_reaction('⬇')
            await printed_field.add_reaction('⬅')
            await printed_field.add_reaction('➡')
            #await printed_field.add_reaction('🇮')
            await printed_field.add_reaction('🗺️')
            global mapview
            mapview = False
            await printed_field.add_reaction('🚫')
            x1 = x - 1
            y1 = y - 1
            minable_tree = False
            while True:
                if field[x1][y1] == ":palm_tree:":
                    minable_tree = True
                    minable_tree_coord = (x1, y1)
                    #print(minable_tree)
                    #print(minable_tree_coord)
                    await printed_field.add_reaction('🪓')
                    break
                else:
                    y1 = y1 + 1
                    if y1 > y + 1:
                        y1 = y - 1
                        x1 = x1 + 1
                        if x1 > x + 1:
                            minable_tree = False
                            #print(minable_tree)
                            break
            
            initial_time = time.perf_counter()
            print(initial_time)
            

            

            while True:
                '''
                if mapview is not True:    
                    if field is not readWorld(person_id):
                        field = readWorld(person_id)
                        await printed_field.edit(content=boardfield(field, x, y))
                '''

                

                
                
                try:

                    def check(reaction, user):
                        return reaction.message.id == printed_field.id and user.id == ctx.author.id

                    reaction1 = await self.bot.wait_for('reaction_add', check=check, timeout=75.0)

                    move = str(reaction1[0])
                    
                    field = readWorld(person_id)
                    await printed_field.edit(content=boardfield(field, x, y))
                    
                    print(x, y)

                    if move == "🚫":                
                        if ctx.author.id == person_id:
                            clearWorld(person_id)
                            await ctx.send("killing world")
                        else:
                            field[x][y] = ":green_square:"
                            print(field[x][y])
                            await ctx.send("you left the world")
                        break
                            
                    
                    
                    if move == "🗺️":
                        if mapview == False:
                            big_line = ""
                            var = 0
                            for i in field:
                                for j in i:
                                    big_line = big_line + str(j)
                                    var = var + 1
                                    if var == len(i):
                                        big_line = big_line + j + "\n"
                                        var = 0
                            mapview = True
                            #print(big_line)
                            await printed_field.edit(content=big_line)
                            await printed_field.remove_reaction("🗺️", self.bot.get_user(ctx.author.id))
                        else:
                            await printed_field.edit(content=boardfield(field, x, y))
                            await printed_field.remove_reaction("🗺️", self.bot.get_user(ctx.author.id))
                            mapview = False
                    elif move == "🪓":
                        #print(minable_tree_coord)
                        treex, treey = minable_tree_coord
                        field[treex][treey] = blocks           
                            
                        await printed_field.edit(content=boardfield(field, x, y))
                        await printed_field.remove_reaction("🪓", self.bot.get_user(ctx.author.id))
                        


                        #CHECKS AGAIN
                        x1 = x - 1
                        y1 = y - 1
                        minable_tree = False
                        while True:
                            if field[x1][y1] == ":palm_tree:":
                                minable_tree = True
                                minable_tree_coord = (x1, y1)
                                print(minable_tree)
                                #print(minable_tree_coord)
                                await printed_field.add_reaction('🪓')
                                break
                            else:
                                y1 = y1 + 1
                                if y1 > y + 1:
                                    y1 = y - 1
                                    x1 = x1 + 1
                                    if x1 > x + 1:
                                        minable_tree = False
                                        print(minable_tree)
                                        await printed_field.remove_reaction("🪓", self.bot.get_user(self.bot.user.id))
                                        break

                        #GIVE PLAYER WOOD


                    elif move == "⬆":
                        if mapview == False:
                            #print(field[x-1][y])
                            if field[x-1][y] == ":palm_tree:":
                                field[x][y] = player
                            else:
                                field[x][y] = blocks
                                x = x - 1
                                if x <= 1:
                                    x = 2
                                field[x][y] = player
                                print(x, y)
                                await printed_field.edit(content=boardfield(field, x, y))
                                x1 = x - 1
                                y1 = y - 1
                                minable_tree = False
                                while True:
                                    if field[x1][y1] == ":palm_tree:":
                                        minable_tree = True
                                        minable_tree_coord = (x1, y1)
                                        print(minable_tree)
                                        #print(minable_tree_coord)
                                        await printed_field.add_reaction('🪓')
                                        break
                                    else:
                                        y1 = y1 + 1
                                        if y1 > y + 1:
                                            y1 = y - 1
                                            x1 = x1 + 1
                                            if x1 > x + 1:
                                                minable_tree = False
                                                print(minable_tree)
                                                break

                        await printed_field.remove_reaction('⬆', self.bot.get_user(ctx.author.id))

                    elif move == "⬇":
                        if mapview == False:
                            if field[x+1][y] == ":palm_tree:":
                                field[x][y] = player
                            else:
                                field[x][y] = blocks
                                x = x + 1
                                if x >= 12:
                                    x = 11
                                field[x][y] = player
                                print(x, y)
                                await printed_field.edit(content=boardfield(field, x, y))
                                x1 = x - 1
                                y1 = y - 1
                                minable_tree = False
                                while True:
                                    if field[x1][y1] == ":palm_tree:":
                                        minable_tree = True
                                        minable_tree_coord = (x1, y1)
                                        print(minable_tree)
                                        #print(minable_tree_coord)
                                        await printed_field.add_reaction('🪓')
                                        break
                                    else:
                                        y1 = y1 + 1
                                        if y1 > y + 1:
                                            y1 = y - 1
                                            x1 = x1 + 1
                                            if x1 > x + 1:
                                                minable_tree = False
                                                print(minable_tree)
                                                break
                        await printed_field.remove_reaction('⬇', self.bot.get_user(ctx.author.id))
                    elif move == "⬅":
                        if mapview == False:
                            if field[x][y-1] == ":palm_tree:":
                                field[x][y] = player
                            else:
                                field[x][y] = blocks
                                y = y - 1
                                if y <= 1:
                                    y = 2
                                field[x][y] = player
                                print(x, y)
                                await printed_field.edit(content=boardfield(field, x, y))
                                x1 = x - 1
                                y1 = y - 1
                                minable_tree = False
                                while True:
                                    if field[x1][y1] == ":palm_tree:":
                                        minable_tree = True
                                        minable_tree_coord = (x1, y1)
                                        print(minable_tree)
                                        #print(minable_tree_coord)
                                        await printed_field.add_reaction('🪓')
                                        break
                                    else:
                                        y1 = y1 + 1
                                        if y1 > y + 1:
                                            y1 = y - 1
                                            x1 = x1 + 1
                                            if x1 > x + 1:
                                                minable_tree = False
                                                print(minable_tree)
                                                break
                        await printed_field.remove_reaction('⬅', self.bot.get_user(ctx.author.id))
                    elif move == "➡":
                        if mapview == False:
                            if field[x][y+1] == ":palm_tree:":
                                field[x][y] = player
                            else:
                                field[x][y] = blocks
                                y = y + 1
                                if y >= 12:
                                    y = 11
                                field[x][y] = player
                                print(x, y)
                                await printed_field.edit(content=boardfield(field, x, y))
                                x1 = x - 1
                                y1 = y - 1
                                minable_tree = False
                                while True:
                                    if field[x1][y1] == ":palm_tree:":
                                        minable_tree = True
                                        minable_tree_coord = (x1, y1)
                                        print(minable_tree)
                                        #print(minable_tree_coord)
                                        await printed_field.add_reaction('🪓')
                                        break
                                    else:
                                        y1 = y1 + 1
                                        if y1 > y + 1:
                                            y1 = y - 1
                                            x1 = x1 + 1
                                            if x1 > x + 1:
                                                minable_tree = False
                                                print(minable_tree)
                                                break
                        await printed_field.remove_reaction('➡', self.bot.get_user(ctx.author.id))
                    writeWorld(person_id, field)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title="Timeout Error", description="How do you take this long to make a move", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    join_game = False
                    break

        


    @minecraft.command()
    async def update(self, ctx, time):
        if ctx.author.id == 743819073917550682:
            writeTime(ctx.author.id, time)
            embed = discord.Embed(title="Record Updated.", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You are missing a vital step in achieving this power", color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @minecraft.command()
    async def replays(self, ctx, person: discord.Member = None):
        if person == None:
            a = 0
            member_replays = gameIds()
            replay_option = gameIds()[a].split(" ")
            person_display_name = "All "
        else:
            member_replays = []
            for replay_info in gameIds():
                if int(replay_info.split(" ")[0]) == person.id:
                    member_replays.append(replay_info)  
            a = 0
            replay_option = member_replays[a].split(" ")
            person_display_name = str(person.display_name) + "'s "
            print(member_replays, "dab")
        
           
        
        #os.get size stuff
        
        
        


        embed=discord.Embed(title=person_display_name + "Replays", color=discord.Color.purple())
        embed.add_field(name="React with :white_check_mark: to view this game:", value="<@" + str(replay_option[0]) + ">'s " + str(replay_option[1]) + " second game", inline=True)
        replay_selection = await ctx.send(embed=embed)        
        await replay_selection.add_reaction('🚫')
        while a < len(member_replays):
            if a == 0 and a == len(member_replays) - 1:
                try:
                    await replay_selection.remove_reaction("➡", self.bot.get_user(self.bot.user.id))
                    await replay_selection.remove_reaction("⬅", self.bot.get_user(self.bot.user.id))
                except:
                    pass
                await replay_selection.add_reaction('✅')
            elif a == 0:
                try:
                    await replay_selection.remove_reaction("⬅", self.bot.get_user(self.bot.user.id))
                except:
                    pass
                await replay_selection.add_reaction('✅')
                await replay_selection.add_reaction('➡')
            elif a == len(member_replays) - 1:
                try:
                    await replay_selection.remove_reaction("➡", self.bot.get_user(self.bot.user.id))
                except:
                    pass
                await replay_selection.add_reaction('⬅')
                await replay_selection.add_reaction('✅')
            else:
                await replay_selection.add_reaction('⬅')
                await replay_selection.add_reaction('✅')
                await replay_selection.add_reaction('➡')
            
            try:
                def check1(reaction, user):
                    return reaction.message.id == replay_selection.id and user.id == ctx.author.id
                reaction1 = await self.bot.wait_for('reaction_add', check=check1, timeout=30.0)
                game = str(reaction1[0])
                if game == "🚫":
                    embed=discord.Embed(title="Exiting", description="**Tip:** You can use '-minecraft' to play solo.", color=discord.Color.dark_magenta())
                    await ctx.send(embed=embed)
                    view_game = False
                    break
                if game == "✅":
                    #global person_id
                    person_id = replay_option[0]
                    person_time = replay_option[1]
                    print(member_replays, "DAB")
                    view_game = True
                    break
                elif game == "➡":
                    a = a + 1
                    await replay_selection.remove_reaction("➡", self.bot.get_user(ctx.author.id))
                elif game == "⬅":
                    a = a - 1
                    await replay_selection.remove_reaction("⬅", self.bot.get_user(ctx.author.id))
                replay_option = member_replays[a].split(" ")
                embed=discord.Embed(title=person_display_name + "Replays", color=discord.Color.purple())
                embed.add_field(name="React with :white_check_mark: to view this game:" , value="<@" + str(replay_option[0]) + ">'s " + str(replay_option[1]) + " second game", inline=True)
                await replay_selection.edit(embed=embed)
            except asyncio.TimeoutError:
                embed=discord.Embed(title="Timeout Error", description="Use '-minecraft view' to view the replays again.", color=discord.Color.red())
                await ctx.send(embed=embed)
                view_game = False
                break
  
        if view_game == True:

            replay_message = await ctx.send("Loading Replay...")
            await asyncio.sleep(1)

            removenewline = readReplay(person_id, person_time).replace("\n", "")
            list_world = removenewline.split(" & ")
            
            move_count = 0
            while move_count < len(list_world):
                removed_brackets2 = list_world[move_count][2:]
                #removed_brackets2 = second_line[2:]
                removed_brackets = removed_brackets2[:-3]
                firstWorldList = removed_brackets.split("], [")
                #print(len(firstWorldList))
                #"'', '', '', '', '', '', '', '', '', '', '', '', '', ''"
                a = 0
                list_line = []
                twoarray_line = []
                while a < len(firstWorldList):
                    for i in firstWorldList[a].split(", "):
                        fixed = ''.join(i.split("'", 2))
                        list_line.append(fixed)
                    twoarray_line.append(list_line)
                    list_line = []
                    a = a + 1

                #print(twoarray_line)
                #print(type(twoarray_line))
                
                big_line = ""
                var = 0
                for i in twoarray_line:
                    for j in i:
                        big_line = big_line + str(j)
                        var = var + 1
                        if var == len(i):
                            big_line = big_line + j + "\n"
                            var = 0
                await replay_message.edit(content=big_line)
                move_count = move_count + 1
                await asyncio.sleep(1)
            
            embed=discord.Embed(title="Replay Finished!", color=discord.Color.green())
            await ctx.send(embed=embed)
        
        


    @minecraft.command()
    async def record(self, ctx):
        convertedId = str(ctx.author.id)
        if convertedId in open("minecraftlb").read():
            print("success")
            #print(convertedId + "aaa")
            phrase = convertedId
            line_number = "Phrase not found"
            f = open("minecraftlb", "r")

            for number, line in enumerate(f):
                if phrase in line:
                    line_number = number
                    break
            f.close()

            print(line_number) #0, 1, its the user id"
            with open("minecraftlb", 'r') as f:
                for line in islice(f, line_number + 1, line_number + 2):
                    embed=discord.Embed(title="Current Record: " + line, color=discord.Color.blue())
                    await ctx.send(embed=embed)
            f.close()
        
        else:
            embed=discord.Embed(title="Use '-minecraft' to play and set a record!", color=discord.Color.purple())
            await ctx.send(embed=embed)


    @minecraft.command()
    async def lb(self, ctx):
        print(rankIds())
        print(rankPoints())
        points_descending = rankPoints()
        points_descending.sort(reverse=False)
        print(points_descending)

        lb_dict = {rankPoints()[i]: rankIds()[i] for i in range(len(rankIds()))}
        #<@" + str(number) + ">
        print(lb_dict)
        print(points_descending[2])
        print(lb_dict[points_descending[2]])
        embed=discord.Embed(title="Leaderboard", description="<@" + str(lb_dict[points_descending[0]]) + ">: " + str(points_descending[0]) + "\n<@" + str(lb_dict[points_descending[1]]) + ">: " + str(points_descending[1]) + "\n<@" + str(lb_dict[points_descending[2]]) + ">: " + str(points_descending[2]), color=discord.Color.blue())
        await ctx.send(embed=embed)

    
    

    


def setup(bot):
    bot.add_cog(Minecraft(bot))
