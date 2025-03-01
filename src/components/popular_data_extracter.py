import pandas as pd
from ..utils import get_db_connection, release_connection
from ..logger import get_logger

custom_logger = get_logger()

def get_popular_books_df()-> pd.DataFrame:
    """
        Get the popular books data from the popular_recommendations table.
    """
    
    conn = get_db_connection()
    try:
        custom_logger.info("Getting popular books data from popular_recommendations table...")
        cur = conn.cursor()
        cur.execute("SELECT * FROM popular_recommendations")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        cur.close()
        return df
    
    except Exception as e:
        custom_logger.error("Error in get_popular_books_df: %s", e)
        return None
    
    finally:
        release_connection(conn)
        
    

