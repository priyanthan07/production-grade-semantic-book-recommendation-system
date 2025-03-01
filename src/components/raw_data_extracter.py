import pandas as pd
from ..utils import get_db_connection, release_connection, get_query_index, save_query_index
from ..logger import get_logger

custom_logger = get_logger()


def get_raw_books_df()-> pd.DataFrame:
    """
        Retrieves a batch of raw book data from the books table using the last saved query index.
        After retrieving, it updates the query index to the max id from the current batch.
    """
        
    conn = get_db_connection()
    try:
        batch_size = 100
        last_index = get_query_index()
        
        if isinstance(last_index, tuple):
            last_index = last_index[0]

        custom_logger.info("Loading raw data from books table... Last index: %s", last_index)

        if last_index is None or last_index == 1:
            query = f"SELECT * FROM books ORDER BY id LIMIT {batch_size}"
        else:
            query = f"SELECT * FROM books WHERE id > {last_index} ORDER BY id LIMIT {batch_size}"
        
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()                   # Fetch all rows as a list of tuples
        columns = [desc[0] for desc in cur.description]  # Extract column names
        cur.close()

        # Convert the list of tuples to a Pandas DataFrame with appropriate column names
        raw_df = pd.DataFrame(rows, columns=columns)
        custom_logger.info("Retrieved %d rows from books table.", len(raw_df))
        
        if not raw_df.empty:
            new_index = int(raw_df["id"].max())
            save_query_index(new_index)
            custom_logger.info("Updated query index to %s", new_index)
        else:
            custom_logger.info("No new data found. Query index remains unchanged.")
        
        return raw_df
    
    except Exception as e:
        custom_logger.error("Error in get_raw_books_df: %s", e)
        return None
    
    finally:
        release_connection(conn)
        