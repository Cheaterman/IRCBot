import os

from twisted.words.protocols import irc

from chatlog import MessageLogger


class IRCBot(irc.IRCClient):
    nickname = 'Weedykins'

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        self.logger = MessageLogger(os.path.join(self.factory.path, 'irc.log'))
        self.logger.log(
            "[Connected to {}]".format(self.factory.hostname)
        )

        self.commands = self.factory.commands

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log(
            "[Disconnected from {}]".format(self.factory.hostname)
        )

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.logger.log("[Joined {}]".format(self.factory.channel))

    def privmsg(self, prefix, channel, msg):
        user = prefix.split('!')[0]
        self.logger.log("<%s> %s" % (user, msg))

        if self.commands.parse(self, channel, user, msg):
            return

    def say(self, channel, msg, to=None):
        if to:
            msg = "{}: {}".format(to, msg)
        self.msg(channel, msg)
        self.logger.log("<{}> {}".format(self.nickname, msg))

    def action(self, prefix, channel, msg):
        user = prefix.split('!')[0]
        self.logger.log("* {} {}".format(user, msg))

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("{} is now known as {}".format(old_nick, new_nick))

    def irc_JOIN(self, prefix, params):
        nick = prefix.split('!')[0]
        self.logger.log("{} joined channel".format(nick))

    def irc_PART(self, prefix, params):
        nick = prefix.split('!')[0]
        channel = params[0]
        self.logger.log("{} left channel {}".format(nick, channel))

    def irc_QUIT(self, prefix, params):
        nick = prefix.split('!')[0]
        reason = params[0]
        self.logger.log("{} quit ({})".format(nick, reason))
