from ..logger import get_logger
from ..pipelines.data_preprocessing_pipeline import data_cleaning
from ..pipelines.sentiment_analysis_pipeline import sentiment_analysis
from ..pipelines.popular_recommendation_pipeline import popular_recommendations
from ..pipelines.vector_db_pipeline import manage_vector_db

custom_logger = get_logger()

def periodic_pipeline():
    """
    Runs the periodic data pipelines:
      - Data cleaning
      - Sentiment analysis
      - Popular recommendation generation and saving to DB
      - Vector database management
    """
    try:
        custom_logger.info("Running periodic data pipelines...")
        
        # Run data cleaning
        custom_logger.info("Starting data cleaning pipeline...")
        preprocessed_df = data_cleaning()
        custom_logger.info("Data cleaning pipeline completed successfully.")
        
        # Run sentiment analysis on the preprocessed data
        custom_logger.info("Starting sentiment analysis pipeline...")
        processed_df = sentiment_analysis(preprocessed_df)
        custom_logger.info("Sentiment analysis pipeline completed successfully.")
        
        # Generate popular recommendations
        custom_logger.info("Starting popular recommendations pipeline...")
        popular_recommendations(10)
        custom_logger.info("Popular recommendations pipeline completed successfully.")
        
        # Manage the vector database
        custom_logger.info("Starting vector database management...")
        manage_vector_db()
        custom_logger.info("Vector database management completed successfully.")
        
        custom_logger.info("Periodic pipeline completed successfully.")
        
    except Exception as ex:
        custom_logger.error(f"Error in periodic_pipeline: {ex}", exc_info=True)
        raise ex