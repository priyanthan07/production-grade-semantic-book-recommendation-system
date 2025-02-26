from ..logger import custom_logger
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from langchain.docstore.document import Document
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pandas as pd
from tqdm import tqdm
from ..components.blue_green_index_management import (
    get_blue_index,
    get_green_index,
    save_blue_index,
    save_green_index,
    validate_green_index,
    clear_index
)

load_dotenv()

def manage_vector_db():
    """
        Loads a preprocessed DataFrame, extracts the tagged_description column,
        and inserts vectors into the green index. If validation passes, swap 
        the indexes (blue <-> green). If validation fails, revert to the existing blue index.
    """
    try:
        custom_logger.info("Loading preprocessed data from preprocessed_books_data table...")
        preprocessed_df = get_cleaned_books_df()
        custom_logger.info("preprocessed data loaded, shape: %s", preprocessed_df.shape)
                
        documents = [Document(page_content=text) for text in preprocessed_df["tagged_description"].tolist()]
        embeddings = OpenAIEmbeddings()
        
        blue_index = get_blue_index()
        green_index = get_green_index()
        
        custom_logger.info(f"Active (blue) index: {blue_index}, Inactive (green) index: {green_index}")
        
        chunk_size = 100  # Adjust chunk size based on your data volume and performance needs
        total_docs = len(documents)
        custom_logger.info(f"Total documents to insert: {total_docs}")
        
        custom_logger.info("Adding vectors to Pinecone...")
        
        pinecone_vectorstore = Pinecone(
            index_name=green_index,
            embedding=embeddings
        )
        
        for i in tqdm(range(0, total_docs, chunk_size), desc="Inserting vectors"):
            chunk_docs = documents[i : i + chunk_size]
            pinecone_vectorstore.add_documents(chunk_docs)

        custom_logger.info(f"All documents inserted into the green index '{green_index}'")
        
        ## validation
        if validate_green_index(green_index):
            custom_logger.info("Green index validation passed. Swapping indexes...")
            save_blue_index(green_index)
            save_green_index(blue_index)
            clear_index(green_index)
            custom_logger.info(f"Swapped: new blue index is '{green_index}', old blue index is now '{blue_index}'")
        
        else:
            # Validation failed, revert to the existing blue index
            custom_logger.error("Green index validation failed. Rollback to the existing blue index.")
            clear_index(green_index)            
        
    except Exception as ex:
        custom_logger.error("Error in sentiment_analysis_pipeline: %s", ex)
