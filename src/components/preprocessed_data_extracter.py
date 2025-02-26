import pandas as pd
from ..utils import get_db_connection, release_connection
from ..logger import custom_logger


def get_cleaned_books_df()-> pd.DataFrame:
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM preprocessed_books_data", con=conn)
        return df
    
    except Exception as e:
        custom_logger.error("Error in get_cleaned_books_df: %s", e)
        return None
    
    finally:
        release_connection(conn)
        
    

