from dotenv import load_dotenv
from database import DataBase, DataBaseCreator
from perf_counter import Counter
from database_push import DatabasePusher
from seeder import Seeder
import os
import time

load_dotenv()

PW = os.getenv('PW')
USER = os.getenv('USER')
DB_NAME = os.getenv('DB_NAME')

def main():
    
    db = DataBase(DB_NAME, USER, PW)
    db_creator = DataBaseCreator(db)
    db_creator.create_test_table()
    
    db_pusher= DatabasePusher(db)
    seeder = Seeder()
    thousand_data = seeder.create_thousand()
    
    with Counter() as count:
        db_pusher.push_naive_version(thousand_data)   
        
    print(count.elapsed)
    
    
main()