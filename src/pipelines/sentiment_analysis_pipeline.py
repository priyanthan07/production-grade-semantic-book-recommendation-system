from ..components.get_emotion_scores import calculate_emotion_scores
from ..utils import  save_cleaned_data_to_db
from ..logger import custom_logger
import pandas as pd



def sentiment_analysis(preprocessed_df)-> pd.DataFrame:
    """
        Takes in a preprocessed DataFrame and returns the DataFrame with emotion scores added.
    """
    try:
        custom_logger.info("Calculating emotion scores...")
        # Calculate emotion scores
        sentiment_df = calculate_emotion_scores(preprocessed_df)
        custom_logger.info("Emotion scores calculated successfully.{sentiment_df.shape}")
        
        save_cleaned_data_to_db(sentiment_df, "preprocessed_books_data")
        
        custom_logger.info("preprocessed data saved to database")
        
        return sentiment_df
        
    except Exception as ex:
        custom_logger.error("Error in sentiment_analysis_pipeline: %s", ex)
        return None