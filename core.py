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
        
    def register(self, replyto, details):
        if replyto.startswith('#'):
            self.__mock(replyto)
            return
        
        m = Message()
        m.command = 'PRIVMSG'
        u = user.User(details[0])
        if u.new:
            u.username = details[0]
            u.setpassword(details[1])
            u.save()
            m.params = [replyto, 'Done']
        else:
            m.params = [replyto, 'User already exists']
        self.connection.send(m)
        
    def login(self, replyto, details):
        if replyto.startswith('#'):
            self.__mock(replyto)
            return

        m = Message()
        m.command = 'PRIVMSG'
        u = user.login(details[0], details[1])
        if u == None:
            m.params = [replyto, 'Login failed']
        else:
            if u.username in user.logged_in_users:
                m.params = [replyto, 'Already logged in']
            else:
                u.nick = replyto
                u.last_login = datetime.now()
                u.save()
                user.logged_in_users.append(u.username)
                m.params = [replyto, 'Login succeeded']
        self.connection.send(m)
        
    def logout(self, replyto, details):
        m = Message()
        m.command = 'PRIVMSG'
        u = user.getuserbynick(replyto)
        if u == None:
            m.params = [replyto, 'Unable to match nick to user']
        else:
            if u.username in user.logged_in_users:
                user.logged_in_users.remove(u.username)
                m.params = [replyto, 'Done']
            else:
                m.params = [replyto, 'You are not logged in']
        self.connection.send(m)
        
    def finduser(self, replyto, details):
        users = user.finduser(details[0])
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, '']
        for row in users:
            m.params[1] = str(row)
            self.connection.send(m)
        
    def __mock(self, replyto):
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, 'You are an idiot']
        self.connection.send(m)
