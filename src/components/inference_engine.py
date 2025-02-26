import os
import pandas as pd
from dotenv import load_dotenv
from ..logger import custom_logger
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from ..components.blue_green_index_management import get_blue_index
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from ..components.popular_data_extracter import get_popular_books_df

load_dotenv()

embeddings = OpenAIEmbeddings()


def retrieve_semantic_recommendation(
                        query: str,
                        category: str = None,
                        tone: str = None,
                        initial_top_k: int = 50,
                        final_top_k: int = 16,
                    ) -> pd.DataFrame:
    try:
        index_name = get_blue_index()
        if index_name is None:
            return None
        
        vectorstore = Pinecone(
            index_name=index_name,
            embedding=embeddings
        )
        
        books = get_cleaned_books_df()
        
        recommendations = vectorstore.similarity_search(query, k=initial_top_k)

        rec_books_isbn_list = [int(recommendation.page_content.strip('"').split()[0]) for recommendation in recommendations]
        books_rec_list = books[books["isbn13"].isin(rec_books_isbn_list)].head(final_top_k)
        
        if category != "All":
            books_rec_list = books_rec_list[books_rec_list["simple_categories"] == category].head(final_top_k)
        else:
            books_rec_list = books_rec_list.head(final_top_k)

        if tone == "Happy":
            books_rec_list.sort_values(by="joy", ascending=False, inplace=True)
        elif tone == "Surprising":
            books_rec_list.sort_values(by="surprise", ascending=False, inplace=True)
        elif tone == "Angry":
            books_rec_list.sort_values(by="anger", ascending=False, inplace=True)
        elif tone == "Suspenseful":
            books_rec_list.sort_values(by="fear", ascending=False, inplace=True)
        elif tone == "Sad":
            books_rec_list.sort_values(by="sadness", ascending=False, inplace=True)

        return books_rec_list
    
    except Exception as ex:
        custom_logger.error("Error in retrieve_semantic_recommendation: %s", ex)
        return None


def recommend_book(query: str, category:str, tone:str):
    
    try:
        recommendations = retrieve_semantic_recommendation(query, category, tone)
        results = []
        
        for _, row in recommendations.iterrows():
            desc = row["description"]
            desc_split = desc.split()
            truncated_desc = " ".join(desc_split[:30]) + "..."
            
            authers_split = row["authors"].split(";")
            if len(authers_split) == 2:
                authers_str = f"{authers_split[0]} and {authers_split[1] }"
            elif len(authers_split) >= 2:
                authers_str = f"{', '.join(authers_split[:-1])} and {authers_split[-1] }"
            else:
                authers_str=row["authors"]
                
            caption = f"{row['title']} by {authers_str}: {truncated_desc}"
            results.append((row["large_thumbnail"], caption))
        return results
    
    except Exception as ex:
        custom_logger.error("Error in recommend_book: %s", ex)
        return None
    
    
def recommend_popular_books():
    
    try:
        books = get_cleaned_books_df()
        pop_books_list = get_popular_books_df()
        
        pop_books_isbn_list = pop_books_list["isbn13"].to_list()
        recommendations = books[books["isbn13"].isin(pop_books_isbn_list)]
        
        results = []
        
        for _, row in recommendations.iterrows():
            desc = row["description"]
            desc_split = desc.split()
            truncated_desc = " ".join(desc_split[:30]) + "..."
            
            authers_split = row["authors"].split(";")
            if len(authers_split) == 2:
                authers_str = f"{authers_split[0]} and {authers_split[1] }"
            elif len(authers_split) >= 2:
                authers_str = f"{', '.join(authers_split[:-1])} and {authers_split[-1] }"
            else:
                authers_str=row["authors"]
                
            caption = f"{row['title']} by {authers_str}: {truncated_desc}"
            results.append((row["large_thumbnail"], caption))
        return results
    
    except Exception as ex:
        custom_logger.error("Error in recommend_book: %s", ex)
        return None