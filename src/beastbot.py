import sys
import sqlite3
import connection
from message import Message
import core
import plugin
import db
import json

def create_connection():
    return sqlite3.connect('beastbot.db')
    
def close_connection(connection):
    connection.close()

class BeastBot:
    def __init__(self, settings):
        db.setup_connection_factory(create_connection, close_connection)
        
        self.settings = settings
        
        self.connection = connection.Connection(self.settings['host'], self.settings['port'])
        self.connection.handshake(self.settings['nick'])
        self.plugins = [core.Core(self.connection, self.settings)]
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
            u = db.User(nick=message.sender)
            u.logout()
        elif message.command == 'NICK':
            # nick updated. Chase them!
            u = db.User(nick=message.sender)
            u.change_nick(message.params[0])
        elif message.command == 'PRIVMSG' and message.params[1].startswith(self.settings['command_prefix']):
            # palm it off to the plugins
            for plugin in self.plugins:
                if plugin.handle(message):
                    break
             
        channel = None
        if message.params[0].startswith('#'):
            channel = message.params[0]
        db.log_message(message.command, message.sender, channel, ' '.join(message.params))

if __name__ == '__main__':
    settings_file = open(sys.argv[1], 'r')
    settings = json.load(settings_file)
    settings_file.close()
    beastbot = BeastBot(settings)
    beastbot.run()
