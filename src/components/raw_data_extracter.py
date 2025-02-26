import pandas as pd
from ..utils import get_db_connection, release_connection
from ..logger import custom_logger


def get_raw_books_df()-> pd.DataFrame:
    conn = get_db_connection()
    try:
        custom_logger.info("Loading raw data from books table...")
        raw_df = pd.read_sql("SELECT * FROM books", con=conn)
        return raw_df
    
    except Exception as e:
        custom_logger.error("Error in get_raw_books_df: %s", e)
        return None
    
    finally:
        release_connection(conn)
        
    

