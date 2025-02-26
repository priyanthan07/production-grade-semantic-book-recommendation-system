import pandas as pd
from ..logger import custom_logger



def get_simplified_categories(df: pd.DataFrame)-> pd.DataFrame:
    try:
        custom_logger.info("Mapping categories to simplified categories...")
        # Map categories to simplified categories
        category_mapping = {
            "Fiction": "Fiction",
            "Juvenile Fiction": "Fiction",
            "Comics & Graphic Novels": "Fiction",
            "Drama": "Fiction",
            "Poetry": "Fiction",
            "Literary Collections": "Fiction",
            "Literary Criticism": "Fiction",
            "Biography & Autobiography": "Nonfiction",
            "History": "Nonfiction",
            "Philosophy": "Nonfiction",
            "Religion": "Nonfiction",
            "Social Science": "Nonfiction",
            "Political Science": "Nonfiction",
            "Psychology": "Nonfiction",
            "Self-Help": "Nonfiction",
            "Health & Fitness": "Nonfiction"
        }
        
        df["simple_categories"] = df["categories"].map(category_mapping)
        return df
        
    except Exception as e:
        custom_logger.info("Error in get_simplified_categories: %s", e)
        return None
