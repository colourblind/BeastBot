class Plugin:
    def __init__(self, connection):
        self.connection = connection
    
    def handle(self, message):
        if not message.params[1] == self.pluginname and not self.pluginname == '':
            return
        p = message.params[1].split(' ')
        methodname = p[0][1:]
        method = getattr(self, methodname)
        if message.params[0].startswith('#'):
            replyto = message.params[0]
        else:
            replyto = message.sender
        method(replyto, p[1:])
