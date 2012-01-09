import sys
import connection
from message import Message
import core

class BeastBot:
    def __init__(self, server, port=6667, nick='BeastBot', username=None, password=None):
        self.connection = connection.Connection(server, port)
        self.connection.handshake(nick)
        self.plugins = [core.Core(self.connection)]
        
    def run(self):
        while True:
            message = self.connection.read_line()
            self.handle(message)
        
    def handle(self, message):
        if message.command == 'PING':
            # respond quick before we get booted!
            m = Message()
            m.command = 'PONG'
            m.params = message.params
            self.connection.send(m)
        elif message.command == 'LEAVE':
            # user left. Log them out if need be
            pass
        elif message.command == 'PRIVMSG' and message.params[1].startswith('!'):
            # palm it off to the plugins
            self.plugins[0].handle(message)
            

if __name__ == '__main__':
    beastbot = BeastBot(sys.argv[1])
    beastbot.run()
