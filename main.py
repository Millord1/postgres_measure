from database import DataBase, DataBaseCreator
from perf_counter import Counter
from database_push import DatabasePusher
from seeder import Seeder
from pathlib import Path

PW = "Millord!"
USER = "postgres"
DB_NAME = "test"

db = DataBase(DB_NAME, USER, PW)
db_creator = DataBaseCreator(db)
db_creator.create_all_tables()

db_pusher= DatabasePusher(db)
seeder = Seeder()

thousand_data = seeder.create_thousand()
ht_data = seeder.create_hundred_thousand()
million_data = seeder.create_million()

def main():
    push_naives()
    push_batches()
        
    
def push_batches():
    # TODO
    pass
    
    
def push_naives():
    push_thousand_naive()
    push_thousand_naive_transaction()

def push_thousand_naive():
    times = []
    db.reset_table()
    for _ in range(0, 10):
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    db.save_times_to_db('thousand_naive', times)
    
def push_thousand_naive_transaction():
    times = []
    db.reset_table()
    for _ in range(0, 10):
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    db.save_times_to_db('thousand_unique', times)
    
main()