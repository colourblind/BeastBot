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

    def test_get_new_user(self):
        user = db.User('foo')
        self.assertEqual(user.username, 'foo')
        self.assertTrue(user.new)
        
    def test_get_existing_user(self):
        user = db.User('admin')
        self.assertEqual(user.username, 'admin')
        self.assertFalse(user.new)
        
    def test_get_user_by_nick(self):
        user = db.User('admin')
        user.nick = 'test_nick'
        user2 = db.User(nick='test_nick')
        self.assertEqual(user.username, 'admin')
        
    def test_check_password(self):
        user = db.User('admin')
        self.assertTrue(user.checkpassword('password'))
        
    def test_set_password(self):
        user = db.User('foo')
        user.setpassword('toast')
        self.assertTrue(user.checkpassword('toast'))
        
    def test_change_nick(self):
        user = db.User('admin')
        user.change_nick('test_nick')
        self.assertEqual(user.nick, 'test_nick')
        user.change_nick('')
        
    def test_logout(self):
        user = db.User('admin')
        user.change_nick('test_nick')
        self.assertEqual(user.nick, 'test_nick')
        user.logout()
        self.assertEqual(user.nick, '')
        
    def test_set_perms(self):
        user = db.User('admin')
        user.setpermissions('#foo', 'o')
        perm = user.getpermissions('#foo')
        self.assertEqual(perm, 'o')
        
    def test_remove_perms(self):
        user = db.User('admin')
        user.setpermissions('#foo', 'o')
        perm = user.getpermissions('#foo')
        self.assertEqual(perm, 'o')
        user.setpermissions('#foo', '0')
        perm2 = user.getpermissions('#foo')
        self.assertIsNone(perm2)
		
if __name__ == '__main__':
    unittest.main()
