from ..components.get_emotion_scores import calculate_emotion_scores
from ..utils import  save_cleaned_data_to_db
from ..logger import get_logger
import pandas as pd

custom_logger = get_logger()

def sentiment_analysis(preprocessed_df)-> pd.DataFrame:
    """
        Takes in a preprocessed DataFrame and returns the DataFrame with emotion scores added.
    """
    try:
        # Calculate emotion scores
        sentiment_df = calculate_emotion_scores(preprocessed_df)
        custom_logger.info("Emotion scores calculated successfully: %s", sentiment_df.shape)
        
        save_cleaned_data_to_db(sentiment_df, "preprocessed_books_data")
        
        custom_logger.info("preprocessed data saved to database")
        
        return sentiment_df
        
    except Exception as ex:
        custom_logger.error("Error in sentiment_analysis_pipeline: %s", ex)
        return None