from ..logger import custom_logger
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from langchain.docstore.document import Document
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import Pinecone  # Updated import
import pandas as pd
from tqdm import tqdm
import pinecone
import os
from ..components.blue_green_index_management import (
    get_blue_index,
    get_green_index,
    save_blue_index,
    save_green_index,
    validate_green_index,
    clear_index,
    check_openai_key
)

load_dotenv()

def manage_vector_db():
    """
        Loads a preprocessed DataFrame, extracts the tagged_description column,
        and inserts vectors into the green index. If validation passes, swap 
        the indexes (blue <-> green). If validation fails, revert to the existing blue index.
    """
    try:
        # Check OpenAI API key before proceeding
        if not check_openai_key():
            custom_logger.error("OpenAI API key validation failed. Cannot proceed with vector DB management.")
            return
            
        custom_logger.info("Loading preprocessed data from preprocessed_books_data table...")
        preprocessed_df = get_cleaned_books_df()
        custom_logger.info("preprocessed data loaded, shape: %s", preprocessed_df.shape)
        
        # Create documents list with metadata
        documents = []
        for idx, row in preprocessed_df.iterrows():
            doc = Document(
                page_content=row["tagged_description"],
                metadata={"book_id": str(row.get("book_id", idx))}
            )
            documents.append(doc)
            
        # Initialize OpenAI embeddings with explicit API key
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # Specify model explicitly
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Pass API key explicitly
        )
        
        blue_index_name = get_blue_index()
        green_index_name = get_green_index()
        
        custom_logger.info(f"Active (blue) index: {blue_index_name}, Inactive (green) index: {green_index_name}")
        
        chunk_size = 100  # Adjust chunk size based on your data volume and performance needs
        total_docs = len(documents)
        custom_logger.info(f"Total documents to insert: {total_docs}")
        
        custom_logger.info("Adding vectors to Pinecone...")
        
        # Initialize Pinecone client with explicit API key
        pinecone_client = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        # Get the green index
        green_index = pinecone_client.Index(green_index_name)
        
        # Create LangChain vectorstore with the Pinecone index
        pinecone_vectorstore = Pinecone(
            index=green_index,  # Pass the index object instead of the name
            embedding=embeddings,
            text_key="text"  # Specify the text key that stores your documents
        )
        
        for i in tqdm(range(0, total_docs, chunk_size), desc="Inserting vectors"):
            chunk_docs = documents[i : i + chunk_size]
            pinecone_vectorstore.add_documents(chunk_docs)
            
        custom_logger.info(f"All documents inserted into the green index '{green_index_name}'")
        
        # validation
        if validate_green_index(green_index_name):
            custom_logger.info("Green index validation passed. Swapping indexes...")
            # Swap blue and green indices
            save_blue_index(green_index_name)
            save_green_index(blue_index_name)
            custom_logger.info(f"Swapped: new blue index is '{green_index_name}', old blue index is now '{blue_index_name}'")
            
        else:
            # Validation failed, revert to the existing blue index
            custom_logger.error("Green index validation failed. Rollback to the existing blue index.")
            clear_index(green_index_name)
            
    except Exception as ex:
        custom_logger.error("Error in vector_db_pipeline: %s", ex)