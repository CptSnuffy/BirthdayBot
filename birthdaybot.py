import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from datetime import datetime
import os
import html
from dotenv import load_dotenv

load_dotenv() #Discord bot token needs to be in a .env file
__location__ = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__))) #shorthand for assigning current working directory


#Returns a list made of entries on a text file. If no file exists it creates one
def initializeBirthdays(birthdays):
    birthdayFile = open(os.path.join(__location__,"birthdays.txt"), encoding="utf-8")
    for line in birthdayFile:
        key, value = line.strip('\n').split(" ",1)
        birthdays[key] = value
    birthdayFile.close()
    return birthdays

#Saves user ids to readable usernames to a separate file
def idToName(name,birthdate):
    idtoNamesFile = open(os.path.join(__location__,"idstonames.txt"), "a", encoding="utf-8")
    idtoNamesFile.write(name+' '+birthdate+'\n')
    idtoNamesFile.close()

#Called with loop, iterates through text file and checks current date for birthdays
def checkBirthdays():
    global birthdayUser
    global date
    birthdays = {}
    birthdates = []
    print(datetime.today())
    today = str(datetime.today().strftime('%m %d')).split(' ')
    print(today)
    f = open(os.path.join(__location__,"birthdays.txt"),'r', encoding="utf-8")
    content = f.read().splitlines()
    for date in range(0,len(content),1):
        print('birthday loop')
        birthdates.append(content[date].split(' '))
    for line in range(0,len(birthdates),1):
        print("looping check")
        print(line)
        print(today)
        print(birthdates[line])
        currentBirthday = birthdates[line]
        birthdayUser = currentBirthday[0]
        currentBirthday = [currentBirthday[1],currentBirthday[2]]
        print(currentBirthday)
        if(currentBirthday == today):
            print("it's someone's birthday")
            return True
    f.close()

birthdays = {}
birthdayUser = ''
client = discord.Client
token = os.getenv('token')
print(birthdays)
date = []
bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Birthday bot is ready')
    called_once_a_day.start()


#This loop will start whenever you launch the bot. It will not check birthdays at midnight unless you launched the bot at midnight
@tasks.loop(hours=24)
async def called_once_a_day():
    global birthdayUser
    global date
    message_channel_id = 800119655892779018 #This variable will need to be changed to whatever channel id your birthday channel uses
    checkBirthdays()
    print(date)
    message_channel = bot.get_channel(message_channel_id)
    print(message_channel)
    if(checkBirthdays()):
        await message_channel.send("@everyone wish a very happy birthday to "+birthdayUser+"! Have an absolutely fantastic day 🎂🥳")

#Birthdays added need to be in a specific format: @USERADDINGBIRTHDAY DAY/MONTH | @Snuffy 27/03 | @Makuhita 06/08
@bot.command()
async def addbirthday(message,*,nameandbirth : str):
    print(nameandbirth)
    birthdayFile = open(os.path.join(__location__,"birthdays.txt"),"a", encoding="utf-8")
    birthdayFile.write(nameandbirth+'\n')
    birthdate = nameandbirth.split(" ",1)
    idToName(message.author.name,birthdate[1])
    birthdayFile.close()
    await message.channel.send("Birthday added!")
    print(birthdays)

#Displays all birthdays in assigned discord channel
@bot.command()
async def birthdays(ctx):
    birthdayFile = open(os.path.join(__location__,"idstonames.txt"), "r", encoding="utf-8")
    birthdaysList = birthdayFile.read()
    birthdayFile.close()
    print(birthdaysList)

    await ctx.send('```'+birthdaysList+'```')
@bot.command()
async def initializeBot(ctx):

    await ctx.send('Birthday loop started!')
bot.run(token)

