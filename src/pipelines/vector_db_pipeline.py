from ..logger import get_logger
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from tqdm.auto import tqdm
import os
import time
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from ..components.blue_green_index_management import (
                                                        get_blue_index,
                                                        get_green_index,
                                                        save_blue_index,
                                                        save_green_index,
                                                        validate_green_index,
                                                        clear_index
                                                    )

load_dotenv()

client = OpenAI()
pc = Pinecone()
spec = ServerlessSpec(cloud="aws", region="us-east-1")

custom_logger = get_logger()

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
        
        # Create documents list with unique IDs
        documents = []
        document_ids = []
        for idx, row in preprocessed_df.iterrows():
            documents.append(row["tagged_description"])
            # Use stable IDs based on DataFrame index
            document_ids.append(f"doc_{idx}")
        
        blue_index_name = get_blue_index()
        green_index_name = get_green_index()
        
        custom_logger.info(f"Active (blue) index: {blue_index_name}, Inactive (green) index: {green_index_name}")

        # Connect to index
        green_index = pc.Index(green_index_name)
        time.sleep(30)
        
        # View index stats
        stats = green_index.describe_index_stats()
        custom_logger.info("Adding vectors to Pinecone. Initial index stats: %s", stats)
        time.sleep(30)
        
        # Smaller batch size to avoid overwhelming the free tier
        batch_size = 8
        max_retries = 3
        
        for i in tqdm(range(0, len(documents), batch_size), desc="Inserting vectors"):
            # Set end position of batch
            i_end = min(i+batch_size, len(documents))
            
            # Get batch of lines and IDs
            lines_batch = documents[i:i_end]
            ids_batch = document_ids[i:i_end]
            
            # Create embeddings
            response = client.embeddings.create(input=lines_batch, model="text-embedding-3-small")
            embeds = [record.embedding for record in response.data]
            
            # Prepare metadata and upsert batch
            meta = [{'text': line} for line in lines_batch]
            to_upsert = list(zip(ids_batch, embeds, meta))
            
            # Get stats before upserting
            stats_before = green_index.describe_index_stats()
            total_before = stats_before.get('total_vector_count', 0)
           
            # Upsert to Pinecone with retries
            retry_count = 0
            while retry_count < max_retries:
                try:
                    green_index.upsert(vectors=to_upsert, namespace="default")
                    wait_time = 5 if i//batch_size >= 2 else 20
                    time.sleep(wait_time)
                    break
                
                except Exception as e:
                    retry_count += 1
                    custom_logger.error(f"Error upserting vectors (attempt {retry_count}/{max_retries}): {e}", exc_info=True)
                    time.sleep(2 * retry_count)  # Exponential backoff
                    if retry_count == max_retries:
                        custom_logger.error("Max retries reached, moving to next batch", exc_info=True)
            
            # Get stats after upserting
            time.sleep(1)  # Wait for stats to update
            stats_after = green_index.describe_index_stats()
            total_after = stats_after.get('total_vector_count', 0)
            
            # Verify vectors were inserted
            if total_after <= total_before:
                custom_logger.warning(f"No new vectors added in batch {i//batch_size}. Before: {total_before}, After: {total_after}")
                # Try to query for one of the vectors to verify it was added
                try:
                    query_results = green_index.fetch(ids=[ids_batch[0]], namespace="default")
                    if query_results and ids_batch[0] in query_results.get('vectors', {}):
                        custom_logger.info(f"Vector {ids_batch[0]} was successfully fetched despite count not increasing")
                    else:
                        custom_logger.error(f"Vector {ids_batch[0]} was not found in index", exc_info=True)
                except Exception as fetch_error:
                    custom_logger.error(f"Error fetching vector: {fetch_error}", exc_info=True)
        
        # Final check of index stats
        final_stats = green_index.describe_index_stats()
        custom_logger.info("All documents processed. Final index stats: %s", final_stats)
        
        # Validation
        if validate_green_index(green_index_name):
            custom_logger.info("Green index validation passed. Swapping indexes...")
            # Swap blue and green indices
            save_blue_index(green_index_name)
            save_green_index(blue_index_name)
            custom_logger.info(f"Swapped: new blue index is '{green_index_name}', new green index is now '{blue_index_name}'")
            clear_index(blue_index_name)
            custom_logger.info(f"Old blue index '{blue_index_name}' cleared")
        else:
            # Validation failed, revert to the existing blue index
            custom_logger.error("Green index validation failed. Rollback to the existing blue index and clear the green index", exc_info=True)
            clear_index(green_index_name)
            
    except Exception as ex:
        custom_logger.error(f"Error in vector_db_pipeline: {ex}", exc_info=True)