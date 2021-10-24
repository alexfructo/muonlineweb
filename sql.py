import pyodbc as db
import abc
from config import SQL_DRIVER, SQL_HOST, SQL_PORT, SQL_USER, SQL_PASS, SQL_BASE


class MSSQL:

    @staticmethod
    def conn():
        try:
            connection = db.connect(r'DRIVER=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s;' % (SQL_DRIVER, SQL_HOST, SQL_PORT, SQL_BASE, SQL_USER, SQL_PASS), autocommit=True)
            #connection.setdecoding(db.SQL_CHAR, encoding='utf-8')
            #connection.setdecoding(db.SQL_WCHAR, encoding='utf-8')
            #connection.setdecoding(db.SQL_WMETADATA, encoding='utf-8')
            #connection.setencoding(encoding='utf-8')
            return connection.cursor()
        except Exception as e:
            return f'Não possível concluir a operação. \n Error: {str(e)}'
