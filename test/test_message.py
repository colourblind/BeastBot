import unittest
from message import Message

class TestMessageParsing(unittest.TestCase):
        
    def test_privmsg(self):
        m = Message('PRIVMSG #foo :this is a test message')
        m.parse()
        self.assertEqual(m.command, 'PRIVMSG')
        self.assertEqual(m.params[0], '#foo')
        self.assertEqual(m.params[1], 'this is a test message')
    
if __name__ == '__main__':
    unittest.main()
