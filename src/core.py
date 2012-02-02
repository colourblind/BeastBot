from datetime import datetime, timedelta
from message import Message
import user
import plugin

class Core(plugin.Plugin):
    def __init__(self, connection):
        plugin.Plugin.__init__(self, connection)
        self.startdate = datetime.now()
        self.pluginname = ''
        user.setup_db()
        user.reset_all_logins()
    
    def uptime(self, nick, channel, details):
        replyto = nick if channel == None else channel
        td = datetime.now() - self.startdate
        total_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'Up since ' + str(self.startdate)]
        self.connection.send(m)
        m.params = [replyto, 'That\'s ' + str(total_seconds) + ' seconds']
        self.connection.send(m)
    
    def uthere(self, nick, channel, details):
        replyto = nick if channel == None else channel
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'Yarr']
        self.connection.send(m)
        
    def join(self, nick, channel, details):
        m = Message()
        m.command = 'JOIN'
        if details[0].startswith('#'):
            m.params = [details[0]]
        else:
            m.params = ['#' + details[0]]
        self.connection.send(m)
        # TODO: check if channel already in system
        # TODO: setup user as operator if not
        
    def die(self, nick, channel, details):
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [nick, 'Aaaieeee!']
        self.connection.send(m)
        m.command = 'QUIT'
        m.params = ['We out']
        self.connection.send(m)
        
    def register(self, nick, channel, details):
        if channel != None:
            self.__mock(channel)
            return
        
        m = Message()
        m.command = 'PRIVMSG'
        u = user.User(details[0])
        if u.new:
            u.username = details[0]
            u.setpassword(details[1])
            u.save()
            m.params = [nick, 'Done']
        else:
            m.params = [nick, 'User already exists']
        self.connection.send(m)
        
    def login(self, nick, channel, details):
        if channel != None:
            self.__mock(channel)
            return

        m = Message()
        m.command = 'PRIVMSG'
        u = user.authenticate(details[0], details[1])
        if u == None:
            m.params = [nick, 'Login failed']
        else:
            if len(u.nick) > 0:
                m.params = [nick, 'Already logged in']
            else:
                u.nick = nick
                u.last_login = datetime.now()
                u.save()
                m.params = [nick, 'Login succeeded']
        self.connection.send(m)
        
    def logout(self, nick, channel, details):
        u = user.User(nick=nick)
        m = Message()
        m.command = 'PRIVMSG'
        if u.new:
            m.params = [nick, 'Unable to match nick to user']
        else:
            u.logout()
            m.params = [nick, 'Done']
        self.connection.send(m)
        
    def finduser(self, nick, channel, details):
        users = user.finduser(details[0])
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [nick, '']
        for row in users:
            m.params[1] = str(row)
            self.connection.send(m)
            
    def __mock(self, replyto):
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'You are an idiot']
        self.connection.send(m)
