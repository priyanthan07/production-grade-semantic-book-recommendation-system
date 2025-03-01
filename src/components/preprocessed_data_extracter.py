import pandas as pd
from ..utils import get_db_connection, release_connection
from ..logger import get_logger

custom_logger = get_logger()

def get_cleaned_books_df()-> pd.DataFrame:
    conn = get_db_connection()
    try:
        
        query = "SELECT * FROM preprocessed_books_data"
        
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()                   # Fetch all rows as a list of tuples
        columns = [desc[0] for desc in cur.description]  # Extract column names
        cur.close()

        # Convert the list of tuples to a Pandas DataFrame with appropriate column names
        df = pd.DataFrame(rows, columns=columns)
        
        return df
    
    except Exception as e:
        custom_logger.error("Error in get_cleaned_books_df: %s", e)
        return None
    
    finally:
        release_connection(conn)
