import os

from ircbot import bot
from commands import seen, time

from random import randint

@bot.command('!help')
def help(self, channel, user):
    msg = 'Command list: '
    commands = [
        '!help',
        '!botsnack',
        '!fortune',
        '!seen',
        '!time',
        '!toke',
        'doobie doobie doo',
        '!drug',
    ]
    for i, command in enumerate(commands):
        msg += command + (', ' if i < len(commands) - 1 else '')
    self.say(channel, msg, user)

@bot.command('!botsnack')
@bot.command('(?i)(.+botsnack)')
def botsnack(self, channel, user, msg=None):
    if(msg and not msg.startswith(self.nickname)):
        return True
    msg = "Thanks! Nomnomnom :3"
    self.say(channel, msg, user)

@bot.command('!fortune')
def fortune(self, channel, user):
    fortune = os.popen('/usr/games/fortune').read()
    msg = "Fortune: \n{}".format(fortune)
    self.msg(channel, msg)
    for line in msg.split('\n'):
        if line:
            self.logger.log("<%s> %s" % (self.nickname, line))

@bot.command('!toke(?:\s+(\w+))?')
def toke(self, channel, user, to=None):
    msg = "Puff! Puff! Pass{}! ^__^".format(' to {}'.format(to) if to else '')
    self.say(channel, msg, user)

@bot.command('!drug(?:\s+(\w+))?')
def toke(self, channel, user, to=None):
    drugs = ["Cocain","LSD","DMT","Mescaline","Shrooms","MDMA","Extacy","Salvia","Opium"]
    drug = drugs[randint(0,len(drugs)-1)]
    msg = "Here is some {}! take it! *bliblibli*".format(drug)
    if to:
        user = to
    self.say(channel, msg, user)

@bot.command('.*(?i)doobie doobie doo')
def doobie_doobie_do(self, channel, user):
    url = 'https://youtu.be/j4XhDpSgHrs'
    msg = "{} owiiiiii! ^__^".format(url)
    self.say(channel, msg, user)

@bot.command('!join ([^ ]+)')
def join(self, channel, user, target):
    if user == 'Cheaterman':
        self.join(target)

@bot.command('!part ([^ ]+)')
def part(self, channel, user, target):
    if user == 'Cheaterman':
        self.leave(target)
