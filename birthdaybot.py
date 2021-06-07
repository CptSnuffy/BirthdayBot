import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
import re
from dotenv import load_dotenv
load_dotenv()

def initializeBirthdays():
    for line in birthdayFile:
        key, value = line.strip('\n').split(" ",1)
        birthdays[key] = value
def idToName(name,birthdate):
    idtoNamesFile = open("d:\Python Projects\BirthdayBot\BirthdayBot\idstonames.txt", "a")
    idtoNamesFile.write(name+' '+birthdate+'\n')
birthdays = {}
birthdayFile = open("d:\Python Projects\BirthdayBot\BirthdayBot\\birthdays.txt")
initializeBirthdays()

token = os.getenv('token')
print(birthdays)

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Birthday bot is ready')

@tasks.loop(hours=24)
async def called_once_a_day():

@bot.command()
async def addbirthday(message,*,nameandbirth : str):
    print(nameandbirth)
    birthdayFile = open("d:\Python Projects\BirthdayBot\BirthdayBot\\birthdays.txt","a")
    birthdayFile.write('\n'+nameandbirth)
    initializeBirthdays()
    birthdate = nameandbirth.split(" ",1)
    idToName(message.author.name,birthdate[1])
    await message.channel.send("Birthday added!")
    print(birthdays)

@bot.command()
async def birthdays(ctx):
    birthdayFile = open("d:\Python Projects\BirthdayBot\BirthdayBot\idstonames.txt", "r")
    birthdaysList = birthdayFile.read()
    print(birthdaysList)

    await ctx.send('```'+birthdaysList+'```')
bot.run(token)
    