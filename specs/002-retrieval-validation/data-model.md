# Data Model: RAG Data Retrieval and Pipeline Validation

## Entity: Query Request
- **query_text**: String - The text to search for semantically similar content
- **top_k**: Integer - Number of top results to retrieve (default: 5)
- **filters**: Dict - Optional filters to apply to the search (source URL, section, etc.)
- **metadata_fields**: List[String] - Which metadata fields to include in results (default: all)

## Entity: Retrieved Chunk
- **id**: String (UUID) - Unique identifier for the retrieved chunk
- **content**: String - The text content of the retrieved chunk
- **relevance_score**: Float - Cosine similarity score between query and chunk (0.0-1.0)
- **source_url**: String - URL where the original document was found
- **section**: String - Section title from the document
- **heading**: String - Heading hierarchy information
- **chunk_metadata**: Dict - Additional metadata from the original chunk
- **retrieved_at**: DateTime - Timestamp when the chunk was retrieved

## Entity: Validation Result
- **id**: String (UUID) - Unique identifier for the validation result
- **query_text**: String - The query used for validation
- **retrieved_chunks_count**: Integer - Number of chunks returned
- **avg_relevance_score**: Float - Average relevance score of retrieved chunks
- **validation_passed**: Boolean - Whether the validation criteria were met
- **issues_found**: List[String] - Any issues detected during validation
- **validation_timestamp**: DateTime - When the validation was performed
- **validation_metrics**: Dict - Additional metrics about the validation process

## Entity: Search Parameters
- **model_used**: String - The embedding model used for the search
- **similarity_threshold**: Float - Minimum similarity score to include in results
- **max_distance**: Float - Maximum distance allowed for results
- **search_filters**: Dict - Filters applied to the search
- **query_embedding**: List[Float] - Vector representation of the query text

## Relationships
- One `Query Request` can return many `Retrieved Chunk` entities
- One `Query Request` generates one `Validation Result`
- One `Search Parameters` applies to one `Query Request`

## Validation Rules
- `Query Request` query_text must not be empty
- `top_k` value must be greater than 0 and less than or equal to 100
- `relevance_score` in `Retrieved Chunk` must be between 0.0 and 1.0
- `Validation Result` must have at least one retrieved chunk to be valid
- `Search Parameters` model_used must match the model used for stored embeddings

## State Transitions
- `Query Request`: Pending → Processing → Completed/Failed
- `Validation Result`: Initialized → In Progress → Passed/Failed
- `Retrieved Chunk`: Retrieved → Validated → Returned to User