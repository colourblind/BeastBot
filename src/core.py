from datetime import datetime, timedelta
from message import Message
import db
import plugin

class Core(plugin.Plugin):
    def __init__(self, connection):
        plugin.Plugin.__init__(self, connection)
        self.startdate = datetime.now()
        self.pluginname = ''
        db.setup_db()
        db.reset_all_logins()
    
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
        if len(details) < 1:
            return self.error_message(nick, channel, 'Usage: !join CHANNEL')
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
        if not self.check_permissions(nick, channel, 'a'):
            return self.error_message(nick, channel, 'Admin rights required')
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [nick, 'Aaaieeee!']
        self.connection.send(m)
        m.command = 'QUIT'
        m.params = ['We out']
        self.connection.send(m)
        
    def register(self, nick, channel, details):
        if len(details) < 2:
            return self.error_message(nick, channel, 'Usage: !register USERNAME PASSWORD')
        if channel != None:
            return self.error_message(nick, channel, 'USE PRIVATE MESSAGES FOR REGISTERING AND LOGGING IN (idiot)')
        
        m = Message()
        m.command = 'PRIVMSG'
        u = db.User(details[0])
        if u.new:
            u.username = details[0]
            u.setpassword(details[1])
            u.save()
            m.params = [nick, 'Done']
        else:
            m.params = [nick, 'User already exists']
        self.connection.send(m)
        
    def login(self, nick, channel, details):
        if len(details) < 2:
            return self.error_message(nick, channel, 'Usage: !login USERNAME PASSWORD')
        if channel != None:
            return self.error_message(nick, channel, 'USE PRIVATE MESSAGES FOR REGISTERING AND LOGGING IN (idiot)')
        u = db.User(nick=nick)
        if not u.new:
            return self.error_message(nick, channel, 'You are already logged in as ' + u.nick)            

        m = Message()
        m.command = 'PRIVMSG'
        u = db.authenticate(details[0], details[1])
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
        u = db.User(nick=nick)
        m = Message()
        m.command = 'PRIVMSG'
        if u.new:
            m.params = [nick, 'Unable to match nick to user']
        else:
            u.logout()
            m.params = [nick, 'Done']
        self.connection.send(m)
        
    def perms(self, nick, channel, details):
        if len(details) == 0:
            return self.error_message(nick, channel, 'Usage: !perms USER [CHANNEL] [PERMISSIONS]')
        u = db.User(details[0])
        if u.new:
            return self.error_message(nick, channel, 'Could not find user')

        m = Message()
        m.command = 'PRIVMSG'
        if len(details) == 1:
            m.params = [nick, str(u.getallpermissions())]
        elif len(details) == 2:
            m.params = [nick, str(u.getpermissions(details[1]))]
        elif len(details) == 3:
            channel = details[1] if details[1].startswith('#') else '#' + details[1]
            if self.check_permissions(nick, channel, 'o'):
                u.setpermissions(channel, details[2])
                m.params = [nick, 'Done']
            else:
                return self.error_message(nick, channel, 'You do not have the required permissions for this channel')
        self.connection.send(m)
            
    def promote(self, nick, channel, details):
        if channel == None and len(details) == 0:
            return self.error_message(nick, channel, 'Usage: !promote CHANNEL')
        u = db.User(nick=nick)
        m = Message()
        if u.new:
            m.command = 'PRIVMSG'
            m.params = [nick, 'Please log in']
            self.connection.send(m)
        else:
            if channel == None:
                channel = details[0] if details[0].startswith('#') else '#' + details[0]
            perms = u.getpermissions(channel)
            if perms != None:
                m.command = 'MODE'
                m.params = [channel, '+' + perms, nick]
                self.connection.send(m)
            else:
                m.command = 'PRIVMSG'
                m.params = [nick, 'You have no rights for this channel']
                self.connection.send(m)
        
    def finduser(self, nick, channel, details):
        if len(details) < 1:
            return;
        users = db.finduser(details[0])
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [nick, '']
        for row in users:
            m.params[1] = str(row)
            self.connection.send(m)
