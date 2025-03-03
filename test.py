# from src.pipelines.data_preprocessing_pipeline import data_cleaning
# from src.pipelines.sentiment_analysis_pipeline import sentiment_analysis
# from src.pipelines.popular_recommendation_pipeline import popular_recommendations
# from src.pipelines.vector_db_pipeline import manage_vector_db
from src.components.preprocessed_data_extracter import get_cleaned_books_df
import pandas as pd
import json


if __name__ == "__main__":
    
    

# Create DataFrame with book data
    data = {
        "isbn13": ["9780002005883", "9780002261982", "9780006163831", "9780006178736", "9780006280897"],
        "isbn10": ["0002005883", "0002261987", "0006163831", "0006178731", "0006280897"],
        "title": ["Gilead", "Spider's Web", "The One Tree", "Rage of Angels", "The Four Loves"],
        "subtitle": [None, "A Novel", None, None, None],
        "authors": ["Marilynne Robinson", "Charles Osborne;Agatha Christie", "Stephen R. Donaldson", "Sidney Sheldon", "Clive Staples Lewis"],
        "categories": ["Fiction", "Detective and mystery stories", "American fiction", "Fiction", "Christian life"],
        "thumbnail": [
            "http://books.google.com/books/content?id=KQZCP...",
            "http://books.google.com/books/content?id=gA5GP...",
            "http://books.google.com/books/content?id=OmQaw...",
            "http://books.google.com/books/content?id=FKo2T...",
            "http://books.google.com/books/content?id=XhQ5X...",
        ],
        "description": [
            "A NOVEL THAT READERS and critics have been eager...",
            "A new 'Christie for Christmas' -- a full-length...",
            "Volume Two of Stephen Donaldson's acclaimed series...",
            "A memorable, mesmerizing heroine Jennifer -- battling...",
            "Lewis' work on the nature of love divides love into...",
        ],
        "published_year": [2004, 2000, 1982, 1993, 2002],
        "average_rating": [3.85, 3.83, 3.97, 3.93, 4.15],
        "num_pages": [247, 241, 479, 512, 170],
        "ratings_count": [361, 5164, 172, 29532, 33684],
    }

    # # Convert to DataFrame
    # df = pd.DataFrame(data)

    # # Display the DataFrame
    # print(df.columns)
    
    
    # df = data_cleaning()
    # print(df.columns)
    # df = sentiment_analysis(df)
    # print(df.isna().sum())
    
    # popular_recommendations(10)
    df = get_cleaned_books_df()
    df = df.head(2)
    json_str = df.to_json(orient="records")
    print(json_str)
