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
db_creator.create_test_table()

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
    for _ in range(0,9):
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    write_file("data/thousand_naive.txt", times)
    
def push_thousand_naive_transaction():
    times = []
    for _ in range(0,9):
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    write_file("data/thousand_unique_tx.txt", times)

def write_file(name: str, content):
    filepath = Path(name)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(map(str, content)), encoding="utf-8")
    
main()