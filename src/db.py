import os

get_connection = None
done_connection = None

def setup_connection_factory(g, d):
    global get_connection, done_connection
    get_connection = g
    done_connection = d

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
                conn = get_connection()
                c = conn.cursor()
                c.execute('select username, password, nick, admin, last_login from user where username = ?', (username,))
                data = c.fetchone()
                done_connection(conn)
            elif not nick == None:
                conn = get_connection()
                c = conn.cursor()
                c.execute('select username, password, nick, admin, last_login from user where nick = ?', (nick,))
                data = c.fetchone()
                done_connection(conn)
                
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
        conn = get_connection()
        c = conn.cursor()
        if self.new:
            data = (self.username, self.__password, self.nick, self.admin, self.last_login)
            c.execute('insert into user (username, password, nick, admin, last_login) values (?, ?, ?, ?, ?)', data)
            self.new = False
        else:
            data = (self.__password, self.nick, self.admin, self.last_login, self.username)
            c.execute('update user set password = ?, nick = ?, admin = ?, last_login = ? where username = ?', data)
        conn.commit()
        done_connection(conn)

    def getallpermissions(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute('select rights, channel from permission where username = ?', (self.username,))
        data = c.fetchall()
        done_connection(conn)
        return data
        
    def getpermissions(self, channel):
        conn = get_connection()
        c = conn.cursor()
        c.execute('select rights from permission where username = ? and channel = ?', (self.username, channel))
        data = c.fetchone()
        result = None
        if data != None:
            result = data[0]
        done_connection(conn)
        return result
        
    def setpermissions(self, channel, rights):
        conn = get_connection()
        c = conn.cursor()
        if rights == '0':
            c.execute('delete from permission where username = ? and channel = ?', (self.username, channel))
        else:
            c.execute('select * from permission where username = ? and channel = ?', (self.username, channel))
            d = c.fetchall()
            #print(len(d))
            if len(d) == 0:
                c.execute('insert into permission (rights, username, channel) values (?, ?, ?)', (rights, self.username, channel))
            else:
                c.execute('update permission set rights = ? where username = ? and channel = ?', (rights, self.username, channel))
        conn.commit()
        done_connection(conn)
        
    def checkpassword(self, password):
        return self.__password == hash(password)
        
    def setpassword(self, newpassword):
        self.__password = hash(newpassword)
        
    def change_nick(self, newnick):
        self.nick = newnick
        self.save()
        
    def logout(self):
        self.nick = ''
        self.save()
        
def authenticate(username, password):
    u = User(username)
    if not u == None:
        if not u.checkpassword(password):
            u = None
    return u
    
def hash(password):
    return password
        
def finduser(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("select username, password, nick, admin, last_login from user where username like ?", ('%' + username + '%',))
    data = c.fetchall()
    done_connection(conn)
    return map(lambda x: User(data=x), data)

def reset_all_logins():
    conn = get_connection()
    c = conn.cursor()
    c.execute("update user set nick = ''")
    conn.commit()
    done_connection(conn)
    
def setup_db(admin_username, admin_password):
    if os.path.exists('beastbot.db') and os.path.isfile('beastbot.db'):
        return
        
    conn = get_connection()
    c = conn.cursor()

    c.execute('create table user (username text primary key, password text, nick text, admin integer, last_login text)')
    c.execute('insert into user values (?, ?, ?, ?, ?)', (admin_username, admin_password, '', True, None))
    
    c.execute('create table permission (username text, channel text, rights text, primary key(username, channel))')
    
    conn.commit()
    done_connection(conn)

def is_new_channel(channel):
    conn = get_connection()
    c = conn.cursor()
    c.execute('select * from permission where channle = ?', (channel,))
    data = c.rowcount == 0
    done_connection(conn)
    return data
