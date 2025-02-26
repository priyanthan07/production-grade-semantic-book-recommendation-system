from ..logger import custom_logger
from ..pipelines.data_preprocessing_pipeline import data_cleaning
from ..pipelines.sentiment_analysis_pipeline import sentiment_analysis
from ..pipelines.popular_recommendation_pipeline import popular_recommendations
from ..pipelines.vector_db_pipeline import manage_vector_db


def periodic_pipeline():
    """
    Runs the periodic data pipelines:
      - Data cleaning
      - Sentiment analysis
      - Popular recommendation generation and saving to DB
    """
    try:
        custom_logger.info("Running periodic data pipelines...")
        
        # Run data cleaning
        preprocessed_df = data_cleaning()
        
        # Run sentiment analysis on the preprocessed data
        processed_df = sentiment_analysis(preprocessed_df)
        
        # Generate popular recommendations
        popular_recommendations(10)
        
        # Manage the vector database
        manage_vector_db()
        
        custom_logger.info("Periodic pipeline completed successfully.")
        
    except Exception as ex:
        custom_logger.error("Error in periodic_pipeline: %s", ex)
        raise ex