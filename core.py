from datetime import datetime, timedelta
from message import Message
import plugin

class Core(plugin.Plugin):
    def __init__(self, connection):
        plugin.Plugin.__init__(self, connection)
        self.startdate = datetime.now()
        self.pluginname = ''
    
    def uptime(self, replyto, details):
        td = datetime.now() - self.startdate
        total_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'Up since ' + str(self.startdate)]
        self.connection.send(m)
        m.params = [replyto, 'That\'s ' + str(total_seconds) + ' seconds']
        self.connection.send(m)
    
    def uthere(self, replyto, details):
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'Yarr']
        self.connection.send(m)
        
    def join(self, replyto, details):
        m = Message()
        m.command = 'JOIN'
        if details[0].startswith('#'):
            m.params = [details[0]]
        else:
            m.params = ['#' + details[0]]
        self.connection.send(m)
        
    def die(self, replyto, details):
        m = Message()
        m.command = 'QUIT'
        m.params = ['We out']
        self.connection.send(m)
