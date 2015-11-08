import sys

from irc import IRCBotFactory


bot = IRCBotFactory(*sys.argv[1:])
from commands import all
