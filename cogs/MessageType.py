from discord.ext import commands
import discord
import time


class MessageType(commands.Cog):
    def __init__(self, bot):
        self.bot = bot #adwadas

    @commands.command()
    async def embed(ctx, title="a ", description="a ", footer=None):
        embed = discord.Embed(title=title, description=description, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def edit(ctx):
        message = await ctx.author.send("hello")
        time.sleep(2)
        await message.edit(content="new content")
        await ctx.author.send("aaaa")

    @commands.command()
    async def testembed(ctx):
        file = discord.File("wanted2.jpg")
        e = discord.Embed(color=discord.Color.blue())
        e.set_image(url="attachment://wanted2.jpg")
        await ctx.send(file=file, embed=e)

    @commands.command()
    async def audio(ctx):
        await ctx.send(file=discord.File("ExampleAudioFile.mp3"))




def setup(bot):
    bot.add_cog(MessageType(bot))