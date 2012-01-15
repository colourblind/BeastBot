import sqlite3
import os

class User:
    def __init__(self, username=None, nick=None, data=None):
        if username == None and nick == None and data == None:
            self.new = True
            self.username = ''
            self.nick = ''
            self.admin = False
            self.last_login = None
            self.__password = ''
        else:
            if not username == None:
                conn = sqlite3.connect('beastbot.db')
                c = conn.cursor()
                c.execute('select username, password, nick, admin, last_login from user where username = ?', (username,))
                data = c.fetchone()
                conn.close()
            elif not nick == None:
                conn = sqlite3.connect('beastbot.db')
                c = conn.cursor()
                c.execute('select username, password, nick, admin, last_login from user where nick = ?', (nick,))
                data = c.fetchone()
                conn.close()
                
            if data == None:
                self.new = True
                self.username = username
                self.nick = ''
                self.admin = False
                self.last_login = None
                self.__password = ''
            else:
                self.new = False
                self.username = data[0]
                self.__password = data[1]
                self.nick = data[2]
                self.admin = data[3]
                self.last_login = data[4]
                
    def __str__(self):
        s = '{0} {1}'.format(self.username, self.nick)
        return s
       
    def save(self):
        conn = sqlite3.connect('beastbot.db')
        c = conn.cursor()
        if self.new:
            data = (self.username, self.__password, self.nick, self.admin, self.last_login)
            c.execute('insert into user (username, password, nick, admin, last_login) values (?, ?, ?, ?, ?)', data)
            self.new = False
        else:
            data = (self.__password, self.nick, self.admin, self.last_login, self.username)
            c.execute('update user set password = ?, nick = ?, admin = ?, last_login = ? where username = ?', data)
        conn.commit()
        conn.close()

    def getpermissions(self, channel):
        conn = sqlite3.connect('beastbot.db')
        c = conn.cursor()
        c.execute('select level from permission where username = ? and channel = ?', (self.username, channel))
        data = c.fetchone()[0]
        conn.close()
        return data
        
    def setpermissions(self, channel, rights):
        # TODO: update vs. insert
        conn = sqlite3.connect('beastbot.db')
        c = conn.cursor()
        c.execute('insert into permission set rights = ? where username = ? and channel = ?', (rights, self.username, channel))
        conn.commit()
        conn.close()
        
    def checkpassword(self, password):
        return self.__password == hash(password)
        
    def setpassword(self, newpassword):
        self.__password = hash(newpassword)
        
def authenticate(username, password):
    u = User(username)
    if not u == None:
        if not u.checkpassword(password):
            u = None
    return u
    
def hash(password):
    return password
        
def finduser(username):
    conn = sqlite3.connect('beastbot.db')
    c = conn.cursor()
    c.execute("select username, password, nick, admin, last_login from user where username like ?", ('%' + username + '%',))
    data = c.fetchall()
    conn.close()
    return map(lambda x: User(data=x), data)

def reset_all_logins():
    conn = sqlite3.connect('beastbot.db')
    c = conn.cursor()
    c.execute("update user set nick = ''")
    conn.commit()
    conn.close()
    
def setup_db():
    if os.path.exists('beastbot.db') and os.path.isfile('beastbot.db'):
        return
        
    conn = sqlite3.connect('beastbot.db')
    c = conn.cursor()

    c.execute('create table user (username text primary key, password text, nick text, admin integer, last_login text)')
    c.execute('insert into user values (?, ?, ?, ?, ?)', ('admin', 'password', '', True, None))
    
    c.execute('create table permission (username text, channel text, rights text, primary key(username, channel))')
    
    conn.commit()
    conn.close()

def is_new_channel(channel):
    conn = sqlite3.connect('beastbot.db')
    c = conn.cursor()
    c.execute('select * from permission where channle = ?', (channel,))
    data = c.rowcount == 0
    conn.close()
    return data
