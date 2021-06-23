import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


def idToName(name,birthdate):
    idtoNamesFile = open("/home/ec2-user/BirthdayBot/idstonames.txt", "a")
    idtoNamesFile.write(name+' '+birthdate+'\n')
    idtoNamesFile.close()

def checkBirthdays():
    global birthdayUser
    global date
    birthdays = {}
    birthdates = []
    print(datetime.today())
    today = str(datetime.today().strftime('%m %d')).split(' ')
    print(today)
    f = open("/home/ec2-user/BirthdayBot/irthdays.txt",'r')
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

@tasks.loop(hours=24)
async def called_once_a_day():
    global birthdayUser
    global date
    message_channel_id = 800119655892779018
    print("day check")
    checkBirthdays()
    print(date)
    print("loopy")
    message_channel = bot.get_channel(message_channel_id)
    print(message_channel)
    if(checkBirthdays()):
        print("Birthday time for real")
        await message_channel.send("@\everyone wish a very happy birthday to "+birthdayUser+"! Have an absolutely fantastic day 🎂🥳")
@bot.command()
async def addbirthday(message,*,nameandbirth : str):
    print(nameandbirth)
    birthdayFile = open("/home/ec2-user/BirthdayBot/birthdays.txt","a")
    birthdayFile.write(nameandbirth+'\n')
    birthdate = nameandbirth.split(" ",1)
    idToName(message.author.name,birthdate[1])
    birthdayFile.close()
    await message.channel.send("Birthday added!")
    print(birthdays)

@bot.command()
async def birthdays(ctx):
    birthdayFile = open("/home/ec2-user/BirthdayBot\idstonames.txt", "r")
    birthdaysList = birthdayFile.read()
    birthdayFile.close()
    print(birthdaysList)

    await ctx.send('```'+birthdaysList+'```')
@bot.command()
async def initializeBot(ctx):

    await ctx.send('Birthday loop started!')
bot.run(token)

    