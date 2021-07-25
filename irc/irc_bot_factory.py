from twisted.internet import protocol

from irc import IRCBot
from commands import CommandParser


class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot

    def __init__(self, hostname, port, channel, path, nickname, password):
        self.hostname = hostname
        self.port = port
        self.channel = channel
        self.path = path
        self.nickname = nickname
        self.password = password
        self.commands = CommandParser()

    def buildProtocol(self, address):
        return self.protocol(self, self.nickname, self.password)

    def clientConnectionLost(self, connector, reason):
        print('Connection lost: {}'.format(reason))
        print('Reconnecting...')
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed: {}'.format(reason))
        reactor.stop()

    def command(self, pattern):
        return self.commands.command(pattern)


