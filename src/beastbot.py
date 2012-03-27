import sys
import sqlite3
import connection
from message import Message
import core
import plugin
import user

def create_connection():
    return sqlite3.connect('beastbot.db')
    
def close_connection(connection):
    connection.close()

class BeastBot:
    def __init__(self, server, port=6667, nick='BeastBot', username=None, password=None):
        user.setup_connection_factory(create_connection, close_connection)
        
        self.connection = connection.Connection(server, port)
        self.connection.handshake(nick)
        self.plugins = [core.Core(self.connection)]
        self.plugins.extend(plugin.load_plugins(self.connection))
        
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
        elif message.command == 'QUIT':
            # user left. Log them out if need be
            u = user.User(nick=message.sender)
            u.logout()
        elif message.command == 'NICK':
            # nick updated. Chase them!
            u = user.User(nick=message.sender)
            u.change_nick(message.params[0])
        elif message.command == 'PRIVMSG' and message.params[1].startswith('!'):
            # palm it off to the plugins
            for plugin in self.plugins:
                if plugin.handle(message):
                    break
            

if __name__ == '__main__':
    beastbot = BeastBot(sys.argv[1])
    beastbot.run()
