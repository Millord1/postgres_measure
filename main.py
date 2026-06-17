from dotenv import load_dotenv
from database import DataBase
import os

load_dotenv()

PW = os.getenv('PW')
USER = os.getenv('USER')
DB_NAME = os.getenv('DB_NAME')

def main():
    db = DataBase(DB_NAME, USER, PW)