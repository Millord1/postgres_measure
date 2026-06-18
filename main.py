from database import DataBase, DataBaseCreator
from perf_counter import Counter
from database_push import DatabasePusher
from seeder import Seeder
from memory_tracker import MemoryTracker
from plot_results import GraphGenerator
import random
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": "localhost",
    "port": 5432,
    "dbname": os.getenv("DB_NAME", "test"),
    "user": os.getenv("USER", "postgres"),
    "password": os.getenv("PW"),
}

db = DataBase(db_config)
db_creator = DataBaseCreator(db)
db_creator.create_all_tables()

db_pusher= DatabasePusher(db)
seeder = Seeder()

thousand_data = seeder.create_thousand()
ht_data = seeder.create_hundred_thousand()
million_data = seeder.create_million()

graph_generator = GraphGenerator(db)

def main():
    
    # db.reset_table()
    # push_thousand_naive()
    # push_thousand_naive_transaction()    
    # push_execute_many()
    # push_execute_batches()
    # push_copy_expert()
    # push_pandas_defaut()
    # push_pandas_multi()
    # push_pandas_callable_copy()
    # push_copy_from_tuple()
    # push_copy_stream_benchmark()
    # push_copy_stream_benchmark_no_faker()
    
    graph_generator.generate_filtered_plots()


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
    for _ in range(0, 10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_naive_version(thousand_data)   
        times.append(count.elapsed)
    db.save_times_to_db('thousand_unique', times)
    
    
def push_execute_many():
    print("Executemany 1k")
    times_1k = []
    for _ in range(10):
        db.reset_table() 
        with Counter() as count:
            db_pusher.push_executemany_version(thousand_data)
        times_1k.append(count.elapsed)
    db.save_times_to_db("Executemany 1k", times_1k)

    print("Executemany 100k")
    times_100k = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_executemany_version(ht_data)
        times_100k.append(count.elapsed)
    db.save_times_to_db("Executemany 100k", times_100k)

    print("Executemany 1M")
    times_1m = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_executemany_version(million_data)
        times_1m.append(count.elapsed)
    db.save_times_to_db("Executemany 1M", times_1m)
    
    
def push_execute_batches():
    print("Execute_batch 1k page_size=100")
    times_1k = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_execute_batch_version(thousand_data, page_size=100)
        times_1k.append(count.elapsed)
    db.save_times_to_db("Execute_batch 1k (page_size=100)", times_1k)

    print("Execute_batch 100k page_size=1000")
    times_100k_moyen = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_execute_batch_version(ht_data, page_size=1000)
        times_100k_moyen.append(count.elapsed)
    db.save_times_to_db("Execute_batch 100k (page_size=1000)", times_100k_moyen)

    print("Execute_batch 100k page_size=10 000")
    times_100k_gros = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_execute_batch_version(ht_data, page_size=10000)
        times_100k_gros.append(count.elapsed)
    db.save_times_to_db("Execute_batch 100k (page_size=10000)", times_100k_gros)

    print("Execute_batch 1M (page_size=10 000)")
    times_1m = []
    for _ in range(10):
        db.reset_table()
        with Counter() as count:
            db_pusher.push_execute_batch_version(million_data, page_size=10000)
        times_1m.append(count.elapsed)
    db.save_times_to_db("Execute_batch 1M (page_size=10000)", times_1m)
    
    
def push_copy_expert():
    
    print("COPY Expert 1k")
    times_1k = []
    for _ in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_version(thousand_data)
        times_1k.append(count.elapsed)
        print(f"Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Expert 1k", times_1k)

    print("COPY Expert 100k")
    times_100k = []
    for _ in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_version(ht_data)
        times_100k.append(count.elapsed)
        print(f"Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Expert 100k", times_100k)

    print("COPY Expert 1M")
    times_1m = []
    for _ in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_version(million_data)
        times_1m.append(count.elapsed)
        print(f"Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Expert 1M", times_1m)
    
    
def push_pandas_defaut():
    print("Pandas to_sql default 1k")
    times_1k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(thousand_data)
        times_1k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Default 1k", times_1k)
    
    print("Pandas to_sql default 100k")
    times_100k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(ht_data)
        times_1k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Default 100k", times_100k)
    
    print("Pandas to_sql default 1M")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(million_data)
        times_1k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Default 1M", times_1m)
    
    
def push_pandas_multi():

    print("Pandas to_sql (Multi + chunksize=1000) 1k")
    times_1k_multi = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(thousand_data, use_multi=True, chunksize=1000)
        times_1k_multi.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Multi 1k", times_1k_multi)

    print("Pandas to_sql (Multi + chunksize=10000)")
    times_100k_multi = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(ht_data, use_multi=True, chunksize=10000)
        times_100k_multi.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Multi 100k", times_100k_multi)

    print("Pandas to_sql (Multi + chunksize=50000) 1M")
    times_1m_multi = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_native_version(million_data, use_multi=True, chunksize=50000)
        times_1m_multi.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Multi 1M", times_1m_multi)
    
    
def push_pandas_callable_copy():
    print("Pandas to_sql (Callable COPY) 1k")
    times_100k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_copy_version(thousand_data, chunksize=100)
        times_100k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Callable COPY 1k", times_100k)
    
    print("Pandas to_sql (Callable COPY) 100k")
    times_100k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_copy_version(ht_data, chunksize=50000)
        times_100k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Callable COPY 100k", times_100k)

    print("Pandas to_sql (Callable COPY) 1M")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_pandas_copy_version(million_data, chunksize=100000)
        times_1m.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | Pic RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("Pandas Callable COPY 1M", times_1m)
    
    
def push_copy_from_tuple():
    print("COPY from tuple 1k")
    times_1k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_stream_version(thousand_data)
            
        times_1k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Stream Tuple 1k", times_1k)
    
    print("COPY from tuple 100k")
    times_100k = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_stream_version(ht_data)
            
        times_100k.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Stream Tuple 100k", times_100k)
    
    print("COPY from tuple 1M")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            db_pusher.push_copy_stream_version(million_data)
            
        times_1m.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Stream Tuple 1M", times_1m)
    
    

# Plus long à cause de Faker
# Plus léger en RAM 
# (ne se voit pas sur cette mesure car le cout de la génération Faker n'apparait pas ici)
def push_copy_stream_benchmark():
    
    print("COPY from tuple 1M")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            million_data_bis = seeder.create_million()
            db_pusher.push_copy_stream_version(million_data_bis)
            
        times_1m.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
    db.save_times_to_db("COPY Stream Tuple 1M", times_1m)
    
    print("COPY from stream 1M")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            faker_generator = seeder.create_million_on_stream()
            db_pusher.push_copy_stream_version(faker_generator)
            
        times_1m.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
        
    db.save_times_to_db("COPY Stream Faker 1M", times_1m)
    
def push_copy_stream_benchmark_no_faker():
    print("COPY from stream 1M Without Faker")
    times_1m = []
    for i in range(10):
        db.reset_table()
        with MemoryTracker() as ram, Counter() as count:
            faker_generator = generate_pure_python_stream()
            db_pusher.push_copy_stream_version(faker_generator)
            
        times_1m.append(count.elapsed)
        print(f"{count.elapsed:.4f}s | RAM = {ram.peak_mo:.2f} Mo")
        
    db.save_times_to_db("COPY Stream Faker 1M", times_1m)

def generate_pure_python_stream(n: int):
    for i in range(n):
        yield (
            i,
            f"Texte rapide numero {i}",
            "2026-06-18", 
            round(random.uniform(10.0, 999.9), 2)
        )
    
main()