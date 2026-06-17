from database import DataBase, DataBaseCreator
from perf_counter import Counter
from database_push import DatabasePusher
from seeder import Seeder
from pathlib import Path

PW = "Millord!"
USER = "postgres"
DB_NAME = "test"

def main():
    
    db = DataBase(DB_NAME, USER, PW)
    db_creator = DataBaseCreator(db)
    db_creator.create_test_table()
    
    db_pusher= DatabasePusher(db)
    seeder = Seeder()
    thousand_data = seeder.create_thousand()
    
    times = []
    
    for _ in range(0,9):
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    
    filepath = Path("data/thousand_naive.txt")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(map(str, times)), encoding="utf-8")
        
    print(times)
    
    
main()