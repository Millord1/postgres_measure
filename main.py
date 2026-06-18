from database import DataBase, DataBaseCreator
from perf_counter import Counter
from database_push import DatabasePusher
from seeder import Seeder

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
    push_thousand_naive()
    push_thousand_naive_transaction()    
    push_execute_many()
    push_execute_batches()


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
    
    
def push_execute_many():
    print("Executemany 1k")
    times_1k = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_executemany_version(thousand_data)
        times_1k.append(count.elapsed)
    db.save_times_to_db("Executemany 1k", times_1k)

    print("Executemany 100k")
    times_100k = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_executemany_version(ht_data)
        times_100k.append(count.elapsed)
    db.save_times_to_db("Executemany 100k", times_100k)

    print("Executemany 1M")
    times_1m = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_executemany_version(million_data)
        times_1m.append(count.elapsed)
    db.save_times_to_db("Executemany 1M", times_1m)
    
    
def push_execute_batches():
    print("Execute_batch 1k page_size=100")
    times_1k = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_batch_version(thousand_data, page_size=100)
        times_1k.append(count.elapsed)
    db.save_times_to_db("Execute_batch 1k (page_size=100)", times_1k)

    print("Execute_batch 100k page_size=1000")
    times_100k_moyen = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_batch_version(ht_data, page_size=1000)
        times_100k_moyen.append(count.elapsed)
    db.save_times_to_db("Execute_batch 100k (page_size=1000)", times_100k_moyen)

    print("Execute_batch 100k page_size=10 000")
    times_100k_gros = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_batch_version(ht_data, page_size=10000)
        times_100k_gros.append(count.elapsed)
    db.save_times_to_db("Execute_batch 100k (page_size=10000)", times_100k_gros)

    print("Execute_batch 1M (page_size=10 000)")
    times_1m = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_batch_version(million_data, page_size=10000)
        times_1m.append(count.elapsed)
    db.save_times_to_db("Execute_batch 1M (page_size=10000)", times_1m)
    
    
def push_execute_values():
    print("Execute_values 1k (page_size=100)")
    times_1k = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_values_version(thousand_data, page_size=100)
        times_1k.append(count.elapsed)
    db.save_times_to_db("Execute_values 1k (page_size=100)", times_1k)

    print("Execute_values 100k (page_size=1000)")
    times_100k_moyen = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_values_version(ht_data, page_size=1000)
        times_100k_moyen.append(count.elapsed)
    db.save_times_to_db("Execute_values 100k (ps: 1000)", times_100k_moyen)

    print("Execute_values 100k (page_size=10000)")
    times_100k_gros = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_values_version(ht_data, page_size=10000)
        times_100k_gros.append(count.elapsed)
    db.save_times_to_db("Execute_values 100k (ps: 10000)", times_100k_gros)

    print("Execute_values 1M (page_size=10000)")
    times_1m = []
    db.reset_table()
    for _ in range(10):
        with Counter() as count:
            db_pusher.push_execute_values_version(million_data, page_size=10000)
        times_1m.append(count.elapsed)
    db.save_times_to_db("Execute_values 1M (page_size=10000)", times_1m)
    
main()