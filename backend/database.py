import psycopg2
import os
from dotenv import load_dotenv

#reads .env file and get database url
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


#makes a connection with the database
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn