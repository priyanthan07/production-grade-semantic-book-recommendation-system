# production-grade-semantic-book-recommendation-system

![image](https://github.com/user-attachments/assets/d0a48ab6-9a1e-483b-836a-179fabfd7264)

#### blog 1 : https://medium.com/@govindarajpriyanthan/building-a-semantic-book-recommendation-system-part-1-9159a16b3fce
#### blog 2 :
#### blog 3 :

## sample logs for periodic runner:
```
2025-03-02 09:50:32 [INFO] Starting periodic pipeline execution.
2025-03-02 09:50:32 [INFO] Running periodic data pipelines...
2025-03-02 09:50:32 [INFO] Starting data cleaning pipeline...
2025-03-02 09:50:32 [INFO] Getting query index...
2025-03-02 09:50:33 [INFO] Loading raw data from books table... Last index: 300
2025-03-02 09:50:33 [INFO] Retrieved 100 rows from books table.
2025-03-02 09:50:33 [INFO] Getting query index...
2025-03-02 09:50:33 [INFO] Updated query index to 400
2025-03-02 09:50:33 [INFO] Raw data loaded, shape: (100, 13)
2025-03-02 09:50:33 [INFO] Filtered out rows with missing critical fields, new shape: (99, 13)
2025-03-02 09:50:33 [INFO] Filtered out rows with short descriptions, new shape: (81, 14)
2025-03-02 09:50:33 [INFO] Mapping categories to simplified categories...
2025-03-02 09:50:33 [INFO] Filling missing simple_categories using LLM predictions...
2025-03-02 09:50:47 [INFO] Droped ['subtitle', 'word_counts_in_desc'] columns               
2025-03-02 09:50:47 [INFO] Adding tagged_description to DataFrame...
2025-03-02 09:50:47 [INFO] Cleaned data saved to cleaned_books table, shape: (81, 15)
2025-03-02 09:50:47 [INFO] Data cleaning pipeline completed successfully.
2025-03-02 09:50:47 [INFO] Starting sentiment analysis pipeline...
2025-03-02 09:50:47 [INFO] Calculating emotion scores for (81, 15)
2025-03-02 09:50:56 [INFO] Emotion scores calculated successfully: (81, 22)               
2025-03-02 09:50:56 [INFO] Saving cleaned data to preprocessed_books_data table...
2025-03-02 09:50:56 [INFO] Data successfully inserted into preprocessed_books_data
2025-03-02 09:50:56 [INFO] preprocessed data saved to database
2025-03-02 09:50:56 [INFO] Sentiment analysis pipeline completed successfully.
2025-03-02 09:50:56 [INFO] Starting popular recommendations pipeline...
2025-03-02 09:50:56 [INFO] Generating popularity-based recommendations...
2025-03-02 09:50:56 [INFO] Ratings count stats - min: 3.0, max: 547207.0, median: 3489.0
2025-03-02 09:50:56 [INFO] Average rating stats - min: 3.08, max: 4.5, median: 3.97
2025-03-02 09:50:56 [INFO] Found 79 books matching popularity criteria
2025-03-02 09:50:56 [INFO] Clearing previous data from popular_recommendations table...
2025-03-02 09:50:56 [INFO] Saving popular books data to popular_recommendations table. columns : isbn13, title, average_rating, ratings_count     
2025-03-02 09:50:56 [INFO] Data successfully inserted into popular_recommendations
2025-03-02 09:50:56 [INFO] Saved 10 popular recommendations to database
2025-03-02 09:50:56 [INFO] Popular recommendations pipeline completed successfully.
2025-03-02 09:50:56 [INFO] Starting vector database management...
2025-03-02 09:50:56 [INFO] Loading preprocessed data from preprocessed_books_data table...
2025-03-02 09:50:56 [INFO] preprocessed data loaded, shape: (249, 22)
2025-03-02 09:50:56 [INFO] Getting blue index...
2025-03-02 09:50:56 [INFO] Getting green index...
2025-03-02 09:50:56 [INFO] Active (blue) index: book-index2, Inactive (green) index: book-index1
2025-03-02 09:51:27 [INFO] Adding vectors to Pinecone. Initial index stats: {'dimension': 1536, 'index_fullness': 0.0, 'namespaces': {'': {'vector_count': 0}}, 'total_vector_count': 0}
Inserting vectors: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 32/32 [05:00<00:00,  9.38s/it]
2025-03-02 09:56:57 [INFO] All documents processed. Final index stats: {'dimension': 1536,'index_fullness': 0.0,'namespaces': {'default': {'vector_count': 249}},'total_vector_count': 249}
2025-03-02 09:56:57 [INFO] Validating green index: book-index1
2025-03-02 09:56:59 [INFO] Index 'book-index1' has 249 vectors.
2025-03-02 09:57:00 [INFO] Validation success: found 5 results for test query 'magic wizard adventure'.
2025-03-02 09:57:00 [INFO] Green index validation passed. Swapping indexes...
2025-03-02 09:57:00 [INFO] Saving blue index...
2025-03-02 09:57:00 [INFO] Saving green index...
2025-03-02 09:57:00 [INFO] Swapped: new blue index is 'book-index1', new green index is now 'book-index2'
2025-03-02 09:57:00 [INFO] Clearing index: book-index2
2025-03-02 09:57:01 [INFO] Index 'book-index2' cleared successfully.
2025-03-02 09:57:01 [INFO] Old blue index 'book-index2' cleared
2025-03-02 09:57:01 [INFO] Vector database management completed successfully.
2025-03-02 09:57:01 [INFO] Periodic pipeline completed successfully.
2025-03-02 09:57:01 [INFO] Periodic pipeline execution completed successfully.
2025-03-02 09:57:01 [INFO] ============   Total time taken: 388.78349781036377 seconds ==================================================
2025-03-02 10:00:32 [INFO] Starting periodic pipeline execution.
2025-03-02 10:00:32 [INFO] Running periodic data pipelines...
2025-03-02 10:00:32 [INFO] Starting data cleaning pipeline...
2025-03-02 10:00:32 [INFO] Getting query index...
2025-03-02 10:00:32 [INFO] Loading raw data from books table... Last index: 400
2025-03-02 10:00:33 [INFO] Retrieved 100 rows from books table.
2025-03-02 10:00:33 [INFO] Getting query index...
2025-03-02 10:00:33 [INFO] Updated query index to 500
2025-03-02 10:00:33 [INFO] Raw data loaded, shape: (100, 13)
2025-03-02 10:00:33 [INFO] Filtered out rows with missing critical fields, new shape: (89, 13)
2025-03-02 10:00:33 [INFO] Filtered out rows with short descriptions, new shape: (74, 14)
2025-03-02 10:00:33 [INFO] Mapping categories to simplified categories...
2025-03-02 10:00:33 [INFO] Droped ['subtitle', 'word_counts_in_desc'] columns
2025-03-02 10:00:33 [INFO] Adding tagged_description to DataFrame...
2025-03-02 10:00:33 [INFO] Cleaned data saved to cleaned_books table, shape: (74, 15)
2025-03-02 10:00:33 [INFO] Data cleaning pipeline completed successfully.
2025-03-02 10:00:33 [INFO] Starting sentiment analysis pipeline...
2025-03-02 10:00:33 [INFO] Calculating emotion scores for (74, 15)
2025-03-02 10:00:43 [INFO] Emotion scores calculated successfully: (74, 22)                                                        
2025-03-02 10:00:43 [INFO] Saving cleaned data to preprocessed_books_data table...
2025-03-02 10:00:43 [INFO] Data successfully inserted into preprocessed_books_data
2025-03-02 10:00:43 [INFO] preprocessed data saved to database
2025-03-02 10:00:43 [INFO] Sentiment analysis pipeline completed successfully.
2025-03-02 10:00:43 [INFO] Starting popular recommendations pipeline...
2025-03-02 10:00:43 [INFO] Generating popularity-based recommendations...
2025-03-02 10:00:43 [INFO] Ratings count stats - min: 3.0, max: 1592632.0, median: 3203.0
2025-03-02 10:00:43 [INFO] Average rating stats - min: 3.08, max: 4.61, median: 3.96
2025-03-02 10:00:43 [INFO] Found 98 books matching popularity criteria
2025-03-02 10:00:43 [INFO] Clearing previous data from popular_recommendations table...
2025-03-02 10:00:43 [INFO] Saving popular books data to popular_recommendations table. columns : isbn13, title, average_rating, ratings_count
2025-03-02 10:00:43 [INFO] Data successfully inserted into popular_recommendations
2025-03-02 10:00:43 [INFO] Saved 10 popular recommendations to database
2025-03-02 10:00:43 [INFO] Popular recommendations pipeline completed successfully.
2025-03-02 10:00:43 [INFO] Starting vector database management...
2025-03-02 10:00:43 [INFO] Loading preprocessed data from preprocessed_books_data table...
2025-03-02 10:00:43 [INFO] preprocessed data loaded, shape: (323, 22)
2025-03-02 10:00:43 [INFO] Getting blue index...
2025-03-02 10:00:43 [INFO] Getting green index...
2025-03-02 10:00:43 [INFO] Active (blue) index: book-index1, Inactive (green) index: book-index2
2025-03-02 10:01:14 [INFO] Adding vectors to Pinecone. Initial index stats: {'dimension': 1536,'index_fullness': 0.0,'namespaces': {'': {'vector_count': 0}},'total_vector_count': 0}
Inserting vectors: 100%|██████████████████████████████████████████████████████████████████████████| 41/41 [06:26<00:00,  9.44s/it]
2025-03-02 10:08:11 [INFO] All documents processed. Final index stats: {'dimension': 1536,'index_fullness': 0.0,'namespaces': {'default': {'vector_count': 323}},'total_vector_count': 323}
2025-03-02 10:08:11 [INFO] Validating green index: book-index2
2025-03-02 10:08:12 [INFO] Index 'book-index2' has 323 vectors.
2025-03-02 10:08:13 [INFO] Validation success: found 5 results for test query 'magic wizard adventure'.
2025-03-02 10:08:13 [INFO] Green index validation passed. Swapping indexes...
2025-03-02 10:08:13 [INFO] Saving blue index...
2025-03-02 10:08:13 [INFO] Saving green index...
2025-03-02 10:08:13 [INFO] Swapped: new blue index is 'book-index2', new green index is now 'book-index1'
2025-03-02 10:08:13 [INFO] Clearing index: book-index1
2025-03-02 10:08:15 [INFO] Index 'book-index1' cleared successfully.
2025-03-02 10:08:15 [INFO] Old blue index 'book-index1' cleared
2025-03-02 10:08:15 [INFO] Vector database management completed successfully.
2025-03-02 10:08:15 [INFO] Periodic pipeline completed successfully.
2025-03-02 10:08:15 [INFO] Periodic pipeline execution completed successfully.
2025-03-02 10:08:15 [INFO] ============   Total time taken: 462.26638174057007 seconds ==================================================

```
