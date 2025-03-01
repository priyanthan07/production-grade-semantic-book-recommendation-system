from transformers import pipeline
from ..logger import get_logger
import numpy as np
import time
import pandas as pd
from tqdm import tqdm

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k = None, verbose=False)
emotion_labels = ["anger", "disgust", "fear", "joy", "sadness", "surprise", "neutral"]

custom_logger = get_logger()

def safe_emotion_classifier(sentences, retries=2, delay=1):
    if not sentences:
        return []
        
    for attempt in range(retries + 1):  # +1 because range is 0-based
        try:
            result = emotion_classifier(sentences)
            if isinstance(result, list):
                return result
            else:
                custom_logger.warning(f"Unexpected result type: {type(result)}")
                
            if attempt < retries:
                custom_logger.debug(f"Retrying classifier (attempt {attempt+1}/{retries})")
                time.sleep(delay)
        except Exception as e:
            custom_logger.warning(f"Error in emotion_classifier (attempt {attempt+1}/{retries}): {str(e)}")
            if attempt < retries:
                time.sleep(delay)
            
    # If we've exhausted all retries, return an empty list
    return []

def calculate_max_scores(predictions):
    try:
        # Initialize dictionary with all emotion labels
        per_emotion_scores = {label: [] for label in emotion_labels}
        
        # Check if predictions is a valid list
        if not predictions or not isinstance(predictions, list):
            custom_logger.warning("Empty or invalid predictions list.")
            return None
        
        for prediction in predictions:
            # Check if this individual prediction is valid
            if not prediction or not isinstance(prediction, list):
                custom_logger.debug("Skipping invalid prediction item.")
                continue
                
            # Check if we have the right number of items
            if len(prediction) != len(emotion_labels):
                custom_logger.debug(f"Prediction has wrong number of labels: {len(prediction)} vs expected {len(emotion_labels)}")
                continue
            
            # Sort prediction by label to ensure consistent ordering
            try:
                sorted_pred = sorted(prediction, key=lambda x: x["label"])
                
                # Add each score to the appropriate list
                for index, label in enumerate(emotion_labels):
                    if index < len(sorted_pred):
                        per_emotion_scores[label].append(sorted_pred[index]["score"])
            except (KeyError, TypeError) as e:
                custom_logger.debug(f"Error processing prediction: {str(e)}")
                continue
        
        # Make sure we have scores for each emotion
        result = {}
        for label, scores in per_emotion_scores.items():
            if scores:  # Only include emotions with at least one score
                result[label] = np.max(scores)
            else:
                result[label] = 0.0  # Default score if none found
        
        return result
        
    except Exception as e:
        custom_logger.error(f"Error in calculate_max_scores: {str(e)}")
        return None


def calculate_emotion_scores(df: pd.DataFrame) -> pd.DataFrame:
    try:
        custom_logger.info("Calculating emotion scores for %s", df.shape)
        result_data = {
            'isbn13': [],
        }
        # Initialize result dictionary with emotion labels
        for label in emotion_labels:
            result_data[label] = []
            
        # Reset index to avoid index issues
        df = df.reset_index(drop=True)
        
        try:
            for i in tqdm(range(len(df)), desc="Calculating Emotion Scores", leave=False):
                try:
                    isbn = df.loc[i, "isbn13"]
                    description = df.loc[i, "description"]
                    
                    # Add the ISBN to our results
                    result_data['isbn13'].append(isbn)
                    
                    # Skip if description is missing
                    if pd.isna(description) or not isinstance(description, str):
                        custom_logger.warning(f"Missing or invalid description for ISBN {isbn}")
                        # Add None values for all emotion scores for this row
                        for label in emotion_labels:
                            result_data[label].append(None)
                        continue
                    
                    # Process the text
                    sentences = description.split(".")
                    # Filter out empty sentences
                    sentences = [s.strip() for s in sentences if s.strip()]
                    
                    if not sentences:
                        custom_logger.warning(f"No valid sentences for ISBN {isbn}")
                        # Add None values for all emotion scores
                        for label in emotion_labels:
                            result_data[label].append(None)
                        continue
                    
                    predictions = safe_emotion_classifier(sentences)
                    max_scores = calculate_max_scores(predictions)
                    
                    if not max_scores:
                        custom_logger.warning(f"No valid emotion scores for ISBN {isbn}")
                        # Add None values for all emotion scores
                        for label in emotion_labels:
                            result_data[label].append(None)
                        continue
                    
                    # Add the emotion scores to our results
                    for label in emotion_labels:
                        result_data[label].append(max_scores.get(label, None))
                        
                except Exception as e:
                    custom_logger.error(f"Error processing item {i} (ISBN: {df.iloc[i].get('isbn13', 'unknown')}): {str(e)}")
                    # Add None values for all emotion scores for this row
                    for label in emotion_labels:
                        result_data[label].append(None)
            
            # Create DataFrame from results
            emotions_df = pd.DataFrame(result_data)
            
            # Merge with original DataFrame
            return pd.merge(df, emotions_df, on="isbn13", how="left")
            
        except Exception as e:
            custom_logger.error(f"Error in processing loop: {str(e)}")
            return df
            
    except Exception as e:
        custom_logger.error(f"Error in calculate_emotion_scores: {str(e)}")
        return df
    