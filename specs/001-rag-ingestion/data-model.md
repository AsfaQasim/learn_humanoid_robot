# Data Model: Documentation Ingestion Pipeline for RAG System

## Entity: Document Chunk
- **id**: String (UUID) - Unique identifier for the chunk
- **content**: String - The text content of the chunk
- **source_url**: String - URL where the original document was found
- **section**: String - Section title from the document
- **heading**: String - Heading hierarchy information
- **metadata**: Dict - Additional metadata (timestamp, etc.)
- **embedding**: List[float] - Vector representation of the content

## Entity: Metadata Record
- **id**: String (UUID) - Unique identifier
- **source_url**: String - Original URL of the document
- **section_title**: String - Section or page title
- **heading_hierarchy**: String - Hierarchy of headings
- **created_at**: DateTime - Timestamp of creation
- **processed_at**: DateTime - Timestamp when processing completed
- **chunk_count**: Integer - Number of chunks created from this document

## Entity: Vector Representation
- **id**: String (UUID) - Unique identifier
- **vector**: List[float] - The embedding vector
- **chunk_id**: String - Reference to the source chunk
- **model_used**: String - Name of the embedding model used
- **created_at**: DateTime - Timestamp of vector creation
- **metadata**: Dict - Associated metadata (URL, section, etc.)

## Relationships
- One `Metadata Record` can have many `Document Chunk` entities
- One `Document Chunk` has one `Vector Representation`
- `Vector Representation` references back to `Document Chunk` via chunk_id

## Validation Rules
- `Document Chunk` content must not be empty
- `source_url` must be a valid URL format
- `embedding` vector must have consistent dimensions
- `Metadata Record` must have a valid timestamp
- `chunk_id` in `Vector Representation` must reference an existing chunk

## State Transitions
- `Metadata Record`: Created → Processing → Processed → Stored
- `Document Chunk`: Extracted → Chunked → Embedded → Indexed
- `Vector Representation`: Generated → Validated → Stored → Queryable