import socket
import message
import sys
import time

class Connection:
    def __init__(self, address, port=6667):
        self.s = socket.socket()
        self.buffer = ''
        print('Connecting to ' + address)
        self.s.connect((address, port))
    
    def __del__(self):
        self.s.close()
        
    def handshake(self, nick, username=None, password=None):
        time.sleep(3)
        m = message.Message()
        m.command = 'NICK'
        m.params = [nick]
        self.send(m)
        m.command = 'USER'
        m.params = ['BeastBot', 'localhost', 'servername', 'BeastBot']
        self.send(m)
    
    def join(self, channel):
        m = message.Message()
        m.command = 'JOIN'
        if channel.startswith('#'):
            m.params.append(channel)
        else:
            m.params.append('#' + channel)
        self.send(m)
        
    def send(self, message):
        data = message.serialise()
        print(data)
        self.s.sendall(data)
        # TODO: unhack
        if message.command == 'QUIT':
            sys.exit(0)

    # Blocks while grabbing data
    def read_line(self):
        # continue to fill the buffer while we wait for an EOL
        while '\r\n' not in self.buffer:
            self.__receive()
        
        # ugh. Should probably retain the tokens, but in theory we're doing 
        # this pretty regularly and shouldn't need to do large splits
        tokens = self.buffer.split('\r\n')
        self.buffer = '\r\n'.join(tokens[1:])
        print(tokens[0])
        m = message.Message(tokens[0])
        m.parse()
        return m
        
    def __receive(self):
        data = self.s.recv(4096)
        self.buffer = self.buffer + data
