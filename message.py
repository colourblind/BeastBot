class Message:
    def __init__(self, raw=''):
        self.raw = raw
        self.prefix = ''
        self.command = ''
        self.params = []
        
    def parse(self):
        tokens = self.raw.split(' ')
        if tokens[0].startswith(':'):
            self.prefix = tokens.pop(0)
        self.command = tokens.pop(0)
        while len(tokens) > 0:
            if tokens[0].startswith(':'):
                tokens[0] = tokens[0][1:]
                self.params.append(' '.join(tokens))
                break
            else:
                self.params.append(tokens.pop(0))
        print('prefix-' + self.prefix)
        print('comman-' + self.command)
        print('params-' + str(self.params))
        
    def serialise(self):
        p = ' '.join(map(lambda x: ':' + x if ' ' in x else x, self.params))
        if len(self.prefix) > 0:
            return ' '.join([self.prefix, self.command, p]) + '\r\n'
        else:
            return ' '.join([self.command, p]) + '\r\n'
