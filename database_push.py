from database import DataBase

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
               
    # def push_unique_transac(self, data: list[tuple]):
        