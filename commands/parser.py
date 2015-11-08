import re


class CommandParser(object):
    commands = {}

    def command(self, pattern):
        regexp = re.compile(pattern)
        def command_generator(function):
            self.commands[regexp] = function
            return function
        return command_generator

    def parse(self, bot, channel, user, msg):
        for regexp, callback in self.commands.items():
            match = regexp.match(msg)
            if match:
                if not callback(bot, channel, user, *match.groups()):
                    return True
