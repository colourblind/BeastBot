import unittest
import db
import mock_db

class TestDb(unittest.TestCase):
    
    def setUp(self):
        mock_db.setup()
    
    def test_login(self):
        user = db.authenticate('admin', 'password')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
        
    def test_login_fail_password(self):
        user = db.authenticate('admin', 'foo')
        self.assertIsNone(user)
        
    def test_login_fail_username(self):
        user = db.authenticate('foo', 'password')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
