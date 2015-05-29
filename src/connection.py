import socket
import message
import sys
import time

# TODO
# handle server passwords
# SSL connections

class Connection:
    def __init__(self, address, port=6667):
        self.s = socket.socket()
        self.buffer = ''
        print('Connecting to ' + address)
        self.s.settimeout(60)
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
        m.params = [nick if username is None else username, '8', '*', '.']
        self.send(m)
        # TODO: pass?
    
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
        data = data[:508] # technically 512, but if I cut it fine some servers just ignore it
        try:
            print(data)
            self.s.sendall(data)
        except UnicodeEncodeError:
            print('UnicodeEncodeError - you should probably fix that')
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
        data = None
        while data is None:
            try:
                data = self.s.recv(4096)
                self.buffer = self.buffer + data
            except socket.timeout:
                # Just keep waiting. Only using a timeout
                # so we can handle interrupts
                pass
