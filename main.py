    #imports
#i use this because i use juypter
import nest_asyncio
nest_asyncio.apply()
import discord
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions

    #functions
def createFile(filename):
    with open(filename, mode='w', newline="") as times:
        fileWriter = csv.writer(times, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(["discord", "username", "password"])

#data is a list
def addToFile(filename, data):
    with open(filename, 'r') as inf:
        reader = csv.reader(inf.readlines())
    with open(filename, 'w') as outf:
        writer = csv.writer(outf)
        for line in reader:
            if line[0] != str(data[0]):
                writer.writerow(line)
        writer.writerow(data)

def readCSV(filename):
    with open(filename, mode='r') as times:
        csv_data = csv.reader(times)
        return list(csv_data)
    
def checkfront(str1, str2):
    try:
        return str1[:len(str2)] == str2
    except:
        return false

class SporkInstance:
    def __init__(self, driver_path, is_headless, credentials):
        if is_headless:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
        else: 
            option = None
        self.driver = webdriver.Chrome(driver_path, options=option)
        self.driver.get('https://spork.school/schedule')
        self.credentials = credentials;

    def enter_credentials(self):
        try:
            usernameField = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, 'username')))
            usernameField.clear()
            usernameField.send_keys(self.credentials[1])
            
            passwordField = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, 'password')))
            passwordField.clear()
            passwordField.send_keys(self.credentials[2])
            passwordField.send_keys(Keys.ENTER)
            
            #if true
            return True
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            self.driver.quit()

    def click_join_button(self):
        try:
            joinButton = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button.ui.green.compact.button')))
            joinButton.click()
            return('succeeded')
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            self.driver.quit()
            return('failed')

def runLogins(filename):
    response = 'Results: \n'
    for i in readCSV(filename):
        if (i[0] != 'discord'):
            response += f'\t-{i[0]}: '
            sporkClient = SporkInstance('/Users/Royce/Spork automation/chromedriver', False, i)
            succeeded = sporkClient.enter_credentials();
            if (succeeded):
                response += sporkClient.click_join_button()
            else:
                response += 'failed'
            sporkClient.driver.quit()
            response += '\n'
            return response
        
    #discord
 # bot.py

#add a token
load_dotenv()
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
