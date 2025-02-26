from ..components.inference_engine import recommend_book
from ..logger import custom_logger
import pandas as pd



def get_recommendations(query: str, category:str, tone:str)-> pd.DataFrame:
    """
        Takes in a query, category and tone and returns the recommendations.
    """
    try:
        custom_logger.info("Getting recommendations...")
        # Get recommendations
        return recommend_book(query, category, tone)
        
    except Exception as ex:
        custom_logger.error("Error in sentiment_analysis_pipeline: %s", ex)
        return None