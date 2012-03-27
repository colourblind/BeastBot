import unittest
import mock_db
from message import Message

class TestMessageParsing(unittest.TestCase):
        
    def test_basic(self):
        m = Message('PRIVMSG #foo :this is a test message')
        m.parse()
        self.assertEqual(m.command, 'PRIVMSG')
        self.assertEqual(m.params[0], '#foo')
        self.assertEqual(m.params[1], 'this is a test message')
        
    def test_escape_colon(self):
        m = Message('PRIVMSG #foo :test: completed')
        m.parse()
        self.assertEqual(m.command, 'PRIVMSG')
        self.assertEqual(m.params[0], '#foo')
        self.assertEqual(m.params[1], 'test: completed')
    
if __name__ == '__main__':
    unittest.main()
