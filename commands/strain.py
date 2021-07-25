from ircbot import bot
from .leaflib import search


@bot.command('!strain (.*)')
def strain(self, channel, user, name):
    data = search(name)
    say = lambda msg: self.say(channel, msg, user)

    if not data:
        say(f'Sorry, strain "{name}" not found :-S')

    say(data[0].description)
