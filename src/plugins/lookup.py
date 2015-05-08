import urllib
import re
from xml.etree import ElementTree
import plugin
from message import Message

class Lookup(plugin.Plugin):
    def __init__(self, connection):
        plugin.Plugin.__init__(self, connection)
        self.pluginname = 'lookup'

    # http://blog.programmableweb.com/2010/02/08/googles-secret-weather-api/
    def weather(self, nick, channel, params):
        # ditch this for now. The API appears to have gone away
        return
    
        if len(params) < 1:
            return;

        replyto = nick if channel == None else channel
        location = ' '.join(params)
        url = 'http://www.google.com/ig/api?' + urllib.urlencode({'weather' : location})
        xml = ElementTree.parse(urllib.urlopen(url))
        
        condition = xml.find('.//current_conditions/condition').attrib['data']
        temp = (xml.find('.//current_conditions/temp_c').attrib['data'], xml.find('//temp_f').attrib['data'])
        wind = xml.find('.//current_conditions/wind_condition').attrib['data']
        report = '{0} is currently {1} ({2}C {3}F) {4}'.format(location, condition, temp[0], temp[1], wind)
        
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, report]
        self.connection.send(m)
        
    # Many thanks to Adrian O'Neill for his dictionary web service
    # http://services.aonaware.com/DictService/DictService.asmx/DefineInDict
    # dictId=wn&word=XXXXX
    def define(self, nick, channel, params):
        if len(params) < 1:
            return;
            
        replyto = nick if channel == None else channel
        url = 'http://services.aonaware.com/DictService/DictService.asmx/DefineInDict'
        body = urllib.urlencode({'dictId' : 'wn', 'word' : params[0]}) 
        xml = ElementTree.parse(urllib.urlopen(url, body))
       
        namespace = '{http://services.aonaware.com/webservices/}'
        result = xml.findtext('.//{0}Definition/{0}WordDefinition'.format(namespace))
    
        m = Message()
        m.command = 'PRIVMSG'
        
        lines = result.split('\n')
        for i in range(min(len(result), 5)):
            m.params = [replyto, lines[i]]
            self.connection.send(m)

    # http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=Toast        
    def wiki(self, nick, channel, params):
        if len(params) < 1:
            return;

        replyto = nick if channel == None else channel
        qs = { 
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'xml',
            'titles': ' '.join(params)
        }
        url = 'http://en.wikipedia.org/w/api.php?' + urllib.urlencode(qs)

        xml = ElementTree.parse(urllib.urlopen(url))
        result = xml.findtext('.//rev')

        if result is not None:
            result = self.deugly_wikimedia(result)
        else:
            result = 'Couldn\'t find it :('
            
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, result]
        self.connection.send(m)

    # Helper method to remove the WikiMedia markup from a string
    def deugly_wikimedia(self, data):
        stack = []
        offset = 0
        # remove metadata sections
        while '{{' in data:
            start = data.find('{{', offset)
            end = data.find('}}', offset)
            if start == -1 or end < start:
                if len(stack) == 0:
                    break # fuck it
                a = stack.pop()
                d = data[:a] + data[end + 2:]
                data = d
                offset = a + 2
            else:
                stack.append(start)
                offset = start + 2
        
        # remove blank lines
        data = data.replace('\r\n', '')
        data = data.replace('\n', '')
        
        # scrap text formatting
        data = data.replace("''", '')
        data = data.replace("'''", '')
        data = data.replace("''''", '')
        data = data.replace("'''''", '')
        
        # tidy links
        data = re.sub(r'\[\[([^\]\|]+)\|([^\]\|]+)\]\]', r'\2', data)
        data = re.sub(r'\[\[([^\]\|]+)\]\]', r'\1', data)
        
        # split paragraphs
        data = data.splitlines()[0]
        
        return data

