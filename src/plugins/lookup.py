import urllib
from xml.etree.ElementTree import ElementTree
import plugin
from message import Message

class Lookup(plugin.Plugin):
    def __init__(self, connection):
        plugin.Plugin.__init__(self, connection)
        self.pluginname = 'lookup'

    # http://blog.programmableweb.com/2010/02/08/googles-secret-weather-api/
    def weather(self, replyto, params):
        location = ' '.join(params)
        url = 'http://www.google.com/ig/api?' + urllib.urlencode({'weather' : location})
        xml = ElementTree(file=urllib.urlopen(url))
        
        condition = xml.find('//current_conditions/condition').attrib['data']
        temp = (xml.find('//current_conditions/temp_c').attrib['data'], xml.find('//temp_f').attrib['data'])
        wind = xml.find('//current_conditions/wind_condition').attrib['data']
        report = '{0} is currently {1} ({2}C {3}F) {4}'.format(location, condition, temp[0], temp[1], wind)
        
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, report]
        self.connection.send(m)
        
    # Many thanks to Adrian O'Neill for his dictionary web service
    # http://services.aonaware.com/DictService/DictService.asmx/DefineInDict
    # dictId=wn&word=XXXXX
    def define(self, replyto, params):
        url = 'http://services.aonaware.com/DictService/DictService.asmx/DefineInDict'
        body = urllib.urlencode({'dictId' : 'wn', 'word' : params[0]}) 
        xml = ElementTree(file=urllib.urlopen(url, body))
        
        namespace = '{http://services.aonaware.com/webservices/}'
        result = xml.findtext('//{0}Definition/{0}WordDefinition'.format(namespace))
    
        m = Message()
        m.command = 'PRIVMSG'
        
        lines = result.split('\n')
        for i in range(min(len(result), 5)):
            m.params = [replyto, lines[i]]
            self.connection.send(m)

    # http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=Toast        
    def wiki(self, replyto, params):
        url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=' + urllib.encode(params[0])
        xml = ElementTree(file=urllib.open(url))
    
        result = xml.findtext('rev')
        result = self.__deugly_wikimedia(result)
    
        m = Message()
        m.command = 'PRIVMSG'
        m.params = [replyto, result]
        self.connection.send(m)

    # Helper method to remove the WikiMedia markup from a string
    def __deugly_wikimedia(data):
        
        return data
