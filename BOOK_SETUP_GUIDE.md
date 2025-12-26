# Setup Instructions for Physical AI Humanoids Book RAG System

## 1. Environment Variables

Create a `.env` file in the `backend` directory with your Qdrant credentials:

```env
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

Example:
```env
QDRANT_URL=https://your-cluster-name.us-east1-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_secret_api_key_here
```

## 2. Files Created

The following files have been created in the `backend` directory:

### Core Scripts:
- `ingest_book.py` - Main ingestion script for your Physical AI Humanoids book
- `verify_book_ingestion.py` - Verification script to check successful ingestion
- `query_book.py` - Query script to retrieve relevant chunks from your book
- `test_book_system.py` - Test script to verify all systems work

### Documentation:
- `BOOK_RAG_README.md` - Complete usage guide

## 3. How to Use

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Set Environment Variables
```bash
# On Windows (Command Prompt)
set QDRANT_URL=your_url
set QDRANT_API_KEY=your_key

# On Windows (PowerShell)
$env:QDRANT_URL="your_url"
$env:QDRANT_API_KEY="your_key"

# Or create a .env file in the backend directory
```

### Step 3: Ingest Your Book
```bash
cd backend
python ingest_book.py "path/to/your/Physical_AI_Humanoids_Book.pdf"
```

### Step 4: Verify Ingestion
```bash
python verify_book_ingestion.py
```

### Step 5: Query Your Book
```bash
python query_book.py "What are the key components of humanoid robots?"
```

## 4. Features

✅ **Semantic Chunking**: 300-500 word chunks with 50-100 word overlap
✅ **384-Dim Embeddings**: Compatible with your Qdrant collection
✅ **Proper Metadata**: Each chunk includes source, chunk number, word count
✅ **Error Handling**: Comprehensive logging and error management
✅ **PDF/TXT Support**: Works with both PDF and text files
✅ **Integration Ready**: Works with your existing RAG system

## 5. Collection Details

- **Collection Name**: `test_ingestion_custom`
- **Vector Size**: 384 dimensions (matches your requirements)
- **Distance Metric**: Cosine
- **Embedding Model**: BAAI/bge-small-en-v1.5 (produces 384-dim vectors)
- **Source Label**: "Physical AI Humanoid Book"

## 6. Integration with Existing System

Your existing RAG system continues to work:
- `python ask_endpoint.py` - API endpoint
- `python terminal_chatbot.py` - Interactive terminal chat
- The new book content will be available in queries to your existing system

## 7. Troubleshooting

- **Collection Not Found**: Ensure Qdrant is running and credentials are correct
- **File Not Found**: Verify the path to your book file
- **API Key Issues**: Check that QDRANT_API_KEY and QDRANT_URL are set correctly
- **Connection Issues**: Verify network connectivity to your Qdrant instance