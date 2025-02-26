import pandas as pd
import numpy as np
from transformers import pipeline
import concurrent.futures
from ..logger import custom_logger
from tqdm.auto import tqdm

llm_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
fiction_categories = ["Fiction", "Nonfiction"]

def fill_missing_simple_cat(text):
    try:
        result = llm_pipe(text, fiction_categories)
        return result["labels"][np.argmax(result["scores"])]

    except Exception as e:
        custom_logger.error("Error in fill_missing_simple_cat: %s", e)
        return None
    
def fill_missing_simple_cat_parallel(descriptions, max_workers=8):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(tqdm(executor.map(fill_missing_simple_cat, descriptions),total=len(descriptions), desc="LLM Predictions"))
        return results
    
    except Exception as e:
        custom_logger.error("Error in fill_missing_simple_cat_parallel: %s", e)
        return None