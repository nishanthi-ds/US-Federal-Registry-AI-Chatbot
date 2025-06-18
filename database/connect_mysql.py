import mysql.connector
from utils.config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)