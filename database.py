import psycopg2

class DataBase:
    
    test_table = "test"
    time_table = "time"
    push_type_table = "push_type"
    
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
        
    def reset_table(self):
        self.cursor.execute(f"TRUNCATE TABLE {self.test_table};")
        self.conn.commit()
    
    
    def save_times_to_db(self, method_name: str, times: list[float]):
        try:
            q_push_type = f"""
                INSERT INTO {self.push_type_table} (name) 
                VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING push_id;
            """
            self.cursor.execute(q_push_type, (method_name,))
            push_id = self.cursor.fetchone()[0]
            
            time_data = [(push_id, t) for t in times]
            
            q_times = f"""
                INSERT INTO {self.time_table} (push_id, time)s
                VALUES (%s, %s);
            """
            self.cursor.executemany(q_times, time_data)
            
            self.conn.commit()
            print(f"Sauvegarde réussie en DB pour : {method_name}")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur lors de la sauvegarde en DB : {e}")
    

class DataBaseCreator:
    def __init__(self, db: DataBase):
        self.db = db
        
    def create_all_tables(self):
        self.__create_test_table()
        self.__create_time_tables()
        self.db.conn.commit()
        
        
    def __create_test_table(self):
        q = f"""
        CREATE TABLE IF NOT EXISTS {self.db.test_table} (
            number INTEGER,
            texte TEXT,
            date TIMESTAMP,
            decimal FLOAT
        );
        """
        
        self.db.cursor.execute(q)
    
    def __create_time_tables(self):
        q_names = f"""
        CREATE TABLE IF NOT EXISTS {self.db.push_type_table} (
            push_id SERIAL PRIMARY KEY,
            name VARCHAR(60) UNIQUE
        )
        """
        
        q_times = f"""
        CREATE TABLE IF NOT EXISTS {self.db.time_table} (
            time_id SERIAL PRIMARY KEY,
            push_id INTEGER REFERENCES {self.db.push_type_table} (push_id) ON DELETE CASCADE,
            time NUMERIC(20,16)
        )
        """
        
        self.db.cursor.execute(q_names)
        self.db.cursor.execute(q_times)