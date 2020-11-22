    #imports
#i use this because i use juypter
import nest_asyncio
nest_asyncio.apply()
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
            sporkClient = SporkInstance('chromedriver.exe', False, i)
            succeeded = sporkClient.enter_credentials();
            if (succeeded):
                response += sporkClient.click_join_button()
            else:
                response += 'failed'
            sporkClient.driver.quit()
            response += '\n'
            return response
  
