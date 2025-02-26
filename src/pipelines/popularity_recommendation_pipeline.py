import pandas as pd
from ..logger import custom_logger
from ..components.preprocessed_data_extracter import get_cleaned_books_df




def popular_recommendations(n: int) -> pd.DataFrame:
    """
    Popularity-based recommendation pipeline.

    """
    try:
        custom_logger.info("Generating popularity-based recommendations...")
        df = get_cleaned_books_df()
        
        df = df[["isbn13", "title", "average_rating", "ratings_count"]].sort_values(by="ratings_count" ,ascending=False)
        pop_recommendations = df[(df["average_rating"]>4.1) & (df["ratings_count"]>500000)].sort_values(by="ratings_count" ,ascending=False)
        
        custom_logger.info("Popularity-based recommendations generated successfully.")
        return pop_recommendations.head(n)
        
    
    except Exception as ex:
        custom_logger.error("Error in popularity_recommendation_pipeline: %s", ex)
        return None