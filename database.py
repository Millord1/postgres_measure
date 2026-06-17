import psycopg2

class DataBase:
    
    test_table = "test"
    
    def __init__(self, db_name: str, user: str, pw: str):
        self.db_name = db_name
        self.user = user
        self.pw = pw
        self.__check_database()
        
    def __check_database(self):
        self.__connect_without_db()
        self.cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}';")
        exists = self.cursor.fetchone()

        if not exists:
            self.cursor.execute(f"CREATE DATABASE {self.db_name};")
            
        self.cursor.close()
        self.conn.close()
        self.__connect()
        
    def __connect_without_db(self):
        self.conn = psycopg2.connect(
            user=self.user, 
            password=self.pw, 
            host="localhost", 
            port="5432"
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        
    def __connect(self):
        self.conn = psycopg2.connect(
            dbname=self.db_name, 
            user=self.user, 
            password=self.pw, 
            host="localhost", 
            port="5432"
        )
        self.cursor = self.conn.cursor()
        
    def __is_empty(self, table: str):
        q = f"SELECT NOT EXISTS (SELECT 1 FROM {table} LIMIT 1);"
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        return result[0] if result else True
    
    

class DataBaseCreator:
    def __init__(self, db: DataBase):
        self.db = db
        
    def create_all(self):
        self.__create_test_table()
        
    def __create_test_table(self):
        q = f"""
        CREATE TABLE IF NOT EXISTS {self.db.test_table} (
            number INTEGER
            texte TEXT,
            date DATETIME,
            decimal FLOAT
        );
        """
        
        self.db.cursor.execute(q)
        self.db.conn.commit()
    