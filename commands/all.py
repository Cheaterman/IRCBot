import os

from ircbot import bot
from commands import seen, time


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

@bot.command('(?i)doobie doobie doo')
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
