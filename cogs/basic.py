import discord
from discord.ext import commands
import math

# discord.py calls groups of commands cogs
# cogs can also be handlers for different types of events
# and respond to changes in data as they happen

# setup
class BasicCog:
    def __init__(self, bot):
        self.bot = bot

    # ping command
    @commands.command()
    async def ping(self, ctx):
        # replies back to the command context with the
        # text "Pong!"
        await ctx.send("Pong!")

    # Echo command
    @commands.command()
    async def echo(self, ctx, *, message: str='_echo_'):
        await ctx.send(ctx.author.mention + ' : ' + message)

# add this cog to the bot
def setup(bot):
    bot.add_cog(BasicCog(bot))
