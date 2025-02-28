import pandas as pd
from ..logger import custom_logger
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from ..utils import save_popular_data_to_db

def popular_recommendations(n: int = 10) -> pd.DataFrame:
    """
    Popularity-based recommendation pipeline.
    Returns top n popular books with high ratings.
    """
    try:
        custom_logger.info("Generating popularity-based recommendations...")
        df = get_cleaned_books_df()
        
        # Make sure required columns exist
        required_columns = ["isbn13", "title", "average_rating", "ratings_count"]
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            custom_logger.error(f"Missing required columns: {missing}")
            return None
        
        # Select and sort by popularity
        pop_df = df[required_columns].copy()
        
        # Log data distribution to help understand filter thresholds
        custom_logger.info(f"Ratings count stats - min: {pop_df['ratings_count'].min()}, "
                          f"max: {pop_df['ratings_count'].max()}, "
                          f"median: {pop_df['ratings_count'].median()}")
        
        custom_logger.info(f"Average rating stats - min: {pop_df['average_rating'].min()}, "
                          f"max: {pop_df['average_rating'].max()}, "
                          f"median: {pop_df['average_rating'].median()}")
        
        # Use less restrictive filters (adjust these based on your actual data)
        pop_recommendations = pop_df[
            (pop_df["average_rating"] > 4.0) & 
            (pop_df["ratings_count"] > 1000)
        ].sort_values(by="ratings_count", ascending=False)
        
        custom_logger.info(f"Found {len(pop_recommendations)} books matching popularity criteria")
        
        # Take top n recommendations
        top_n = pop_recommendations.head(n)
        
        if len(top_n) == 0:
            custom_logger.warning("No books met the popularity criteria!")
            return None
            
        # Ensure correct data types for database
        top_n["isbn13"] = top_n["isbn13"].astype(str)
        top_n["title"] = top_n["title"].astype(str)
        top_n["average_rating"] = top_n["average_rating"].astype(float)
        top_n["ratings_count"] = top_n["ratings_count"].astype(float)
        
        # Save to database
        save_popular_data_to_db(top_n, "popular_recommendations")
        
        custom_logger.info(f"Saved {len(top_n)} popular recommendations to database")
        
        return top_n
    
    except Exception as ex:
        custom_logger.error(f"Error in popularity_recommendation_pipeline: {ex}")
        return None