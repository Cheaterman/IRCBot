import time

from chatlog import DATE_FORMAT


class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime('[{}]'.format(DATE_FORMAT))
        with open(self.file, 'a') as file:
            file.write('%s %s\n' % (timestamp, message))
