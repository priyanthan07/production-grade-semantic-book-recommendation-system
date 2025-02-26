from dotenv import load_dotenv
from ..logger import custom_logger
from ..utils import get_db_connection, release_connection
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import os

load_dotenv()



def get_blue_index():
    """
        Get the blue index from the index_state table.
    """
    try:
        custom_logger.info("Getting blue index...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT blue-index FROM index_state")
        blue_index = cur.fetchone()
        cur.close()
        release_connection(conn)
        return blue_index
    
    except Exception as ex:
        custom_logger.error("Error in get_blue_index: %s", ex)
        return None
    
def get_green_index():
    """
        Get the green index from the index_state table.
    """
    try:
        custom_logger.info("Getting green index...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT green-index FROM index_state")
        green_index = cur.fetchone()
        cur.close()
        release_connection(conn)
        return green_index
    
    except Exception as ex:
        custom_logger.error("Error in get_green_index: %s", ex)
        return None
    
def save_blue_index(value):
    """
        Get the blue index from the index_state table.
    """
    try:
        custom_logger.info("Getting blue index...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("UPDATE index_state SET blue-index = %s", (value,))
        
        conn.commit()
        cur.close()
        release_connection(conn)
    
    except Exception as ex:
        custom_logger.error("Error in get_blue_index: %s", ex)
    
def save_green_index(value):
    """
        Get the green index from the index_state table.
    """
    try:
        custom_logger.info("Getting green index...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("UPDATE index_state SET green-index = %s", (value,))
        
        conn.commit()
        cur.close()
        release_connection(conn)
    
    except Exception as ex:
        custom_logger.error("Error in get_green_index: %s", ex)
        
        
        
def validate_green_index(index_name: str) -> bool:
    """
        Validates the newly built (green) index by:
        1. Checking index stats (e.g., vector count).
        2. Running a sample semantic search query (optional).
        3. Returning True if it meets the required criteria, False otherwise.
    """
    try:
        custom_logger.info(f"Validating green index: {index_name}")

        # 1. Check index stats
        index_client = Pinecone.Index(index_name)
        stats = index_client.describe_index_stats()
        total_vectors = stats["total_vector_count"]
        custom_logger.info(f"Index '{index_name}' has {total_vectors} vectors.")

        # threshold check: ensure the new index has at least 10 vectors
        if total_vectors <= 10:
            custom_logger.error(f"Validation failed: index '{index_name}' has too few vectors ({total_vectors}).")
            return False

        embeddings = OpenAIEmbeddings()
        vectorstore = Pinecone(
            index_name=index_name,
            embedding=embeddings
        )

        # A test query you expect to have relevant results
        test_query = "magic wizard adventure"
        query_results = vectorstore.similarity_search(test_query, k=3)

        if not query_results:
            custom_logger.error(f"Validation failed: no results returned for test query '{test_query}'.")
            return False

        custom_logger.info(f"Validation success: found {len(query_results)} results for test query '{test_query}'.")

        return True

    except Exception as e:
        custom_logger.error(f"Error validating green index '{index_name}': {e}")
        return False


def clear_index(index_name: str) -> None:
    """
    Clears (or deletes) all vectors in the specified Pinecone index.
    """
    try:
        custom_logger.info(f"Clearing index: {index_name}")
        index_client = Pinecone.Index(index_name)

        # deleteAll=True removes all vectors. You can also delete specific IDs if needed.
        index_client.delete(deleteAll=True)
        custom_logger.info(f"Index '{index_name}' cleared successfully.")

    except Exception as e:
        custom_logger.error(f"Failed to clear index '{index_name}': {e}")