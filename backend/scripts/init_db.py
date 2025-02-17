import psycopg2
from decouple import config
import sys
import os

def init_database():
    # Get database URL from environment
    db_url = config('DATABASE_URL')
    
    # Parse database URL
    db_info = db_url.replace('postgresql://', '').split('/')
    db_credentials = db_info[0].split('@')
    user_pass = db_credentials[0].split(':')
    host_port = db_credentials[1].split(':')
    
    username = user_pass[0]
    password = user_pass[1]
    host = host_port[0]
    port = host_port[1]
    database = db_info[1]
    
    # Connect to PostgreSQL
    try:
        # Connect to default database
        conn = psycopg2.connect(
            dbname='postgres',
            user=username,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database}'")
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE {database}')
            print(f"Database '{database}' created successfully")
        else:
            print(f"Database '{database}' already exists")
            
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    if init_database():
        print("Database initialization completed successfully")
    else:
        print("Database initialization failed")
        sys.exit(1) 