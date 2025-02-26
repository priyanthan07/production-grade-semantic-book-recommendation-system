from ..components.get_emotion_scores import calculate_emotion_scores
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
        
        return sentiment_df
        
    except Exception as ex:
        custom_logger.error("Error in sentiment_analysis_pipeline: %s", ex)
        return None