import pyodbc
from contextlib import contextmanager

@contextmanager
def conectar_banco():
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"  
        "Database=DB_Loja;"  
        "Trusted_Connection=yes;" 
    )
    conn = pyodbc.connect(connection_string)
    try:
        yield conn
    finally:
        conn.close()
