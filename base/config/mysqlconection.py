import pymysql.cursors
class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host='localhost', user='root', password='27112007fi', db=db,
            charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=False)
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            if query.lower().startswith('select'):
                return cursor.fetchall()
            self.connection.commit()
            return cursor.lastrowid

def connectToMySQL(db):
    return MySQLConnection(db)