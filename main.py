from dotenv import load_dotenv
from database import DataBase, DataBaseCreator
from perf_counter import Counter
import os
import time

load_dotenv()

PW = os.getenv('PW')
USER = os.getenv('USER')
DB_NAME = os.getenv('DB_NAME')

def main():
    
    # db = DataBase(DB_NAME, USER, PW)
    # db_creator = DataBaseCreator(db)
    # db_creator.create_test_table()
    
    with Counter() as count:
        time.sleep(1)
        
    print(count.elapsed)
    
    
main()