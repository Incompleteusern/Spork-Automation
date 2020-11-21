#discord
import discord
import main

#add a token
TOKEN = "token"
GUILD = "guild"

client = discord.Client()

def checkfront(str1, str2):
    try:
        return str1[:len(str2)] == str2
    except:
        return false

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guilds:')
    for i in client.guilds:
        print(f'- {i}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower()[0] == '!':
        response = None;
        if checkfront(message.content.lower(), "!help"):
            response = '!login or !add [Username] [Password]: adds your name for auto login \n!run: inputs all data saved'
        elif checkfront(message.content.lower(), '!login') or  checkfront(message.content.lower(), '!add'):
            messagelist = message.content.split()
            try:
                addToFile('names.csv', [message.author, messagelist[1], messagelist[2]])
                response = 'Success! Your login has been recorded {}'.format(message.author.mention)
            except(IndexError):
                response = 'Invalid syntax'
        elif checkfront(message.content.lower(), '!run'):   
            if (message.author.guild_permissions.administrator):
                response = runLogins('names.csv')
            else:
                response = 'You do not have the permissions'
        
        if (response != None):
            await message.channel.send(response)
            await message.delete()
        
client.run(TOKEN)
