import sqlite3
import db

memory_db = None

def setup():
    global memory_db
    if not memory_db == None:
        return
    memory_db = TestConnection()
    db.setup_connection_factory(memory_db.get_connection, memory_db.done_connection)
    db.setup_db('admin', 'password')

class TestConnection():
    def __init__(self):
        #print('** Opening test database')
        self._connection = sqlite3.connect(':memory:')
        
    def __del__(self):
        #print('** Closing test database')
        self._connection.close()
        
    def get_connection(self):
        return self._connection
        
    def done_connection(self, connection):
        pass

