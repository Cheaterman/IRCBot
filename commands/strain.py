from ircbot import bot
from .leaflib import search


@bot.command('!strain (.*)')
def strain(self, channel, user, name):
    say = lambda msg: self.say(channel, msg, user)
    descriptions = [
        strain.description
        for strain in search(name)
        if strain.description
    ]

    if not descriptions:
        say(f'Sorry, strain "{name}" not found :-S')
        return

    say(descriptions[0])
