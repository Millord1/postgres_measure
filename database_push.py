from database import DataBase
from seeder import seed

class DatabasePusher:
    def __init__(self, db: DataBase):
        self.db = db
        
    def push_thousand(self):
        data = seed(1000)
        