from transformers import pipeline
from ..logger import custom_logger
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k = None)
emotion_labels = ["anger", "disgust", "fear", "joy", "sadness", "surprise", "neutral"]

def calculate_max_scores(predictions):
    try:
        per_emotion_scores = {label: [] for label in emotion_labels}
        for prediction in predictions:
            sorted_pred = sorted(prediction, key=lambda x: x["label"])
            for index, label in enumerate(emotion_labels):
                per_emotion_scores[label] += [sorted_pred[index]["score"]]
        return {label: np.max(scores) for label, scores in per_emotion_scores.items()}  
    
    except Exception as e:
        custom_logger.error("Error in calculate_max_scores: %s", e)
        return None


def calculate_emotion_scores(df: pd.DataFrame)-> pd.DataFrame:
    try:
        isbns = []
        emotion_scores = {label: [] for label in emotion_labels}
        
        for i in tqdm(range(len(df))):
            isbns.append(df["isbn13"][i])
            sentences = df["description"][i].split(".")
            predictions = emotion_classifier(sentences)
            max_scores = calculate_max_scores(predictions)
            for label in emotion_labels:
                emotion_scores[label].append(max_scores[label])
                
        emotions_df = pd.DataFrame(emotion_scores)
        emotions_df["isbn13"] = isbns
        
        return pd.merge(df, emotions_df, on="isbn13", how= "left")
    
    except Exception as e:
        custom_logger.error("Error in calculate_emotion_scores: %s", e)
        return None