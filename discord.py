# bot.py
import discord
from discord.ext import commands

TOKEN = 'token'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command(name='add', help='Adds your name for auto login')
async def autoLogin(ctx, username, password):
    addToFile('names.csv', [ctx.message.author, username, password])
    await ctx.send('Success! Your login has been recorded {}'.format(ctx.message.author.mention))
    await message.delete()

@bot.command(name='run', help='auto logins all saved credentials and returns whether a button was pressed')
@commands.has_role('admin')
async def logins(ctx):
    response = runLogins('names.csv')
    await ctx.send(response)

bot.run(TOKEN)
