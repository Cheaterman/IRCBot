from ircbot import bot
from .leaflib import search


@bot.command('!strain (.*)')
def strain(self, channel, user, name):
    say = lambda msg: self.say(channel, msg, user)
    strains_with_descriptions = [
        strain
        for strain in search(name)
        if strain.description
    ]

    if not strains_with_descriptions:
        say(f'Sorry, strain "{name}" not found :-S')
        return

    strain = strains_with_descriptions[0]
    say(f'{strain.name} - {strain.description}')
