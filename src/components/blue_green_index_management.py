from dotenv import load_dotenv
from ..logger import get_logger
from ..utils import get_db_connection, release_connection
# Updated imports to use the correct packages
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec# Updated import for OpenAIEmbeddings
import os
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables

load_dotenv()

client = OpenAI()
pc = Pinecone()
spec = ServerlessSpec(cloud="aws", region="us-east-1")

custom_logger = get_logger()

def get_blue_index():
    """
        Get the blue index from the index_state table.
    """
    try:
        custom_logger.info("Getting blue index...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT blue_index FROM index_state")
        blue_index = cur.fetchone()
        cur.close()
        release_connection(conn)
        # Extract the string from the tuple
        return blue_index[0] if blue_index else None
    
    except Exception as ex:
        custom_logger.error(f"Error in get_blue_index: {ex}", exc_info=True)
        return None
    
def get_green_index():
    """
        Get the green index from the index_state table.
    """
    try:
        custom_logger.info("Getting green index...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT green_index FROM index_state")
        green_index = cur.fetchone()
        cur.close()
        release_connection(conn)
        # Extract the string from the tuple
        return green_index[0] if green_index else None
    
    except Exception as ex:
        custom_logger.error(f"Error in get_green_index: {ex}", exc_info=True)
        return None
    
def save_blue_index(value):
    """
        Save the blue index to the index_state table.
    """
    try:
        custom_logger.info("Saving blue index...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("UPDATE index_state SET blue_index = %s", (value,))
        
        conn.commit()
        cur.close()
        release_connection(conn)
    
    except Exception as ex:
        custom_logger.error(f"Error in save_blue_index: {ex}", exc_info=True)
    
def save_green_index(value):
    """
        Save the green index to the index_state table.
    """
    try:
        custom_logger.info("Saving green index...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("UPDATE index_state SET green_index = %s", (value,))
        
        conn.commit()
        cur.close()
        release_connection(conn)
    
    except Exception as ex:
        custom_logger.error(f"Error in save_green_index: {ex}", exc_info=True)
        
        
def validate_green_index(index_name: str) -> bool:
    """
        Validates the newly built (green) index by:
        1. Checking index stats (e.g., vector count).
        2. Running a sample semantic search query (optional).
        3. Returning True if it meets the required criteria, False otherwise.
    """
    try:
            
        custom_logger.info(f"Validating green index: {index_name}")

        # Initialize Pinecone client
        index = pc.Index(index_name)
        
        # 1. Check index stats
        stats = index.describe_index_stats()
        total_vectors = stats["total_vector_count"]

        # threshold check: ensure the new index has at least 10 vectors
        if total_vectors <= 5:
            custom_logger.error(f"Validation failed: index '{index_name}' has too few vectors ({total_vectors}).", exc_info=True)
            return False
        
        custom_logger.info(f"Index '{index_name}' has {total_vectors} vectors.")
        
        test_query = "magic wizard adventure"
        query_embd = client.embeddings.create(input=test_query, model="text-embedding-3-small").data[0].embedding

        # A test query you expect to have relevant results
        query_results = index.query(vector=query_embd, top_k=5, include_metadata=True, namespace="default")
        if not query_results:
            custom_logger.error(f"Validation failed: no results returned for test query '{test_query}'.", exc_info=True)
            return False

        custom_logger.info(f"Validation success: found {len(query_results['matches'])} results for test query '{test_query}'.")
        return True

    except Exception as e:
        custom_logger.error(f"Error validating green index '{index_name}': {e}", exc_info=True)
        return False


def clear_index(index_name: str) -> None:
    """
        Clears (or deletes) all vectors in the specified Pinecone index.
    """
    try:
        custom_logger.info(f"Clearing index: {index_name}")
        index = pc.Index(index_name)

        # Using the updated API syntax: delete_all instead of deleteAll
        index.delete(delete_all=True, namespace="default")
        custom_logger.info(f"Index '{index_name}' cleared successfully.")

    except Exception as e:
        custom_logger.error(f"Failed to clear index '{index_name}': {e}", exc_info=True)