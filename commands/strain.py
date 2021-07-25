from ircbot import bot
from .leaflib import search


@bot.command('!strain (.*)')
def strain(self, channel, user, name):
    data = search(name)
    say = lambda msg: self.say(channel, msg, user)
    descriptions = [strain.description for strain in data]

    if not any(descriptions):
        say(f'Sorry, strain "{name}" not found :-S')
        return

    say(descriptions[0])
