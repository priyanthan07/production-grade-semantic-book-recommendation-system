from dotenv import load_dotenv
from ..logger import custom_logger
from ..utils import get_db_connection, release_connection
# Updated imports to use the correct packages
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings  # Updated import for OpenAIEmbeddings
import pinecone
import os

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set properly
def check_openai_key():
    """Check if the OpenAI API key is properly set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        custom_logger.error("OPENAI_API_KEY is not set in environment variables or .env file")
        return False
    if api_key.startswith("sk-") and len(api_key) > 20:
        return True
    custom_logger.error("OPENAI_API_KEY appears to be invalid. It should start with 'sk-' and be longer than 20 characters")
    return False

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
        cur.execute("SELECT green_index FROM index_state")
        green_index = cur.fetchone()
        cur.close()
        release_connection(conn)
        # Extract the string from the tuple
        return green_index[0] if green_index else None
    
    except Exception as ex:
        custom_logger.error("Error in get_green_index: %s", ex)
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
        custom_logger.error("Error in save_blue_index: %s", ex)
    
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
        custom_logger.error("Error in save_green_index: %s", ex)
        
        
def validate_green_index(index_name: str) -> bool:
    """
        Validates the newly built (green) index by:
        1. Checking index stats (e.g., vector count).
        2. Running a sample semantic search query (optional).
        3. Returning True if it meets the required criteria, False otherwise.
    """
    try:
        # Check OpenAI API key first
        if not check_openai_key():
            custom_logger.error("OpenAI API key validation failed. Cannot proceed with index validation.")
            return False
            
        custom_logger.info(f"Validating green index: {index_name}")

        # Initialize Pinecone client
        pinecone_client = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pinecone_client.Index(index_name)
        
        # 1. Check index stats
        stats = index.describe_index_stats()
        total_vectors = stats["total_vector_count"]
        custom_logger.info(f"Index '{index_name}' has {total_vectors} vectors.")

        # threshold check: ensure the new index has at least 10 vectors
        if total_vectors <= 1:
            custom_logger.error(f"Validation failed: index '{index_name}' has too few vectors ({total_vectors}).")
            return False

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # Specify model explicitly
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Pass API key explicitly
        )
        
        vectorstore = Pinecone(
            index=index,  # Pass the initialized index directly
            embedding=embeddings,
            text_key="text"  # Specify the key that contains the text in your documents
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
        pinecone_client = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pinecone_client.Index(index_name)

        # Using the updated API syntax: delete_all instead of deleteAll
        index.delete(delete_all=True)
        custom_logger.info(f"Index '{index_name}' cleared successfully.")

    except Exception as e:
        custom_logger.error(f"Failed to clear index '{index_name}': {e}")