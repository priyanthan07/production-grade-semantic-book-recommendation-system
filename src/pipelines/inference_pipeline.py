from ..components.inference_engine import recommend_book
from ..logger import get_logger
import pandas as pd

custom_logger = get_logger()

def get_recommendations(query: str, category:str, tone:str)-> pd.DataFrame:
    """
        Takes in a query, category and tone and returns the recommendations.
    """
    try:
        custom_logger.info("Getting recommendations...")
        # Get recommendations
        return recommend_book(query, category, tone)
        
    except Exception as ex:
        custom_logger.error(f"Error in sentiment_analysis_pipeline: {ex}", exc_info=True)
        return None