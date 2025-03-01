import pandas as pd
import numpy as np
from transformers import pipeline
import concurrent.futures
from ..logger import get_logger
from tqdm import tqdm

custom_logger = get_logger()

llm_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", verbose=False)
fiction_categories = ["Fiction", "Nonfiction"]

def fill_missing_simple_cat(descriptions_list):
    results = []
    try:
        for text in tqdm(descriptions_list, leave=False, desc="Predicting Categories"):
            result = llm_pipe(text, fiction_categories)
            results.append(result["labels"][np.argmax(result["scores"])])
        return results
    except Exception as e:
        custom_logger.error("Error in fill_missing_simple_cat: %s", e)
        return [None] * len(descriptions_list)