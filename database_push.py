from database import DataBase
from psycopg2.extras import execute_batch

class DatabasePusher:
    def __init__(self, db: DataBase):
        self.db = db
        
    def push_naive_version(self, data: list[tuple]):
        for item in data: 
            self.db.cursor.execute(f"""
                INSERT INTO {self.db.test_table} 
                (number, texte, date, decimal) 
                VALUES (%s,%s,%s,%s)
            """,item)
            self.db.conn.commit()
               
    def push_unique_transac(self, data: list[tuple]):
        for item in data: 
            self.db.cursor.execute(f"""
                INSERT INTO {self.db.test_table} 
                (number, texte, date, decimal) 
                VALUES (%s,%s,%s,%s)
            """,item)
        self.db.conn.commit()
        
    def push_executemany_version(self, data: list[tuple]):
        q = f"""
            INSERT INTO {self.db.test_table} (number, texte, date, decimal) 
            VALUES (%s, %s, %s, %s)
        """
        self.db.cursor.executemany(q, data)
        self.db.conn.commit()
        
    def push_execute_batch_version(self, data: list[tuple], page_size: int = 1000):
        q = f"""
            INSERT INTO {self.db.test_table} (number, texte, date, decimal) 
            VALUES (%s, %s, %s, %s)
        """
        execute_batch(self.db.cursor, q, data, page_size=page_size)
        self.db.conn.commit()