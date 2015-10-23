#!/usr/bin/python
# coding: utf-8

import os, re, sys, time

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log


class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime('[%H:%M:%S]')
        with open(self.file, 'a') as file:
            file.write('%s %s\n' % (timestamp, message))


class IRCBot(irc.IRCClient):
    nickname = 'Weedykins'
    password = ''

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        self.logger = MessageLogger(self.factory.filename)
        self.logger.log(
            "[Connected to {}]".format(self.factory.hostname)
        )

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log(
            "[Disconnected from {}]".format(self.factory.hostname)
        )

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.logger.log("[Joined {}]".format(self.factory.channel))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        if(
            msg.startswith('!botsnack') or
            (
                msg.startswith(self.nickname) and
                'botsnack' in msg
            )
        ):
            msg = "{}: Thanks! Nomnomnom :3".format(user)
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))

        match = re.match('!seen (\w+)', msg)
        if match:
            nick = match.group(1)
            with open(self.logger.file, 'r') as file:
                for line in reversed(list(file)[:-1]):
                    match = re.match("\[(\d+:\d+:\d+)\] <{}> (.*)".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {} saying « {} »".format(user, nick, match.group(1), match.group(2))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
			break

                    match = re.match("\[(\d+:\d+:\d+)\] \* {} (.*)".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {}, « {} »".format(user, nick, match.group(1), match.group(2))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
			break

                    match = re.match("\[(\d+:\d+:\d+)\] {} is now known as (.*)".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {}, changing name to « {} »".format(user, nick, match.group(1), match.group(2))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
                        break

                    match = re.match("\[(\d+:\d+:\d+)\] {} joined channel".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {}, joining channel".format(user, nick, match.group(1))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
                        break

                    match = re.match("\[(\d+:\d+:\d+)\] {} left channel \((.*)\)".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {}, leaving channel ({})".format(user, nick, match.group(1), match.group(2))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
                        break

                    match = re.match("\[(\d+:\d+:\d+)\] {} quit \((.*)\)".format(nick), line)
                    if match:
                        msg = "{}: {} was last seen at {}, quitting ({})".format(user, nick, match.group(1), match.group(2))
                        self.msg(channel, msg)
                        self.logger.log("<%s> %s" % (self.nickname, msg))
                        break

                if not match:
                    msg = "{}: Sorry, I haven't seen {}! :-$".format(user, nick)
                    self.msg(channel, msg)
                    self.logger.log("<%s> %s" % (self.nickname, msg))

        if msg.startswith('!fortune'):
            fortune = os.popen('/usr/games/fortune').read()
            msg = "Fortune: \n{}".format(fortune)
            self.msg(channel, msg)
            for line in msg.split('\n'):
                if line:
                    self.logger.log("<%s> %s" % (self.nickname, line))

        match = re.match('!join ([^ ]+)', msg)
        if user == 'Cheaterman' and match:
            self.join(match.group(1))

        match = re.match('!part ([^ ]+)', msg)
        if user == 'Cheaterman' and match:
            self.leave(match.group(1))


    def action(self, user, channel, msg):
        user = user.split('!', 1)[0]
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
        reason = params[1]
        self.logger.log("{} left channel ({})".format(nick, reason))

    def irc_QUIT(self, prefix, params):
        nick = prefix.split('!')[0]
        reason = params[1]
        self.logger.log("{} quit ({})".format(nick, reason))


class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot

    def __init__(self, hostname, port, channel, filename):
        self.hostname = hostname
        self.port = port
        self.channel = channel
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        print "Connection lost: {}".format(reason)
        print "Reconnecting..."
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: {}".format(reason)
        reactor.stop()


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = IRCBotFactory(*sys.argv[1:])

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    reactor.connectTCP(hostname, port, factory)

    reactor.run()
