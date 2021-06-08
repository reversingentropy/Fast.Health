from mysql.connector import pooling
from mysql.connector.conversion import MySQLConverter
from config.settings import Settings

class NumpyMySQLConverter(MySQLConverter):
    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)

class DatabasePool:
    #class variable
    connection_pool = pooling.MySQLConnectionPool(
                            pool_name="ws_pool",
                            #    pool_size=5,
                            #    host='localhost',
                            #    database='furniture',
                            #    user='root',
                            #    password='sum381Tk!')
                            pool_size=5,
                            host=Settings.host,
                            database=Settings.database,
                            user=Settings.user,
                            password=Settings.password)


    @classmethod
    def getConnection(cls): 
        dbConn = cls.connection_pool.get_connection()
#        dbConn.set_converter_class(NumpyMySQLConverter)        
        return dbConn
