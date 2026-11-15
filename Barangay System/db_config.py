import pymysql


class MySQLConnector:
    """Small replacement for flaskext.mysql. Keeps the same mysql.connect() call
    used in class, but only needs PyMySQL (no extra package that can break)."""

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'db_barangay_system'

    def connect(self):
        return pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset='utf8mb4')


mysql = MySQLConnector()
