import os
import psycopg2
from psycopg2 import extras
from psycopg2 import pool
from .logger import get_logger
from dotenv import load_dotenv
load_dotenv()

custom_logger = get_logger()

try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1, 
        maxconn=10, 
        user=os.getenv("PG_USERNAME"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        database=os.getenv("PG_DBNAME")
    )
except Exception as e:
    raise e

def get_db_connection():
    """
    Get a connection from the pool.
    """
    try:
       conn = connection_pool.getconn()
       if conn:
          conn.autocommit = True 
          return conn
       
    except Exception as e:
       raise e


def release_connection(conn):
    """
    Return a connection back to the pool instead of closing it.
    """
    try:
        if conn:
            connection_pool.putconn(conn)
    except Exception as e:
        raise e


def close_pool():
    """
    Close all connections when shutting down the application.
    """
    try:
        if connection_pool:
            connection_pool.closeall()
    except Exception as e:
        raise e
    
def get_query_index():
    """
        Get the query index from the index_state table.
    """
    conn = None
    try:
        custom_logger.info("Getting query index...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT query_index FROM index_state")
        query_index = cur.fetchone()
        cur.close()

        return query_index
    
    except Exception as ex:
        custom_logger.error(f"Error in get_query_index: {e}", exc_info=True)
        return None
    finally:
        release_connection(conn)
    
def save_query_index(value):
    """
        Get the query index from the index_state table.
    """
    try:
        custom_logger.info("Getting query index...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("UPDATE index_state SET query_index = %s", (value,))
        
        conn.commit()
        cur.close()
        release_connection(conn)
    
    except Exception as ex:
        custom_logger.error(f"Error in save_query_index: {e}", exc_info=True)
    
def save_cleaned_data_to_db(df, table_name):
    """
        Save the cleaned data to the specified table in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        
        custom_logger.info("Saving cleaned data to %s table...", table_name)
        columns = list(df.columns)
        cols_str = ", ".join(columns)
        
        # Convert DataFrame rows into a list of tuples
        data_tuples = [tuple(row) for row in df.to_numpy()]
        
        query = f"INSERT INTO {table_name} ({cols_str}) VALUES %s"
        
        extras.execute_values(cursor, query, data_tuples)
        conn.commit()
        cursor.close()
        custom_logger.info("Data successfully inserted into %s", table_name)
                
    except Exception as e:
        conn.rollback()
        custom_logger.error(f"Error inserting data into {table_name}: {e}", exc_info=True)
        raise e
    finally:
        release_connection(conn)
        
def save_popular_data_to_db(df, table_name):
    """
        Save the popular books data to the specified table in the database.
        The table is cleared first (old data is removed) and then new data is inserted.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        custom_logger.info("Clearing previous data from %s table...", table_name)
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
        
        columns = list(df.columns)
        cols_str = ", ".join(columns)
        custom_logger.info("Saving popular books data to %s table. columns : %s", table_name, cols_str)
        
        # Convert DataFrame rows into a list of tuples
        data_tuples = [tuple(row) for row in df.to_numpy()]
        
        query = f"INSERT INTO {table_name} ({cols_str}) VALUES %s"
        
        extras.execute_values(cursor, query, data_tuples)
        conn.commit()
        cursor.close()
        custom_logger.info("Data successfully inserted into %s", table_name)
                
    except Exception as e:
        conn.rollback()
        custom_logger.error(f"Error inserting data into {table_name}: {e}", exc_info=True)
        raise e
    
    finally:
        release_connection(conn)


    