import imp
import inspect
import os
import user
from message import Message

class Plugin:
    def __init__(self, connection):
        self.connection = connection
        self.pluginname = ''
    
    def handle(self, message):
        # Tokenise the message
        p = message.params[1].split(' ')
        # Strip the leading !
        p[0] = p[0][1:]
        # Bail if it's not us (although if no plugin name is specified
        # try anyway
        if not p[0] == self.pluginname and not self.pluginname == '':
            return
            
        # Strip the plugin name from the params
        if p[0] == self.pluginname:
            p = p[1:]

        methodname = p[0]
        try:
            method = getattr(self, methodname)
        except (AttributeError):
            return False

        channel = None
        if message.params[0].startswith('#'):
            channel = message.params[0]
        method(message.sender, channel, p[1:])
            
        return True

    def check_permissions(self, nick, channel, required):
        u = user.User(nick=nick)
        if u == None:
            return False
        if u.admin:
            return True
        if required == 'a':
            return u.admin

        perms = u.getpermissions(channel)
        print('Perms for {0} {1} {2} {3}'.format(nick, channel, perms, required))
        if perms == None:
            return False
        elif required == 'o' and (perms == 'o' or perms == 'v'):
            return True
        elif required == 'v' and perms == 'v':
            return True
        return False
        
    def error_message(self, nick, channel, message):
        recipient = channel if channel != None else nick
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [recipient, message]
        self.connection.send(m)
        
def load_plugins(connection):
    modules = load_modules()
    plugins = []
    
    for module in modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                print('Loading plugin {0} . . .'.format(obj))
                c = getattr(module, name)
                instance = c(connection)
                plugins.append(instance)

    return plugins
        
def load_modules():
    plugins = []
    
    fileList = filter(lambda x: x.lower().endswith('.py'), os.listdir('plugins'))
    for file in fileList:
        name, meh = os.path.splitext(os.path.split(file)[-1])
        path = os.path.join('plugins', file)
        print('Checking module {0} from {1} . . . '.format(name, path))
        plugins.append(imp.load_source(name, path))
    
    return plugins
