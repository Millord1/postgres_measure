from database import DataBase
from psycopg2.extras import execute_batch
import io
import pandas as pd
from sqlalchemy import create_engine

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
        
    def push_copy_version(self, data: list[tuple]):
        f = io.StringIO()
        
        for row in data:
            line = '\t'.join(str(val) for val in row)
            f.write(line + '\n')
        
        f.seek(0)
        
        q = f"""
            COPY {self.db.test_table} (number, texte, date, decimal) 
            FROM STDIN 
            WITH DELIMITER E'\t';
        """
        self.db.cursor.copy_expert(q, f)
        self.db.conn.commit()
        
        
    def push_pandas_native_version(self, data: list[tuple], use_multi: bool = False, chunksize: int = None):
        conn_str = f"postgresql+psycopg2://{self.db.user}:{self.db.pw}@localhost:5432/{self.db.db_name}"
        engine = create_engine(conn_str)
        
        df = pd.DataFrame(data, columns=['number', 'texte', 'date', 'decimal'])
        
        method_strategy = 'multi' if use_multi else None
        
        df.to_sql(
            name=self.db.test_table, 
            con=engine, 
            if_exists='append', 
            index=False, 
            chunksize=chunksize, 
            method=method_strategy
        )