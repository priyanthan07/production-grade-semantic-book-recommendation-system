import os
import pandas as pd
from dotenv import load_dotenv
from ..logger import get_logger
from ..components.blue_green_index_management import get_blue_index
from ..components.preprocessed_data_extracter import get_cleaned_books_df
from ..components.popular_data_extracter import get_popular_books_df
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from openai import OpenAI

load_dotenv()

client = OpenAI()
pc = Pinecone()
spec = ServerlessSpec(cloud="aws", region="us-east-1")

custom_logger = get_logger()

def retrieve_semantic_recommendation(
                        query: str,
                        category: str = None,
                        tone: str = None,
                        initial_top_k: int = 50,
                        final_top_k: int = 16,
                    ) -> pd.DataFrame:
    try:
        blue_index_name = get_blue_index()
        if blue_index_name is None:
            return None
        
        blue_index = pc.Index(blue_index_name)
        books = get_cleaned_books_df()
        query_embd = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding

        # A test query you expect to have relevant results
        recommendations = blue_index.query(vector=query_embd, top_k=5, include_metadata=True, namespace="default")

        rec_books_isbn_list = [int(recommendation['metadata']['text'].strip('"').split()[0]) for recommendation in recommendations['matches']]
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
        custom_logger.error(f"Error in retrieve_semantic_recommendation: {ex}", exc_info=True)
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
            results.append((row["thumbnail"], caption))
        return results
    
    except Exception as ex:
        custom_logger.error(f"Error in recommend_book: {ex}", exc_info=True)
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
            results.append((row["thumbnail"], caption))
        return results
    
    except Exception as ex:
        custom_logger.error(f"Error in recommend_popular_books: {ex}", exc_info=True)
        return None
    