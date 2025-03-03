from ..logger import get_logger
from ..components.raw_data_extracter import get_raw_books_df
from ..components.fill_missing_simple_categories import fill_missing_simple_cat
from ..components.map_categories import get_simplified_categories
from ..utils import save_cleaned_data_to_db
import numpy as np
import pandas as pd

custom_logger = get_logger()

def data_cleaning()-> pd.DataFrame:
    """
        Reads raw data from the books table, cleans the data, applies feature engineering,
        and returns the cleaned result.
    """
    try:
        
        raw_df = get_raw_books_df()
        custom_logger.info("Raw data loaded, shape: %s", raw_df.shape)
        
        # drop any row where any one of the specified columns contains a missing value (NaN)
        # and .copy() method then creates a new DataFrame from the resulting data.
        cleaned_df = raw_df.dropna(subset=["description", "num_pages", "average_rating", "published_year", "ratings_count"]).copy()
        custom_logger.info("Filtered out rows with missing critical fields, new shape: %s", cleaned_df.shape)
        
        # Calculate word counts for description and filter out short ones (<25 words)
        cleaned_df["word_counts_in_desc"] = cleaned_df["description"].str.split().str.len()
        cleaned_df = cleaned_df[cleaned_df["word_counts_in_desc"] >= 30]
        custom_logger.info("Filtered out rows with short descriptions, new shape: %s", cleaned_df.shape)
        
        # Create a combined title and subtitle column (handling missing subtitles)
        cleaned_df["title_and_subtitle"] = np.where(cleaned_df["subtitle"].isna(),
                                                    cleaned_df["title"],
                                                    cleaned_df[["title", "subtitle"]].astype(str).agg(":".join, axis=1))
        
        cleaned_df = get_simplified_categories(cleaned_df)
        
        missing_cat_mask = cleaned_df["simple_categories"].isna()
        
        if missing_cat_mask.any():
            custom_logger.info("Filling missing simple_categories using LLM predictions...")
                        
            # Extract the descriptions as a list from rows where simple_categories is missing
            descriptions = cleaned_df.loc[missing_cat_mask, "description"].tolist()
            
            # Process the descriptions in parallel
            predictions = fill_missing_simple_cat(descriptions)
            
            # Assign the predictions back to the DataFrame
            cleaned_df.loc[missing_cat_mask, "simple_categories"] = predictions
            
    
        # Drop columns no longer needed
        cleaned_df.drop(columns=["subtitle", "word_counts_in_desc"], inplace=True)
        custom_logger.info("Droped %s columns ", ["subtitle", "word_counts_in_desc"])
        
        custom_logger.info("Adding tagged_description to DataFrame...")
        cleaned_df["tagged_description"] = cleaned_df[["isbn13", "description"]].astype(str).agg(" ".join, axis=1)
        
        custom_logger.info("Cleaned data saved to cleaned_books table, shape: %s", cleaned_df.shape)
        
        return cleaned_df

    except Exception as ex:
        custom_logger.error(f"Error in data_cleaning_pipeline: [ex]", exc_info=True)